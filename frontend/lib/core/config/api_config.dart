import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

/// Centralized API configuration that dynamically resolves the working backend URL.
///
/// Debug / development:
///   - Probes common local addresses and locks onto the first responsive backend.
///
/// Release / production:
///   - Uses the deployed Railway backend by default.
///   - Never probes LAN/localhost addresses.
///   - Rejects private IPs unless an explicit compile-time override is provided.
class ApiConfig {
  static String? _cachedBaseUrl;

  /// Default fallback Wi-Fi IP of the host machine (overridable at build time).
  static const String hostLanIp = String.fromEnvironment(
    'API_HOST_LAN_IP',
    defaultValue: '192.168.1.5',
  );

  static String get baseUrl {
    if (_cachedBaseUrl != null) return _cachedBaseUrl!;
    return _resolveInitialBaseUrl();
  }

  static void setBaseUrl(String url) {
    _cachedBaseUrl = url.endsWith('/') ? url.substring(0, url.length - 1) : url;
    debugPrint('[ApiConfig] Base URL manually set to: $_cachedBaseUrl');
  }

  static String _resolveInitialBaseUrl() {
    const configuredBaseUrl = String.fromEnvironment('API_BASE_URL');
    if (configuredBaseUrl.isNotEmpty) return configuredBaseUrl;

    if (Platform.isAndroid) {
      return 'https://web-production-8ece9b.up.railway.app';
    }
    return 'http://127.0.0.1:8000';
  }

  static bool _isPrivateOrLocalhost(String url) {
    final lower = url.toLowerCase();
    return lower.startsWith('http://192.168.') ||
        lower.startsWith('http://10.') ||
        lower.startsWith('http://127.0.0.1') ||
        lower.startsWith('http://localhost') ||
        lower.startsWith('http://10.0.2.2') ||
        lower.startsWith('http://10.0.3.2');
  }

  static String _productionSafeUrl(String url) {
    if (kReleaseMode && _isPrivateOrLocalhost(url)) {
      debugPrint(
        '[ApiConfig] SECURITY: Release build blocked private/local URL: $url',
      );
      return 'https://web-production-8ece9b.up.railway.app';
    }
    return url;
  }

  /// Quickly tests candidate URLs against `/api/v1/health` and locks onto the first responsive backend.
  static Future<String> discoverWorkingUrl() async {
    const configuredBaseUrl = String.fromEnvironment('API_BASE_URL');
    if (configuredBaseUrl.isNotEmpty) {
      final sanitized = _productionSafeUrl(
        configuredBaseUrl.endsWith('/')
            ? configuredBaseUrl.substring(0, configuredBaseUrl.length - 1)
            : configuredBaseUrl,
      );
      _cachedBaseUrl = sanitized;
      return _cachedBaseUrl!;
    }

    // Production safety: release builds must never probe local addresses.
    if (kReleaseMode) {
      _cachedBaseUrl = _resolveInitialBaseUrl();
      debugPrint(
        '[ApiConfig] Release build — using production base URL: $_cachedBaseUrl',
      );
      return _cachedBaseUrl!;
    }

    final candidates = <String>[
      if (Platform.isAndroid) 'http://127.0.0.1:8000',
      'http://$hostLanIp:8000',
      if (Platform.isAndroid) 'http://10.0.2.2:8000',
      'http://localhost:8000',
    ];

    for (final candidate in candidates) {
      try {
        final dio = Dio(
          BaseOptions(
            connectTimeout: const Duration(milliseconds: 1500),
            receiveTimeout: const Duration(milliseconds: 1500),
          ),
        );
        final response = await dio.get('$candidate/api/v1/health');
        if (response.statusCode == 200) {
          debugPrint('[ApiConfig] Discovered active backend at: $candidate');
          _cachedBaseUrl = candidate;
          return _cachedBaseUrl!;
        }
      } catch (_) {
        // Continue to next candidate
      }
    }

    _cachedBaseUrl = _resolveInitialBaseUrl();
    debugPrint('[ApiConfig] Using default base URL: $_cachedBaseUrl');
    return _cachedBaseUrl!;
  }
}
