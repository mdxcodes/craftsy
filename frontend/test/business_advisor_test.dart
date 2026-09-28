import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:craftsy/features/home/screens/business_advisor_screen.dart';
import 'package:craftsy/data/models/product.dart';
import 'package:craftsy/data/services/api_service.dart';
import 'package:craftsy/data/services/advisor_service.dart';
import 'package:craftsy/core/providers/app_providers.dart';

class _FakeProductListNotifier extends StateNotifier<AsyncValue<List<Product>>>
    implements ProductListNotifier {
  _FakeProductListNotifier(List<Product> products)
    : super(AsyncValue.data(products));

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

class _FakeAdvisorService implements AdvisorService {
  _FakeAdvisorService(this._response);
  final AdvisorAnalysisResponse _response;

  @override
  Future<AdvisorAnalysisResponse> analyzeCatalog(List<AdvisorProductSummary> products) async {
    return _response;
  }
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() async {
    final tempDir = await Directory.systemTemp.createTemp(
      'hive_business_advisor_test',
    );
    Hive.init(tempDir.path);

    if (!Hive.isAdapterRegistered(1)) {
      Hive.registerAdapter(ProductStatusAdapter());
    }
    if (!Hive.isAdapterRegistered(0)) {
      Hive.registerAdapter(ProductAdapter());
    }

    if (!Hive.isBoxOpen('products_box')) {
      await Hive.openBox<Product>('products_box');
    }
    if (!Hive.isBoxOpen('pending_sync_box')) {
      await Hive.openBox<String>('pending_sync_box');
    }
  });

  testWidgets(
    'Business Advisor renders with products',
    (WidgetTester tester) async {
      final products = [
        Product(
          id: 'p1',
          title: 'Handcrafted Vase',
          description: 'A beautiful vase',
          price: 500.0,
          photoPath: '/tmp/vase.jpg',
          category: 'Pottery',
          status: ProductStatus.live,
          stock: 3,
          createdAt: DateTime.now(),
        ),
      ];

      final fakeService = _FakeAdvisorService(
        AdvisorAnalysisResponse(
          advice: [
            AdvisorSuggestion(
              productId: 'p1',
              productTitle: 'Handcrafted Vase',
              adviceType: 'low_stock',
              priority: 'high',
              title: 'Low Stock Alert',
              description: 'Handcrafted Vase\nCurrent Stock: 3\nSuggested Stock: 10',
              suggestedAction: 'update_stock',
              suggestedStock: 10,
              currentStock: 3,
            ),
          ],
          totalProducts: 1,
          productsNeedingAttention: 1,
        ),
      );

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            apiServiceProvider.overrideWithValue(MockApiService()),
            productListProvider.overrideWith(
              (ref) => _FakeProductListNotifier(products),
            ),
            advisorServiceProvider.overrideWith((_) => fakeService),
          ],
          child: const MaterialApp(
            home: BusinessAdvisorScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle(const Duration(seconds: 2));

      expect(find.text('AI Business Advisor'), findsOneWidget);
      expect(find.text('Low Stock Alert'), findsOneWidget);
      expect(find.text('Update Stock'), findsOneWidget);
    },
  );

  testWidgets(
    'Business Advisor shows empty state when no products',
    (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            apiServiceProvider.overrideWithValue(MockApiService()),
            productListProvider.overrideWith(
              (ref) => _FakeProductListNotifier([]),
            ),
          ],
          child: const MaterialApp(
            home: BusinessAdvisorScreen(),
          ),
        ),
      );

      await tester.pumpAndSettle(const Duration(seconds: 2));

      expect(find.text('AI Business Advisor'), findsOneWidget);
      expect(find.text('Add products to get personalized business advice.'), findsOneWidget);
    },
  );
}
