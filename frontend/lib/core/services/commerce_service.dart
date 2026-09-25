import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config/api_config.dart';
import '../../data/repositories/auth_repository.dart';

/// Exception carrying HTTP status + server detail for honest error display.
class CommerceApiException implements Exception {
  final int? statusCode;
  final String message;

  CommerceApiException(this.message, {this.statusCode});

  @override
  String toString() => message;
}

// ── Models ───────────────────────────────────────────────────────────────────

class CartItem {
  final String id;
  final String productId;
  final int quantity;
  final double unitPrice;
  final String title;
  final String imageUrl;
  final int stock;

  CartItem({
    required this.id,
    required this.productId,
    required this.quantity,
    required this.unitPrice,
    this.title = '',
    this.imageUrl = '',
    this.stock = 0,
  });

  double get lineTotal => unitPrice * quantity;

  factory CartItem.fromJson(Map<String, dynamic> json) {
    return CartItem(
      id: json['id'] ?? '',
      productId: json['product_id'] ?? '',
      quantity: (json['quantity'] ?? 0) as int,
      unitPrice: (json['unit_price'] ?? 0).toDouble(),
      title: json['title'] ?? '',
      imageUrl: json['image_url'] ?? '',
      stock: (json['stock'] ?? 0) as int,
    );
  }
}

class Cart {
  final String id;
  final String userId;
  final List<CartItem> items;
  final double subtotal;

  Cart({
    required this.id,
    required this.userId,
    required this.items,
    this.subtotal = 0,
  });

  int get itemCount =>
      items.fold(0, (sum, item) => sum + item.quantity);

  factory Cart.fromJson(Map<String, dynamic> json) {
    return Cart(
      id: json['id'] ?? '',
      userId: json['user_id'] ?? '',
      items: (json['items'] as List<dynamic>? ?? [])
          .map((e) => CartItem.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      subtotal: (json['subtotal'] ?? 0).toDouble(),
    );
  }
}

class Address {
  final String id;
  final String label;
  final String name;
  final String phone;
  final String line1;
  final String line2;
  final String city;
  final String state;
  final String pincode;
  final bool isDefault;

  Address({
    required this.id,
    this.label = 'home',
    required this.name,
    required this.phone,
    required this.line1,
    this.line2 = '',
    required this.city,
    required this.state,
    required this.pincode,
    this.isDefault = false,
  });

  String get oneLine =>
      [line1, if (line2.isNotEmpty) line2, city, state, pincode]
          .where((part) => part.isNotEmpty)
          .join(', ');

  factory Address.fromJson(Map<String, dynamic> json) {
    return Address(
      id: json['id'] ?? '',
      label: json['label'] ?? 'home',
      name: json['name'] ?? '',
      phone: json['phone'] ?? '',
      line1: json['line1'] ?? '',
      line2: json['line2'] ?? '',
      city: json['city'] ?? '',
      state: json['state'] ?? '',
      pincode: json['pincode'] ?? '',
      isDefault: json['is_default'] ?? false,
    );
  }

  Map<String, dynamic> toCreateJson() => {
        'label': label,
        'name': name,
        'phone': phone,
        'line1': line1,
        'line2': line2,
        'city': city,
        'state': state,
        'pincode': pincode,
        'is_default': isDefault,
      };
}

class PlacedOrderItem {
  final String id;
  final String productId;
  final String title;
  final String imageUrl;
  final int quantity;
  final double unitPrice;
  final double totalPrice;

  PlacedOrderItem({
    required this.id,
    required this.productId,
    required this.title,
    required this.quantity,
    required this.unitPrice,
    required this.totalPrice,
    this.imageUrl = '',
  });

  factory PlacedOrderItem.fromJson(Map<String, dynamic> json) {
    return PlacedOrderItem(
      id: json['id'] ?? '',
      productId: json['product_id'] ?? '',
      title: json['product_title'] ?? '',
      imageUrl: json['product_image_url'] ?? '',
      quantity: (json['quantity'] ?? 0) as int,
      unitPrice: (json['unit_price'] ?? 0).toDouble(),
      totalPrice: (json['total_price'] ?? 0).toDouble(),
    );
  }
}

class PaymentInfo {
  final String id;
  final double amount;
  final String method;
  final String status;

  PaymentInfo({
    required this.id,
    required this.amount,
    required this.method,
    required this.status,
  });

  factory PaymentInfo.fromJson(Map<String, dynamic> json) {
    return PaymentInfo(
      id: json['id'] ?? '',
      amount: (json['amount'] ?? 0).toDouble(),
      method: json['method'] ?? '',
      status: json['status'] ?? '',
    );
  }
}

class ShipmentInfo {
  final String id;
  final String status;
  final String carrier;
  final String trackingId;

  ShipmentInfo({
    required this.id,
    required this.status,
    this.carrier = '',
    this.trackingId = '',
  });

  factory ShipmentInfo.fromJson(Map<String, dynamic> json) {
    return ShipmentInfo(
      id: json['id'] ?? '',
      status: json['status'] ?? '',
      carrier: json['carrier'] ?? '',
      trackingId: json['tracking_id'] ?? '',
    );
  }
}

class PlacedOrder {
  final String id;
  final double totalAmount;
  final String status;
  final List<PlacedOrderItem> items;
  final PaymentInfo? payment;
  final ShipmentInfo? shipment;
  final String? placedAt;

  PlacedOrder({
    required this.id,
    required this.totalAmount,
    required this.status,
    required this.items,
    this.payment,
    this.shipment,
    this.placedAt,
  });

  factory PlacedOrder.fromJson(Map<String, dynamic> json) {
    return PlacedOrder(
      id: json['id'] ?? '',
      totalAmount: (json['total_amount'] ?? 0).toDouble(),
      status: json['status'] ?? '',
      items: (json['items'] as List<dynamic>? ?? [])
          .map((e) => PlacedOrderItem.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      payment: json['payment'] != null
          ? PaymentInfo.fromJson(Map<String, dynamic>.from(json['payment']))
          : null,
      shipment: json['shipment'] != null
          ? ShipmentInfo.fromJson(Map<String, dynamic>.from(json['shipment']))
          : null,
      placedAt: json['placed_at'],
    );
  }
}

class ConsumerOrderSummary {
  final String id;
  final String status;
  final double totalAmount;
  final int quantity;
  final int itemCount;
  final String firstItemTitle;
  final String firstItemImageUrl;
  final String buyerLocation;
  final String? placedAt;
  final String? shippedAt;
  final String? deliveredAt;
  final String? trackingId;

  ConsumerOrderSummary({
    required this.id,
    required this.status,
    required this.totalAmount,
    required this.quantity,
    required this.itemCount,
    required this.firstItemTitle,
    required this.firstItemImageUrl,
    required this.buyerLocation,
    this.placedAt,
    this.shippedAt,
    this.deliveredAt,
    this.trackingId,
  });

  factory ConsumerOrderSummary.fromJson(Map<String, dynamic> json) {
    return ConsumerOrderSummary(
      id: json['id'] ?? '',
      status: json['status'] ?? '',
      totalAmount: (json['total_amount'] ?? 0).toDouble(),
      quantity: (json['quantity'] ?? 0) as int,
      itemCount: (json['item_count'] ?? 0) as int,
      firstItemTitle: json['first_item_title'] ?? '',
      firstItemImageUrl: json['first_item_image_url'] ?? '',
      buyerLocation: json['buyer_location'] ?? '',
      placedAt: json['placed_at'],
      shippedAt: json['shipped_at'],
      deliveredAt: json['delivered_at'],
      trackingId: json['tracking_id'],
    );
  }
}

class ConsumerOrderDetail {
  final String id;
  final String status;
  final double totalAmount;
  final String buyerName;
  final String buyerLocation;
  final String buyerPhone;
  final String? placedAt;
  final String? shippedAt;
  final String? deliveredAt;
  final String? trackingId;
  final List<PlacedOrderItem> items;
  final PaymentInfo? payment;
  final ShipmentInfo? shipment;
  final Address? address;

  ConsumerOrderDetail({
    required this.id,
    required this.status,
    required this.totalAmount,
    required this.buyerName,
    required this.buyerLocation,
    required this.buyerPhone,
    required this.items,
    this.placedAt,
    this.shippedAt,
    this.deliveredAt,
    this.trackingId,
    this.payment,
    this.shipment,
    this.address,
  });

  factory ConsumerOrderDetail.fromJson(Map<String, dynamic> json) {
    return ConsumerOrderDetail(
      id: json['id'] ?? '',
      status: json['status'] ?? '',
      totalAmount: (json['total_amount'] ?? 0).toDouble(),
      buyerName: json['buyer_name'] ?? '',
      buyerLocation: json['buyer_location'] ?? '',
      buyerPhone: json['buyer_phone'] ?? '',
      placedAt: json['placed_at'],
      shippedAt: json['shipped_at'],
      deliveredAt: json['delivered_at'],
      trackingId: json['tracking_id'],
      items: (json['items'] as List<dynamic>? ?? [])
          .map((e) => PlacedOrderItem.fromJson(Map<String, dynamic>.from(e)))
          .toList(),
      payment: json['payment'] != null
          ? PaymentInfo.fromJson(Map<String, dynamic>.from(json['payment']))
          : null,
      shipment: json['shipment'] != null
          ? ShipmentInfo.fromJson(Map<String, dynamic>.from(json['shipment']))
          : null,
      address: json['address'] != null
          ? Address.fromJson(Map<String, dynamic>.from(json['address']))
          : null,
    );
  }
}

// ── Service ──────────────────────────────────────────────────────────────────

/// Authenticated commerce API client — cart, addresses, checkout, my orders.
///
/// All requests attach the Bearer token from AuthRepository. Server data is
/// authoritative; client totals are display-only.
class CommerceService {
  final Dio _dio;
  final Future<String?> Function() _tokenProvider;

  CommerceService({Dio? dio, Future<String?> Function()? tokenProvider})
      : _dio = dio ??
            Dio(BaseOptions(
              baseUrl: ApiConfig.baseUrl,
              connectTimeout: const Duration(seconds: 8),
              receiveTimeout: const Duration(seconds: 15),
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
              },
            )),
        _tokenProvider = tokenProvider ?? AuthRepository().getAccessToken;

  void _syncBaseUrl() {
    _dio.options.baseUrl = ApiConfig.baseUrl;
  }

  Future<Map<String, String>> _authHeaders() async {
    final token = await _tokenProvider();
    if (token == null || token.isEmpty) {
      throw CommerceApiException('not_authenticated', statusCode: 401);
    }
    return {'Authorization': 'Bearer $token'};
  }

  dynamic _unwrap(Response response) => _decode(response.data);

  dynamic _decode(dynamic data) {
    if (data is String && data.isNotEmpty) {
      try {
        return jsonDecode(data);
      } catch (_) {
        return data;
      }
    }
    return data;
  }

  Never _throwFromDio(DioException e) {
    final detail = _decode(e.response?.data);
    String message = e.message ?? 'network_error';
    if (detail is Map && detail['detail'] != null) {
      message = detail['detail'].toString();
    }
    throw CommerceApiException(message, statusCode: e.response?.statusCode);
  }

  // ── Cart ───────────────────────────────────────────────────────────────────

  Future<Cart> getCart() async {
    _syncBaseUrl();
    try {
      final response = await _dio.get('/api/v1/cart',
          options: Options(headers: await _authHeaders()));
      return Cart.fromJson(Map<String, dynamic>.from(_unwrap(response)));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  Future<Cart> addToCart(String productId, {int quantity = 1}) async {
    _syncBaseUrl();
    try {
      final response = await _dio.post('/api/v1/cart/items',
          options: Options(headers: await _authHeaders()),
          data: {'product_id': productId, 'quantity': quantity});
      return Cart.fromJson(Map<String, dynamic>.from(_unwrap(response)));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  Future<Cart> updateCartItem(String itemId, int quantity) async {
    _syncBaseUrl();
    try {
      final response = await _dio.put('/api/v1/cart/items/$itemId',
          options: Options(headers: await _authHeaders()), data: {'quantity': quantity});
      return Cart.fromJson(Map<String, dynamic>.from(_unwrap(response)));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  Future<Cart> removeCartItem(String itemId) async {
    _syncBaseUrl();
    try {
      final response = await _dio.delete('/api/v1/cart/items/$itemId',
          options: Options(headers: await _authHeaders()));
      return Cart.fromJson(Map<String, dynamic>.from(_unwrap(response)));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  Future<void> clearCart() async {
    _syncBaseUrl();
    try {
      await _dio.delete('/api/v1/cart',
          options: Options(headers: await _authHeaders()));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  // ── Addresses ──────────────────────────────────────────────────────────────

  Future<List<Address>> getAddresses() async {
    _syncBaseUrl();
    try {
      final response = await _dio.get('/api/v1/addresses',
          options: Options(headers: await _authHeaders()));
      return (response.data as List<dynamic>)
          .map((e) => Address.fromJson(Map<String, dynamic>.from(e)))
          .toList();
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  Future<Address> createAddress(Address address) async {
    _syncBaseUrl();
    try {
      final response = await _dio.post('/api/v1/addresses',
          options: Options(headers: await _authHeaders()), data: address.toCreateJson());
      return Address.fromJson(Map<String, dynamic>.from(_unwrap(response)));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  Future<Address> updateAddress(String addressId, Map<String, dynamic> updates) async {
    _syncBaseUrl();
    try {
      final response = await _dio.put('/api/v1/addresses/$addressId',
          options: Options(headers: await _authHeaders()), data: updates);
      return Address.fromJson(Map<String, dynamic>.from(_unwrap(response)));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  Future<void> deleteAddress(String addressId) async {
    _syncBaseUrl();
    try {
      await _dio.delete('/api/v1/addresses/$addressId',
          options: Options(headers: await _authHeaders()));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  // ── Checkout & orders ──────────────────────────────────────────────────────

  Future<PlacedOrder> checkout({
    required String addressId,
    required List<CartItem> items,
    String paymentMethod = 'cod',
  }) async {
    _syncBaseUrl();
    try {
      final response = await _dio.post('/api/v1/orders/checkout',
          options: Options(headers: await _authHeaders()),
          data: {
            'items': items
                .map((i) => {'product_id': i.productId, 'quantity': i.quantity})
                .toList(),
            'address_id': addressId,
            'payment_method': paymentMethod,
          });
      return PlacedOrder.fromJson(Map<String, dynamic>.from(_unwrap(response)));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  Future<List<ConsumerOrderSummary>> getMyOrders(
      {int limit = 50, int offset = 0}) async {
    _syncBaseUrl();
    try {
      final response = await _dio.get('/api/v1/orders/my',
          options: Options(headers: await _authHeaders()),
          queryParameters: {'limit': limit, 'offset': offset});
      final data = Map<String, dynamic>.from(_unwrap(response));
      return (data['orders'] as List<dynamic>? ?? [])
          .map((e) => ConsumerOrderSummary.fromJson(Map<String, dynamic>.from(e)))
          .toList();
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }

  Future<ConsumerOrderDetail> getMyOrder(String orderId) async {
    _syncBaseUrl();
    try {
      final response = await _dio.get('/api/v1/orders/my/$orderId',
          options: Options(headers: await _authHeaders()));
      return ConsumerOrderDetail.fromJson(
          Map<String, dynamic>.from(_unwrap(response)));
    } on DioException catch (e) {
      _throwFromDio(e);
    }
  }
}

/// Application-wide commerce service singleton.
final commerceService = CommerceService();

/// Riverpod provider exposing the commerce service (overridable in tests).
final commerceServiceProvider =
    Provider<CommerceService>((ref) => commerceService);
