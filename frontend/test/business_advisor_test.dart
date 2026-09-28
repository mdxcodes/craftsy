import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:craftsy/features/home/screens/business_advisor_screen.dart';
import 'package:craftsy/data/models/product.dart';
import 'package:craftsy/data/services/api_service.dart';
import 'package:craftsy/core/providers/app_providers.dart';

class _FakeProductListNotifier extends StateNotifier<AsyncValue<List<Product>>>
    implements ProductListNotifier {
  _FakeProductListNotifier(List<Product> products)
    : super(AsyncValue.data(products));

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
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
    'Business Advisor renders suggestion cards',
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
        Product(
          id: 'p2',
          title: 'Bamboo Basket',
          description: 'Woven basket',
          price: 300.0,
          photoPath: '/tmp/basket.jpg',
          category: 'Bamboo',
          status: ProductStatus.soldOut,
          stock: 0,
          createdAt: DateTime.now(),
        ),
      ];

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            apiServiceProvider.overrideWithValue(MockApiService()),
            productListProvider.overrideWith(
              (ref) => _FakeProductListNotifier(products),
            ),
          ],
          child: const MaterialApp(
            home: BusinessAdvisorScreen(),
          ),
        ),
      );

      await tester.pump(const Duration(seconds: 2));

      expect(find.text('AI Business Advisor'), findsOneWidget);
      expect(find.text('Here are some suggestions for your business'), findsOneWidget);
      expect(find.text('Price Review Needed'), findsOneWidget);
      expect(find.text('Low Stock Alert'), findsOneWidget);
      expect(find.text('Slow Moving Products'), findsOneWidget);
      expect(find.text('Festival Demand Opportunity'), findsOneWidget);
      expect(find.text('Ask AI Advisor'), findsOneWidget);
    },
  );

  testWidgets(
    'Business Advisor shows empty message when no products',
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

      await tester.pump(const Duration(seconds: 2));

      expect(find.text('AI Business Advisor'), findsOneWidget);
      expect(find.text('Add products to get price recommendations.'), findsOneWidget);
    },
  );
}
