import 'dart:convert';
import 'dart:typed_data';

import 'package:dio/dio.dart';
import 'package:dio/src/adapter.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:craftsy/core/services/commerce_service.dart';

/// Captures requests and returns canned responses — no real network.
class _FakeAdapter implements HttpClientAdapter {
  final ResponseBody Function(RequestOptions options) handler;
  final List<RequestOptions> requests = [];

  _FakeAdapter(this.handler);

  @override
  void close({bool force = false}) {}

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? requestStream,
    Future<void>? cancelFuture,
  ) async {
    requests.add(options);
    return handler(options);
  }
}

CommerceService _serviceWith(ResponseBody Function(RequestOptions) handler) {
  final dio = Dio();
  final adapter = _FakeAdapter(handler);
  dio.httpClientAdapter = adapter;
  return CommerceService(
    dio: dio,
    tokenProvider: () async => 'mock_jwt_token_9876543210',
  );
}

ResponseBody _ok(Map<String, dynamic> json) => ResponseBody.fromString(
      jsonEncode(json),
      200,
    );

void main() {
  group('CommerceService — cart', () {
    test('getCart sends Bearer token and parses cart with subtotal',
        () async {
      late RequestOptions captured;
      final service = _serviceWith((options) {
        captured = options;
        return _ok({
          'id': 'cart_1',
          'user_id': 'user_1',
          'subtotal': 450.0,
          'items': [
            {
              'id': 'item_1',
              'product_id': 'prod_1',
              'quantity': 2,
              'unit_price': 100.0,
              'title': 'Blue Pottery Vase',
              'image_url': '/uploads/x.jpg',
              'stock': 10,
            },
            {
              'id': 'item_2',
              'product_id': 'prod_2',
              'quantity': 1,
              'unit_price': 250.0,
              'title': 'Wooden Bowl',
              'image_url': '',
              'stock': 3,
            },
          ],
        });
      });

      final cart = await service.getCart();

      expect(captured.headers['Authorization'],
          'Bearer mock_jwt_token_9876543210');
      expect(captured.uri.path, '/api/v1/cart');
      expect(cart.items.length, 2);
      expect(cart.subtotal, 450.0);
      expect(cart.itemCount, 3);
      expect(cart.items[0].title, 'Blue Pottery Vase');
      expect(cart.items[0].lineTotal, 200.0);
      expect(cart.items[0].stock, 10);
    });

    test('addToCart posts product id and quantity', () async {
      late RequestOptions captured;
      final service = _serviceWith((options) {
        captured = options;
        return _ok({
          'id': 'cart_1',
          'user_id': 'user_1',
          'subtotal': 500.0,
          'items': [
            {
              'id': 'item_1',
              'product_id': 'prod_1',
              'quantity': 2,
              'unit_price': 500.0,
              'title': 'T',
              'image_url': '',
              'stock': 5,
            }
          ],
        });
      });

      await service.addToCart('prod_1', quantity: 2);

      expect(captured.method, 'POST');
      expect(captured.uri.path, '/api/v1/cart/items');
      expect(captured.data, {'product_id': 'prod_1', 'quantity': 2});
    });

    test('server stock error (409) surfaces as CommerceApiException',
        () async {
      final service = _serviceWith((options) => ResponseBody.fromString(
            jsonEncode({'detail': 'Only 2 left for Blue Vase'}),
            409,
          ));

      await expectLater(
        service.addToCart('prod_1', quantity: 5),
        throwsA(isA<CommerceApiException>()
            .having((e) => e.statusCode, 'statusCode', 409)
            .having(
                (e) => e.message, 'message', 'Only 2 left for Blue Vase')),
      );
    });

    test('missing token raises not_authenticated without a request',
        () async {
      var called = false;
      final dio = Dio();
      dio.httpClientAdapter = _FakeAdapter((options) {
        called = true;
        return ResponseBody.fromString('{}', 200);
      });
      final service =
          CommerceService(dio: dio, tokenProvider: () async => null);

      await expectLater(
        service.getCart(),
        throwsA(isA<CommerceApiException>()
            .having((e) => e.statusCode, 'statusCode', 401)),
      );
      expect(called, isFalse);
    });
  });

  group('CommerceService — checkout', () {
    test('checkout posts item ids and quantities only (no client prices)',
        () async {
      late RequestOptions captured;
      final service = _serviceWith((options) {
        captured = options;
        return _ok({
          'id': 'ord_123',
          'customer_id': 'user_1',
          'total_amount': 1400.0,
          'status': 'new',
          'channel': 'craftsy',
          'quantity': 3,
          'items': [
            {
              'id': 'oi_1',
              'product_id': 'prod_1',
              'product_title': 'A',
              'product_image_url': '',
              'quantity': 1,
              'unit_price': 100.0,
              'total_price': 100.0,
            },
            {
              'id': 'oi_2',
              'product_id': 'prod_2',
              'product_title': 'B',
              'product_image_url': '',
              'quantity': 2,
              'unit_price': 650.0,
              'total_price': 1300.0,
            },
          ],
          'payment': {
            'id': 'pay_1',
            'amount': 1400.0,
            'method': 'cod',
            'status': 'pending',
          },
          'shipment': {'id': 'shp_1', 'status': 'pending'},
          'placed_at': '2026-09-25T10:00:00',
        });
      });

      final order = await service.checkout(
        addressId: 'addr_1',
        items: [
          CartItem(
              id: 'i1',
              productId: 'prod_1',
              quantity: 1,
              unitPrice: 1.0,
              title: 'A'),
          CartItem(
              id: 'i2',
              productId: 'prod_2',
              quantity: 2,
              unitPrice: 2.0,
              title: 'B'),
        ],
        paymentMethod: 'cod',
      );

      expect(captured.uri.path, '/api/v1/orders/checkout');
      // Only product ids and quantities cross the wire — never prices
      expect(captured.data['items'], [
        {'product_id': 'prod_1', 'quantity': 1},
        {'product_id': 'prod_2', 'quantity': 2},
      ]);
      expect(captured.data['address_id'], 'addr_1');
      expect(captured.data['payment_method'], 'cod');

      expect(order.id, 'ord_123');
      expect(order.totalAmount, 1400.0);
      expect(order.items.length, 2);
      expect(order.payment!.method, 'cod');
      expect(order.payment!.status, 'pending');
      expect(order.shipment!.status, 'pending');
    });
  });

  group('CommerceService — addresses', () {
    test('createAddress posts full payload and parses response', () async {
      late RequestOptions captured;
      final service = _serviceWith((options) {
        captured = options;
        return ResponseBody.fromString(
          jsonEncode({
            'id': 'addr_9',
            'label': 'home',
            'name': 'Sita Devi',
            'phone': '9876543210',
            'line1': '12 Gram Road',
            'line2': '',
            'city': 'Jaipur',
            'state': 'Rajasthan',
            'pincode': '302001',
            'is_default': true,
          }),
          201,
        );
      });

      final address = await service.createAddress(Address(
        id: '',
        name: 'Sita Devi',
        phone: '9876543210',
        line1: '12 Gram Road',
        city: 'Jaipur',
        state: 'Rajasthan',
        pincode: '302001',
        isDefault: true,
      ));

      expect(captured.method, 'POST');
      expect(captured.data['name'], 'Sita Devi');
      expect(captured.data['pincode'], '302001');
      expect(address.id, 'addr_9');
      expect(address.oneLine, '12 Gram Road, Jaipur, Rajasthan, 302001');
    });
  });

  group('CommerceService — my orders', () {
    test('getMyOrders parses list payload', () async {
      late RequestOptions captured;
      final service = _serviceWith((options) {
        captured = options;
        return _ok({
          'total': 2,
          'orders': [
            {
              'id': 'ord_1',
              'status': 'shipped',
              'total_amount': 500.0,
              'quantity': 1,
              'item_count': 1,
              'first_item_title': 'Vase',
              'first_item_image_url': '/uploads/v.jpg',
              'buyer_location': 'Delhi, Delhi',
              'placed_at': '2026-09-24T10:00:00',
            },
            {
              'id': 'ord_2',
              'status': 'delivered',
              'total_amount': 250.0,
              'quantity': 1,
              'item_count': 1,
              'first_item_title': 'Bowl',
              'first_item_image_url': '',
              'buyer_location': 'Delhi, Delhi',
              'placed_at': '2026-09-20T10:00:00',
            },
          ],
        });
      });

      final orders = await service.getMyOrders();

      expect(captured.uri.path, '/api/v1/orders/my');
      expect(captured.headers['Authorization'],
          'Bearer mock_jwt_token_9876543210');
      expect(orders.length, 2);
      expect(orders[0].status, 'shipped');
      expect(orders[1].status, 'delivered');
      expect(orders[0].firstItemTitle, 'Vase');
    });

    test(
        'getMyOrder parses full detail with payment/shipment/address',
        () async {
      late RequestOptions captured;
      final service = _serviceWith((options) {
        captured = options;
        return _ok({
          'id': 'ord_1',
          'status': 'delivered',
          'total_amount': 500.0,
          'buyer_name': 'Sita',
          'buyer_location': 'Delhi, Delhi',
          'buyer_phone': '9876543210',
          'items': [
            {
              'id': 'oi_1',
              'product_id': 'p1',
              'product_title': 'Vase',
              'product_image_url': '',
              'quantity': 1,
              'unit_price': 500.0,
              'total_price': 500.0,
            }
          ],
          'payment': {
            'id': 'pay_1',
            'amount': 500.0,
            'method': 'cod',
            'status': 'pending',
          },
          'shipment': {
            'id': 'shp_1',
            'status': 'delivered',
            'carrier': null,
            'tracking_id': null,
          },
          'address': {
            'id': 'addr_1',
            'label': 'home',
            'name': 'Sita',
            'phone': '9876543210',
            'line1': '12 Gram Road',
            'line2': '',
            'city': 'Delhi',
            'state': 'Delhi',
            'pincode': '110001',
          },
        });
      });

      final order = await service.getMyOrder('ord_1');

      expect(captured.uri.path, '/api/v1/orders/my/ord_1');
      expect(order.status, 'delivered');
      expect(order.items.length, 1);
      expect(order.payment!.status, 'pending');
      expect(order.shipment!.status, 'delivered');
      expect(order.address!.city, 'Delhi');
    });

    test('other user order (404) raises with server detail', () async {
      final service = _serviceWith((options) => ResponseBody.fromString(
            jsonEncode({'detail': 'Order not found'}),
            404,
          ));

      await expectLater(
        service.getMyOrder('ord_other_user'),
        throwsA(isA<CommerceApiException>()
            .having((e) => e.statusCode, 'statusCode', 404)),
      );
    });
  });
}
