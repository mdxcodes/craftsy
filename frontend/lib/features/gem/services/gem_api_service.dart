import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/config/api_config.dart';
import '../../../data/repositories/auth_repository.dart';

class GemApiException implements Exception {
  final int? statusCode;
  final String message;
  GemApiException(this.message, {this.statusCode});
  @override
  String toString() => message;
}

class GemApiService {
  final Dio _dio;
  final Future<String?> Function() _tokenProvider;

  GemApiService({Dio? dio, Future<String?> Function()? tokenProvider})
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

  Future<Map<String, String>> _authHeaders() async {
    final token = await _tokenProvider();
    if (token == null || token.isEmpty) {
      throw GemApiException('not_authenticated', statusCode: 401);
    }
    return {'Authorization': 'Bearer $token'};
  }

  Future<Map<String, dynamic>> getReadiness(String productId) async {
    final response = await _dio.get(
      '/api/v1/gem/products/$productId/readiness',
      options: Options(headers: await _authHeaders()),
    );
    return response.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> generateListingDraft(String productId) async {
    final response = await _dio.post(
      '/api/v1/gem/products/$productId/listing-draft',
      options: Options(headers: await _authHeaders()),
    );
    return response.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> getListingKit(String productId) async {
    final response = await _dio.get(
      '/api/v1/gem/products/$productId/listing-kit',
      options: Options(headers: await _authHeaders()),
    );
    return response.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> getRegistrationOptions() async {
    final response = await _dio.get(
      '/api/v1/gem/registration-options',
      options: Options(headers: await _authHeaders()),
    );
    return response.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> getRegistrationGuidance(String path) async {
    final response = await _dio.get(
      '/api/v1/gem/registration-guidance',
      queryParameters: {'path': path},
      options: Options(headers: await _authHeaders()),
    );
    return response.data as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> openGemPortal(String productId) async {
    final response = await _dio.post(
      '/api/v1/gem/products/$productId/open',
      options: Options(headers: await _authHeaders()),
    );
    return response.data as Map<String, dynamic>;
  }
}

final gemApiServiceProvider = Provider<GemApiService>((ref) {
  return GemApiService();
});
