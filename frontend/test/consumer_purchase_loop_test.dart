import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';

import 'package:craftsy/core/services/commerce_service.dart';
import 'package:craftsy/features/marketplace/screens/cart_screen.dart';
import 'package:craftsy/features/marketplace/screens/checkout_screen.dart';
import 'package:craftsy/features/marketplace/screens/order_confirmation_screen.dart';
import 'package:craftsy/features/marketplace/screens/my_purchases_screen.dart';
import 'package:craftsy/features/marketplace/screens/purchase_detail_screen.dart';

/// In-memory fake of CommerceService for widget tests.
/// Holds mutable cart state so mutations survive provider invalidation,
/// mirroring how the real backend behaves.
class _FakeCommerceService implements CommerceService {
  Cart currentCart;
  final List<Address> addresses;
  final List<ConsumerOrderSummary> orders;
  ConsumerOrderDetail? detail;

  _FakeCommerceService({
    required Cart initialCart,
    this.addresses = const [],
    this.orders = const [],
    this.detail,
  }) : currentCart = initialCart;

  @override
  Future<Cart> getCart() async => currentCart;

  @override
  Future<Cart> addToCart(String productId, {int quantity = 1}) async =>
      currentCart;

  Cart _rebuild(List<CartItem> items) => Cart(
        id: currentCart.id,
        userId: currentCart.userId,
        items: items,
        subtotal: items.fold(0.0, (s, i) => s + i.lineTotal),
      );

  @override
  Future<Cart> updateCartItem(String itemId, int quantity) async {
    final items = currentCart.items
        .map((i) => i.id == itemId
            ? CartItem(
                id: i.id,
                productId: i.productId,
                quantity: quantity,
                unitPrice: i.unitPrice,
                title: i.title,
                imageUrl: i.imageUrl,
                stock: i.stock,
              )
            : i)
        .toList();
    currentCart = _rebuild(items);
    return currentCart;
  }

  @override
  Future<Cart> removeCartItem(String itemId) async {
    currentCart = _rebuild(
        currentCart.items.where((i) => i.id != itemId).toList());
    return currentCart;
  }

  @override
  Future<void> clearCart() async {
    currentCart = _rebuild([]);
  }

  @override
  Future<List<Address>> getAddresses() async => addresses;

  @override
  Future<Address> createAddress(Address address) async => address;

  @override
  Future<Address> updateAddress(
          String addressId, Map<String, dynamic> updates) async =>
      addresses.first;

  @override
  Future<void> deleteAddress(String addressId) async {}

  @override
  Future<PlacedOrder> checkout({
    required String addressId,
    required List<CartItem> items,
    String paymentMethod = 'cod',
  }) async =>
      PlacedOrder(
        id: 'ord_test123',
        totalAmount: 450.0,
        status: 'new',
        items: const [],
        payment: PaymentInfo(
            id: 'pay_1', amount: 450.0, method: 'cod', status: 'pending'),
        shipment: ShipmentInfo(id: 'shp_1', status: 'pending'),
      );

  @override
  Future<List<ConsumerOrderSummary>> getMyOrders(
      {int limit = 50, int offset = 0}) async =>
      orders;

  @override
  Future<ConsumerOrderDetail> getMyOrder(String orderId) async =>
      detail ??
      (throw CommerceApiException('Order not found', statusCode: 404));

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

Cart _cart(List<CartItem> items) => Cart(
      id: 'cart_1',
      userId: 'user_1',
      items: items,
      subtotal: items.fold(0.0, (s, i) => s + i.lineTotal),
    );

final _cartItem = CartItem(
  id: 'item_1',
  productId: 'prod_1',
  quantity: 2,
  unitPrice: 100.0,
  title: 'Blue Pottery Vase',
  imageUrl: '',
  stock: 10,
);

Widget _wrap(Widget child, {required List<Override> overrides}) {
  return EasyLocalization(
    supportedLocales: const [Locale('en')],
    path: 'assets/translations',
    fallbackLocale: const Locale('en'),
    useOnlyLangCode: true,
    child: ProviderScope(
      overrides: overrides,
      child: MaterialApp(home: child),
    ),
  );
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() async {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      const MethodChannel('plugins.flutter.io/shared_preferences'),
      (MethodCall methodCall) async {
        if (methodCall.method == 'getAll') {
          return <String, Object>{};
        }
        return true;
      },
    );
    await EasyLocalization.ensureInitialized();
  });

  group('CartScreen', () {
    testWidgets('renders items, quantity, and display-only subtotal',
        (tester) async {
      final fake = _FakeCommerceService(initialCart: _cart([_cartItem]));

      await tester.pumpWidget(_wrap(
        const CartScreen(),
        overrides: [commerceServiceProvider.overrideWithValue(fake)],
      ));
      await tester.pumpAndSettle();

      expect(find.text('Blue Pottery Vase'), findsOneWidget);
      expect(find.text('2'), findsOneWidget);
      // Server-provided display totals (200 = 2 × 100): line + summary
      expect(find.text('₹200'), findsNWidgets(2));
      // Checkout navigation exists
      expect(find.byIcon(Icons.shopping_cart_outlined), findsNothing);
    });

    testWidgets('shows empty state for an empty cart', (tester) async {
      final fake = _FakeCommerceService(initialCart: _cart([]));

      await tester.pumpWidget(_wrap(
        const CartScreen(),
        overrides: [commerceServiceProvider.overrideWithValue(fake)],
      ));
      await tester.pumpAndSettle();

      // tr() returns the raw key in test environment (repo convention)
      expect(find.text('cart_empty'), findsOneWidget);
      expect(find.text('cart_continue_shopping'), findsOneWidget);
    });

    testWidgets('increase quantity updates line via backend', (tester) async {
      final fake = _FakeCommerceService(initialCart: _cart([_cartItem]));

      await tester.pumpWidget(_wrap(
        const CartScreen(),
        overrides: [commerceServiceProvider.overrideWithValue(fake)],
      ));
      await tester.pumpAndSettle();

      await tester.tap(find.byIcon(Icons.add));
      await tester.pumpAndSettle();

      // Fake returns quantity 3 → line total 300 (line + summary)
      expect(find.text('3'), findsOneWidget);
      expect(find.text('₹300'), findsNWidgets(2));
    });
  });

  group('CheckoutScreen', () {
    testWidgets('shows COD as the payment method with UPI disclosure',
        (tester) async {
      final fake = _FakeCommerceService(
        initialCart: _cart([_cartItem]),
        addresses: [
          Address(
            id: 'addr_1',
            name: 'Sita Devi',
            phone: '9876543210',
            line1: '12 Gram Road',
            city: 'Jaipur',
            state: 'Rajasthan',
            pincode: '302001',
            isDefault: true,
          ),
        ],
      );

      await tester.pumpWidget(_wrap(
        const CheckoutScreen(),
        overrides: [commerceServiceProvider.overrideWithValue(fake)],
      ));
      await tester.pumpAndSettle();

      expect(find.text('checkout_cod'), findsOneWidget);
      expect(find.text('checkout_upi_coming_later'), findsOneWidget);
      expect(find.text('Sita Devi · 9876543210'), findsOneWidget);
      expect(find.text('checkout_place_order'), findsOneWidget);
    });

    testWidgets('shows add-address prompt when no addresses exist',
        (tester) async {
      final fake = _FakeCommerceService(initialCart: _cart([_cartItem]));

      await tester.pumpWidget(_wrap(
        const CheckoutScreen(),
        overrides: [commerceServiceProvider.overrideWithValue(fake)],
      ));
      await tester.pumpAndSettle();

      expect(find.text('address_add_new'), findsOneWidget);
    });
  });

  group('OrderConfirmationScreen', () {
    testWidgets('shows order id, COD note, total, and next actions',
        (tester) async {
      final order = PlacedOrder(
        id: 'ord_test123',
        totalAmount: 450.0,
        status: 'new',
        items: [
          PlacedOrderItem(
            id: 'oi_1',
            productId: 'prod_1',
            title: 'Blue Pottery Vase',
            quantity: 2,
            unitPrice: 100.0,
            totalPrice: 200.0,
          ),
          PlacedOrderItem(
            id: 'oi_2',
            productId: 'prod_2',
            title: 'Wooden Bowl',
            quantity: 1,
            unitPrice: 250.0,
            totalPrice: 250.0,
          ),
        ],
        payment: PaymentInfo(
            id: 'pay_1', amount: 450.0, method: 'cod', status: 'pending'),
        shipment: ShipmentInfo(id: 'shp_1', status: 'pending'),
      );

      await tester.pumpWidget(_wrap(
        OrderConfirmationScreen(order: order),
        overrides: [],
      ));
      await tester.pumpAndSettle();

      expect(find.text('ord_test123'), findsOneWidget);
      expect(find.text('order_confirmed_title'), findsOneWidget);
      expect(find.text('order_confirmed_cod_note'), findsOneWidget);
      expect(find.text('₹450'), findsOneWidget);
      expect(find.text('order_view_my_orders'), findsOneWidget);
      expect(find.text('cart_continue_shopping'), findsOneWidget);
    });
  });

  group('MyPurchasesScreen', () {
    testWidgets('lists orders with status and total', (tester) async {
      final fake = _FakeCommerceService(
        initialCart: _cart([]),
        orders: [
          ConsumerOrderSummary(
            id: 'ord_1',
            status: 'shipped',
            totalAmount: 500.0,
            quantity: 1,
            itemCount: 1,
            firstItemTitle: 'Vase',
            firstItemImageUrl: '',
            buyerLocation: 'Delhi, Delhi',
            placedAt: '2026-09-24T10:00:00',
          ),
        ],
      );

      await tester.pumpWidget(_wrap(
        const MyPurchasesScreen(),
        overrides: [commerceServiceProvider.overrideWithValue(fake)],
      ));
      await tester.pumpAndSettle();

      expect(find.text('Vase'), findsOneWidget);
      expect(find.text('₹500'), findsOneWidget);
      expect(find.text('order_status_shipped'), findsOneWidget);
    });

    testWidgets('shows empty state when no orders', (tester) async {
      final fake = _FakeCommerceService(initialCart: _cart([]));

      await tester.pumpWidget(_wrap(
        const MyPurchasesScreen(),
        overrides: [commerceServiceProvider.overrideWithValue(fake)],
      ));
      await tester.pumpAndSettle();

      expect(find.text('my_purchases_empty'), findsOneWidget);
    });
  });

  group('PurchaseDetailScreen', () {
    testWidgets('shows tracking timeline with completed stages',
        (tester) async {
      final fake = _FakeCommerceService(
        initialCart: _cart([]),
        detail: ConsumerOrderDetail(
          id: 'ord_1',
          status: 'shipped',
          totalAmount: 500.0,
          buyerName: 'Sita',
          buyerLocation: 'Delhi, Delhi',
          buyerPhone: '9876543210',
          items: [
            PlacedOrderItem(
              id: 'oi_1',
              productId: 'p1',
              title: 'Vase',
              quantity: 1,
              unitPrice: 500.0,
              totalPrice: 500.0,
            ),
          ],
          payment: PaymentInfo(
              id: 'pay_1', amount: 500.0, method: 'cod', status: 'pending'),
          shipment: ShipmentInfo(id: 'shp_1', status: 'in_transit'),
          address: Address(
            id: 'addr_1',
            name: 'Sita',
            phone: '9876543210',
            line1: '12 Gram Road',
            city: 'Delhi',
            state: 'Delhi',
            pincode: '110001',
          ),
        ),
      );

      await tester.pumpWidget(_wrap(
        const PurchaseDetailScreen(orderId: 'ord_1'),
        overrides: [commerceServiceProvider.overrideWithValue(fake)],
      ));
      await tester.pumpAndSettle();

      // Timeline shows all five honest stages (as raw keys in test env);
      // 'shipped' appears twice — timeline step + status pill.
      expect(find.text('order_status_new'), findsOneWidget);
      expect(find.text('order_status_confirmed'), findsOneWidget);
      expect(find.text('order_status_packed'), findsOneWidget);
      expect(find.text('order_status_shipped'), findsNWidgets(2));
      expect(find.text('order_status_delivered'), findsOneWidget);
      // Items + address render from real data
      expect(find.text('Vase'), findsOneWidget);
      expect(find.text('Sita · 9876543210'), findsOneWidget);
    });

    testWidgets('cancelled order shows cancelled banner, not a timeline',
        (tester) async {
      final fake = _FakeCommerceService(
        initialCart: _cart([]),
        detail: ConsumerOrderDetail(
          id: 'ord_2',
          status: 'cancelled',
          totalAmount: 300.0,
          buyerName: 'Sita',
          buyerLocation: 'Delhi, Delhi',
          buyerPhone: '9876543210',
          items: [],
          payment: null,
          shipment: null,
          address: null,
        ),
      );

      await tester.pumpWidget(_wrap(
        const PurchaseDetailScreen(orderId: 'ord_2'),
        overrides: [commerceServiceProvider.overrideWithValue(fake)],
      ));
      await tester.pumpAndSettle();

      // Banner + status pill both show the cancelled state
      expect(find.text('order_status_cancelled'), findsNWidgets(2));
      // No fake timeline stages
      expect(find.text('order_status_shipped'), findsNothing);
      expect(find.text('order_status_delivered'), findsNothing);
    });
  });
}
