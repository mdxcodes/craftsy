import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:craftsy/features/home/screens/business_advisor_screen.dart';
import 'package:craftsy/data/models/product.dart';
import 'package:craftsy/data/services/api_service.dart';
import 'package:craftsy/core/providers/app_providers.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

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
    'Business Advisor renders with products from canonical provider',
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
            localizationsDelegates: [
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ],
            supportedLocales: [Locale('en')],
            home: BusinessAdvisorScreen(),
          ),
        ),
      );

      await tester.pump(const Duration(seconds: 2));

      // Verify screen renders — product titles are plain data, not localized
      // Products may appear in multiple sections (price review, low stock, slow moving)
      expect(find.text('Handcrafted Vase'), findsWidgets);
      expect(find.text('Bamboo Basket'), findsWidgets);
      expect(find.text('₹500'), findsOneWidget);

      // Verify section headers (Easy Localization returns key when not loaded)
      expect(find.text('advisor_price_review'), findsOneWidget);
      expect(find.text('advisor_low_stock'), findsOneWidget);
      expect(find.text('advisor_slow_moving'), findsOneWidget);

      // Scroll to find CTA button at bottom
      await tester.scrollUntilVisible(
        find.text('advisor_ask_craftmitra'),
        200,
        scrollable: find.byType(Scrollable).first,
      );
      expect(find.text('advisor_ask_craftmitra'), findsOneWidget);
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
            localizationsDelegates: [
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ],
            supportedLocales: [Locale('en')],
            home: BusinessAdvisorScreen(),
          ),
        ),
      );

      await tester.pump(const Duration(seconds: 2));

      expect(find.text('advisor_title'), findsOneWidget);
      expect(find.text('advisor_no_products'), findsOneWidget);
      expect(find.text('advisor_add_product'), findsOneWidget);
    },
  );
}
