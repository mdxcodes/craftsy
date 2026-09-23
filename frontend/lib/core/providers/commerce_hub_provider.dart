/// Unified Commerce Hub provider.
///
/// Manages state for the unified commerce experience across
/// all channels: Craftsy Marketplace, ONDC, and GeM.

import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/config/api_config.dart';
import '../../core/models/commerce_hub_models.dart';

/// Provider for the commerce hub API service.
final commerceHubApiProvider = Provider<CommerceHubApi>((ref) {
  return CommerceHubApi();
});

/// Commerce hub API client.
class CommerceHubApi {
  final Dio _dio;

  CommerceHubApi({Dio? dio})
      : _dio = dio ??
            Dio(
              BaseOptions(
                baseUrl: ApiConfig.baseUrl,
                connectTimeout: const Duration(seconds: 8),
                receiveTimeout: const Duration(seconds: 15),
                sendTimeout: const Duration(seconds: 15),
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                },
              ),
            );

  /// Get unified commerce summary for artisan dashboard.
  Future<CommerceSummary> getSummary(String artisanId) async {
    final response = await _dio.get('/api/v1/commerce-hub/summary/$artisanId');
    return CommerceSummary.fromJson(response.data);
  }

  /// Get channel statuses for a product.
  Future<List<ChannelStatusInfo>> getProductChannels(String productId) async {
    final response = await _dio.get('/api/v1/commerce-hub/products/$productId/channels');
    return (response.data as List<dynamic>)
        .map((e) => ChannelStatusInfo.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Get product detail with channel information.
  Future<ProductDetailWithChannels> getProductDetail(String productId) async {
    final response = await _dio.get('/api/v1/commerce-hub/products/$productId/detail');
    return ProductDetailWithChannels.fromJson(response.data);
  }

  /// Get unified inventory for a product.
  Future<ProductInventory> getInventory(String productId) async {
    final response = await _dio.get('/api/v1/commerce-hub/products/$productId/inventory');
    return ProductInventory.fromJson(response.data);
  }

  /// Get cross-channel sync status for a product.
  Future<ProductSyncStatus> getSyncStatus(String productId) async {
    final response = await _dio.get('/api/v1/commerce-hub/products/$productId/sync-status');
    return ProductSyncStatus.fromJson(response.data);
  }

  /// Get all orders for an artisan across all channels.
  Future<List<Map<String, dynamic>>> getOrders(
    String artisanId, {
    String? channel,
    String? status,
    int limit = 50,
  }) async {
    final queryParams = <String, dynamic>{};
    if (channel != null) queryParams['channel'] = channel;
    if (status != null) queryParams['status'] = status;
    queryParams['limit'] = limit;

    final response = await _dio.get(
      '/api/v1/commerce-hub/orders/$artisanId',
      queryParameters: queryParams,
    );
    return (response.data as List<dynamic>)
        .map((e) => e as Map<String, dynamic>)
        .toList();
  }

  /// Get order summary grouped by channel.
  Future<List<OrderChannelSummary>> getOrderChannelSummary(String artisanId) async {
    final response = await _dio.get('/api/v1/commerce-hub/orders/$artisanId/channel-summary');
    return (response.data as List<dynamic>)
        .map((e) => OrderChannelSummary.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Enable a channel for a product.
  Future<Map<String, dynamic>> enableChannel(String productId, String channel) async {
    final response = await _dio.post(
      '/api/v1/commerce-hub/products/$productId/channels/$channel/enable',
    );
    return response.data as Map<String, dynamic>;
  }

  /// Disable a channel for a product.
  Future<Map<String, dynamic>> disableChannel(String productId, String channel) async {
    final response = await _dio.post(
      '/api/v1/commerce-hub/products/$productId/channels/$channel/disable',
    );
    return response.data as Map<String, dynamic>;
  }
}

/// Provider for the current artisan's commerce summary.
final commerceSummaryProvider = FutureProvider.family<CommerceSummary, String>((ref, artisanId) async {
  return ref.read(commerceHubApiProvider).getSummary(artisanId);
});

/// Provider for product channels (status per channel).
final productChannelsProvider = FutureProvider.family<List<ChannelStatusInfo>, String>((ref, productId) async {
  return ref.read(commerceHubApiProvider).getProductChannels(productId);
});

/// Provider for product detail with channels.
final productDetailWithChannelsProvider = FutureProvider.family<ProductDetailWithChannels, String>((ref, productId) async {
  return ref.read(commerceHubApiProvider).getProductDetail(productId);
});

/// Provider for product inventory.
final productInventoryProvider = FutureProvider.family<ProductInventory, String>((ref, productId) async {
  return ref.read(commerceHubApiProvider).getInventory(productId);
});

/// Provider for product sync status.
final productSyncStatusProvider = FutureProvider.family<ProductSyncStatus, String>((ref, productId) async {
  return ref.read(commerceHubApiProvider).getSyncStatus(productId);
});

/// Provider for unified orders.
final unifiedOrdersProvider = FutureProvider.family<List<Map<String, dynamic>>, String>((ref, artisanId) async {
  return ref.read(commerceHubApiProvider).getOrders(artisanId);
});

/// Provider for order channel summary.
final orderChannelSummaryProvider = FutureProvider.family<List<OrderChannelSummary>, String>((ref, artisanId) async {
  return ref.read(commerceHubApiProvider).getOrderChannelSummary(artisanId);
});
