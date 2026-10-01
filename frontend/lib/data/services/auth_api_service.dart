import 'dart:async';
import 'package:dio/dio.dart';
import '../../core/config/api_config.dart';

class AuthException implements Exception {
  final String message;
  final int? statusCode;
  final String? errorCode;

  const AuthException({
    required this.message,
    this.statusCode,
    this.errorCode,
  });

  @override
  String toString() => 'AuthException: $message';
}

class AuthResponse {
  final String accessToken;
  final String tokenType;
  final ArtisanProfile artisan;

  const AuthResponse({
    required this.accessToken,
    required this.tokenType,
    required this.artisan,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      accessToken: json['access_token']?.toString() ?? json['accessToken']?.toString() ?? '',
      tokenType: json['token_type']?.toString() ?? json['tokenType']?.toString() ?? 'bearer',
      artisan: ArtisanProfile.fromJson(json['artisan'] as Map<String, dynamic>? ?? json),
    );
  }
}

class ArtisanProfile {
  final String id;
  final String? name;
  final String phone;
  final String? craftType;
  final String? locationCluster;
  final String? state;
  final String preferredLanguage;
  final String role;

  const ArtisanProfile({
    required this.id,
    this.name,
    required this.phone,
    this.craftType,
    this.locationCluster,
    this.state,
    required this.preferredLanguage,
    required this.role,
  });

  factory ArtisanProfile.fromJson(Map<String, dynamic> json) {
    return ArtisanProfile(
      id: json['id']?.toString() ?? '',
      name: json['name'] as String?,
      phone: json['phone']?.toString() ?? '',
      craftType: json['craft_type'] as String?,
      locationCluster: json['location_cluster'] as String?,
      state: json['state'] as String?,
      preferredLanguage: json['preferred_language']?.toString() ?? 'en',
      role: json['role']?.toString() ?? 'customer',
    );
  }
}

class LoginResponse {
  final String status;
  final String message;
  final String phone;
  final String requestId;
  final bool otpSent;
  final bool isNewUser;

  const LoginResponse({
    required this.status,
    required this.message,
    required this.phone,
    required this.requestId,
    required this.otpSent,
    required this.isNewUser,
  });

  factory LoginResponse.fromJson(Map<String, dynamic> json) {
    return LoginResponse(
      status: json['status']?.toString() ?? 'success',
      message: json['message']?.toString() ?? 'OTP sent successfully.',
      phone: json['phone']?.toString() ?? '',
      requestId: json['request_id']?.toString() ?? json['requestId']?.toString() ?? '',
      otpSent: json['otp_sent'] as bool? ?? true,
      isNewUser: json['is_new_user'] as bool? ?? false,
    );
  }
}

abstract class AuthApiService {
  Future<LoginResponse> sendOtp(String phone);
  Future<AuthResponse> verifyOtp({
    required String phone,
    required String requestId,
    required String otp,
  });
  Future<LoginResponse> resendOtp(String phone);
}

class HttpAuthApiService implements AuthApiService {
  final Dio _dio;

  HttpAuthApiService({Dio? dio})
    : _dio =
          dio ??
          Dio(
            BaseOptions(
              connectTimeout: const Duration(seconds: 15),
              receiveTimeout: const Duration(seconds: 15),
              sendTimeout: const Duration(seconds: 15),
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
              },
            ),
          );

  Future<String> _resolveBaseUrl() async {
    return ApiConfig.baseUrl;
  }

  @override
  Future<LoginResponse> sendOtp(String phone) async {
    final baseUrl = await _resolveBaseUrl();
    _dio.options.baseUrl = baseUrl;

    try {
      final response = await _dio.post(
        '/api/v1/auth/login',
        data: {'phone': phone},
      );

      if (response.statusCode == 200 && response.data != null) {
        return LoginResponse.fromJson(response.data as Map<String, dynamic>);
      }

      throw AuthException(
        message: 'Unexpected response from server.',
        statusCode: response.statusCode,
      );
    } on DioException catch (e) {
      final statusCode = e.response?.statusCode;
      String? errorCode;
      String message = 'Network error. Please try again.';

      if (e.response?.data != null) {
        final data = e.response!.data as Map<String, dynamic>?;
        if (data != null) {
          errorCode = data['error_code']?.toString() ?? data['code']?.toString();
          message = data['message']?.toString() ?? data['msg']?.toString() ?? message;

          if (data['detail'] is Map) {
            final detail = data['detail'] as Map<String, dynamic>;
            errorCode = detail['error_code']?.toString() ?? errorCode;
            message = detail['message']?.toString() ?? message;
          }
        }
      }

      if (statusCode == 429) {
        message = 'Too many requests. Please wait before resending OTP.';
      }

      throw AuthException(
        message: message,
        statusCode: statusCode,
        errorCode: errorCode,
      );
    } catch (e) {
      throw AuthException(message: 'Failed to send OTP: $e');
    }
  }

  @override
  Future<AuthResponse> verifyOtp({
    required String phone,
    required String requestId,
    required String otp,
  }) async {
    final baseUrl = await _resolveBaseUrl();
    _dio.options.baseUrl = baseUrl;

    try {
      final response = await _dio.post(
        '/api/v1/auth/verify-otp',
        data: {
          'phone': phone,
          'request_id': requestId,
          'otp': otp,
        },
      );

      if (response.statusCode == 200 && response.data != null) {
        return AuthResponse.fromJson(response.data as Map<String, dynamic>);
      }

      throw AuthException(
        message: 'Unexpected response from server.',
        statusCode: response.statusCode,
      );
    } on DioException catch (e) {
      final statusCode = e.response?.statusCode;
      String message = 'Network error. Please try again.';
      String? errorCode;

      if (e.response?.data != null) {
        final data = e.response!.data as Map<String, dynamic>?;
        if (data != null) {
          errorCode = data['error_code']?.toString() ?? data['code']?.toString();
          message = data['detail'] is String
              ? data['detail'] as String
              : data['message']?.toString() ?? data['msg']?.toString() ?? message;
        }
      }

      throw AuthException(
        message: message,
        statusCode: statusCode,
        errorCode: errorCode,
      );
    } catch (e) {
      throw AuthException(message: 'Failed to verify OTP: $e');
    }
  }

  @override
  Future<LoginResponse> resendOtp(String phone) async {
    final baseUrl = await _resolveBaseUrl();
    _dio.options.baseUrl = baseUrl;

    try {
      final response = await _dio.post(
        '/api/v1/auth/resend-otp',
        data: {'phone': phone},
      );

      if (response.statusCode == 200 && response.data != null) {
        return LoginResponse.fromJson(response.data as Map<String, dynamic>);
      }

      throw AuthException(
        message: 'Unexpected response from server.',
        statusCode: response.statusCode,
      );
    } on DioException catch (e) {
      final statusCode = e.response?.statusCode;
      String message = 'Network error. Please try again.';
      String? errorCode;

      if (e.response?.data != null) {
        final data = e.response!.data as Map<String, dynamic>?;
        if (data != null) {
          errorCode = data['error_code']?.toString() ?? data['code']?.toString();
          message = data['message']?.toString() ?? data['msg']?.toString() ?? message;
        }
      }

      if (statusCode == 429) {
        message = 'Too many requests. Please wait before resending OTP.';
      }

      throw AuthException(
        message: message,
        statusCode: statusCode,
        errorCode: errorCode,
      );
    } catch (e) {
      throw AuthException(message: 'Failed to resend OTP: $e');
    }
  }
}
