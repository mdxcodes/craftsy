/// Centralized Language Service for Craftsy.
///
/// Single abstraction over all voice/language operations:
/// - Speech-to-Text (ASR)
/// - Neural Machine Translation (NMT)
/// - Text-to-Speech (TTS)
/// - Language Detection (ALD)
///
/// Architecture:
///   Widget → LanguageService → Provider → Bhashini / Fallback
///
/// The UI NEVER calls Bhashini APIs directly.
library;

import 'dart:async';
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../config/api_config.dart';

/// Supported language capabilities per language.
class LanguageConfig {
  final String code;
  final String displayName;
  final String nativeName;
  final bool asrSupported;
  final bool nmtSupported;
  final bool ttsSupported;

  const LanguageConfig({
    required this.code,
    required this.displayName,
    required this.nativeName,
    this.asrSupported = false,
    this.nmtSupported = false,
    this.ttsSupported = false,
  });
}

/// Result of a language operation.
enum LanguageResult { success, unavailable, error, fallback }

/// Centralized language service interface.
abstract class LanguageService {
  /// Get all supported languages with their capabilities.
  List<LanguageConfig> getSupportedLanguages();

  /// Get the language config for a specific language code.
  LanguageConfig? getLanguage(String code);

  /// Convert speech (audio bytes) to text.
  /// [audioBytes] is the recorded audio data.
  /// [languageCode] is the expected language (e.g., 'hi', 'en').
  /// Returns the transcribed text or null on failure.
  Future<String?> speechToText(
    List<int> audioBytes, {
    required String languageCode,
  });

  /// Translate [text] from [sourceLanguage] to [targetLanguage].
  /// Returns the translated text or null on failure.
  Future<String?> translate(
    String text, {
    required String sourceLanguage,
    required String targetLanguage,
  });

  /// Convert [text] to speech and play it.
  /// [languageCode] is the target language.
  /// Returns true on success.
  Future<bool> textToSpeech(String text, {required String languageCode});

  /// Detect the language of [text].
  /// Returns the detected language code or null.
  Future<String?> detectLanguage(String text);

  /// Check if a specific capability is available for a language.
  bool isCapabilitySupported(
    String languageCode,
    LanguageCapability capability,
  );

  /// Get the fallback language code for a capability.
  String getFallbackLanguage(LanguageCapability capability);
}

/// Language capabilities.
enum LanguageCapability { asr, nmt, tts, ald }

/// Language provider interface (Bhashini, Fallback, etc.)
abstract class LanguageProvider {
  /// Provider name.
  String get name;

  /// Whether this provider is currently available.
  Future<bool> isAvailable();

  /// ASR: transcribe audio to text.
  Future<String?> transcribe(
    List<int> audioBytes, {
    required String languageCode,
  });

  /// NMT: translate text.
  Future<String?> translateText(
    String text, {
    required String sourceLanguage,
    required String targetLanguage,
  });

  /// TTS: synthesize speech.
  Future<List<int>?> synthesize(String text, {required String languageCode});

  /// ALD: detect language.
  Future<String?> detect(String text);

  /// Get supported language codes.
  List<String> getSupportedLanguages();
}

/// Fallback language provider (no-op, returns null).
class FallbackLanguageProvider implements LanguageProvider {
  @override
  String get name => 'Fallback';

  @override
  Future<bool> isAvailable() async => false;

  @override
  Future<String?> transcribe(
    List<int> audioBytes, {
    required String languageCode,
  }) async => null;

  @override
  Future<String?> translateText(
    String text, {
    required String sourceLanguage,
    required String targetLanguage,
  }) async => null;

  @override
  Future<List<int>?> synthesize(
    String text, {
    required String languageCode,
  }) async => null;

  @override
  Future<String?> detect(String text) async => null;

  @override
  List<String> getSupportedLanguages() => const ['en', 'hi'];
}

/// Bhashini language provider.
///
/// NOTE: This is a scaffold. Live integration requires Bhashini credentials
/// configured in the backend. All methods return null (unavailable) until
/// credentials are provided.
///
/// Architecture: Flutter → Backend proxy → Bhashini API
/// (credentials stay server-side, never in Flutter source)
class BhashiniLanguageProvider implements LanguageProvider {
  @override
  String get name => 'Bhashini';

  // Bhashini language code mapping (ISO-639)
  static const Map<String, String> _bhashiniCodes = {
    'en': 'en',
    'hi': 'hi',
    'bn': 'bn',
    'ta': 'ta',
    'te': 'te',
    'mr': 'mr',
    'gu': 'gu',
    'kn': 'kn',
    'ml': 'ml',
    'pa': 'pa',
    'or': 'or',
    'as': 'as',
  };

  Dio? _dio;

  Future<Dio> _getDio() async {
    _dio ??= Dio(
      BaseOptions(
        baseUrl: ApiConfig.baseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {'Content-Type': 'application/json'},
      ),
    );
    return _dio!;
  }

  @override
  Future<bool> isAvailable() async {
    try {
      final dio = await _getDio();
      final response = await dio.get('/api/v1/bhashini/status');
      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;
        return data['configured'] == true;
      }
    } catch (_) {
      // Backend not reachable or Bhashini not configured.
    }
    return false;
  }

  @override
  Future<String?> transcribe(
    List<int> audioBytes, {
    required String languageCode,
  }) async {
    try {
      final dio = await _getDio();
      final formData = FormData.fromMap({
        'audio': MultipartFile.fromBytes(audioBytes, filename: 'audio.m4a'),
        'language_code': languageCode,
      });
      final response = await dio.post(
        '/api/v1/bhashini/transcribe',
        data: formData,
      );
      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;
        return data['transcript'] as String?;
      }
    } catch (e) {
      debugPrint('[BhashiniLanguageProvider] transcribe error: $e');
    }
    return null;
  }

  @override
  Future<String?> translateText(
    String text, {
    required String sourceLanguage,
    required String targetLanguage,
  }) async {
    try {
      final dio = await _getDio();
      final response = await dio.post(
        '/api/v1/bhashini/translate',
        queryParameters: {
          'text': text,
          'source_language': sourceLanguage,
          'target_language': targetLanguage,
        },
      );
      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;
        return data['translated_text'] as String?;
      }
    } catch (e) {
      debugPrint('[BhashiniLanguageProvider] translate error: $e');
    }
    return null;
  }

  @override
  Future<List<int>?> synthesize(
    String text, {
    required String languageCode,
  }) async {
    try {
      final dio = await _getDio();
      final response = await dio.post(
        '/api/v1/bhashini/synthesize',
        queryParameters: {
          'text': text,
          'language_code': languageCode,
        },
        options: Options(responseType: ResponseType.bytes),
      );
      if (response.statusCode == 200) {
        return response.data as List<int>?;
      }
    } catch (e) {
      debugPrint('[BhashiniLanguageProvider] synthesize error: $e');
    }
    return null;
  }

  @override
  Future<String?> detect(String text) async {
    try {
      final dio = await _getDio();
      final response = await dio.post(
        '/api/v1/bhashini/detect-language',
        queryParameters: {'text': text},
      );
      if (response.statusCode == 200) {
        final data = response.data as Map<String, dynamic>;
        return data['detected_language'] as String?;
      }
    } catch (e) {
      debugPrint('[BhashiniLanguageProvider] detect error: $e');
    }
    return null;
  }

  @override
  List<String> getSupportedLanguages() => _bhashiniCodes.keys.toList();
}

/// Concrete language service implementation with provider chain.
class CraftsyLanguageService implements LanguageService {
  final List<LanguageProvider> _providers;
  final String _defaultLanguage;
  final Map<String, LanguageConfig> _languages;

  CraftsyLanguageService({
    List<LanguageProvider>? providers,
    String defaultLanguage = 'en',
  }) : _providers =
           providers ??
           [BhashiniLanguageProvider(), FallbackLanguageProvider()],
       _defaultLanguage = defaultLanguage,
       _languages = {
         'en': const LanguageConfig(
           code: 'en',
           displayName: 'English',
           nativeName: 'English',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: true,
         ),
         'hi': const LanguageConfig(
           code: 'hi',
           displayName: 'Hindi',
           nativeName: 'हिन्दी',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: true,
         ),
         'bn': const LanguageConfig(
           code: 'bn',
           displayName: 'Bengali',
           nativeName: 'বাংলা',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: false,
         ),
         'ta': const LanguageConfig(
           code: 'ta',
           displayName: 'Tamil',
           nativeName: 'தமிழ்',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: false,
         ),
         'te': const LanguageConfig(
           code: 'te',
           displayName: 'Telugu',
           nativeName: 'తెలుగు',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: false,
         ),
         'mr': const LanguageConfig(
           code: 'mr',
           displayName: 'Marathi',
           nativeName: 'मराठी',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: false,
         ),
         'gu': const LanguageConfig(
           code: 'gu',
           displayName: 'Gujarati',
           nativeName: 'ગુજરાતી',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: false,
         ),
         'kn': const LanguageConfig(
           code: 'kn',
           displayName: 'Kannada',
           nativeName: 'ಕನ್ನಡ',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: false,
         ),
         'ml': const LanguageConfig(
           code: 'ml',
           displayName: 'Malayalam',
           nativeName: 'മലയാളം',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: false,
         ),
         'pa': const LanguageConfig(
           code: 'pa',
           displayName: 'Punjabi',
           nativeName: 'ਪੰਜਾਬੀ',
           asrSupported: true,
           nmtSupported: true,
           ttsSupported: false,
         ),
       };

  @override
  List<LanguageConfig> getSupportedLanguages() => _languages.values.toList();

  @override
  LanguageConfig? getLanguage(String code) => _languages[code];

  @override
  Future<String?> speechToText(
    List<int> audioBytes, {
    required String languageCode,
  }) async {
    for (final provider in _providers) {
      if (await provider.isAvailable()) {
        final result = await provider.transcribe(
          audioBytes,
          languageCode: languageCode,
        );
        if (result != null) return result;
      }
    }
    return null;
  }

  @override
  Future<String?> translate(
    String text, {
    required String sourceLanguage,
    required String targetLanguage,
  }) async {
    for (final provider in _providers) {
      if (await provider.isAvailable()) {
        final result = await provider.translateText(
          text,
          sourceLanguage: sourceLanguage,
          targetLanguage: targetLanguage,
        );
        if (result != null) return result;
      }
    }
    return null;
  }

  @override
  Future<bool> textToSpeech(String text, {required String languageCode}) async {
    for (final provider in _providers) {
      if (await provider.isAvailable()) {
        final result = await provider.synthesize(
          text,
          languageCode: languageCode,
        );
        if (result != null) return true;
      }
    }
    return false;
  }

  @override
  Future<String?> detectLanguage(String text) async {
    for (final provider in _providers) {
      if (await provider.isAvailable()) {
        final result = await provider.detect(text);
        if (result != null) return result;
      }
    }
    return null;
  }

  @override
  bool isCapabilitySupported(
    String languageCode,
    LanguageCapability capability,
  ) {
    final config = _languages[languageCode];
    if (config == null) return false;
    switch (capability) {
      case LanguageCapability.asr:
        return config.asrSupported;
      case LanguageCapability.nmt:
        return config.nmtSupported;
      case LanguageCapability.tts:
        return config.ttsSupported;
      case LanguageCapability.ald:
        return true; // ALD is generally available
    }
  }

  @override
  String getFallbackLanguage(LanguageCapability capability) {
    // TTS fallback is English (flutter_tts supports en-US and hi-IN)
    if (capability == LanguageCapability.tts) return 'en';
    return _defaultLanguage;
  }
}

/// Singleton language service instance.
final LanguageService languageService = CraftsyLanguageService();

/// Voice interaction states for UI.
enum VoiceState {
  idle,
  listening,
  processing,
  understood,
  confirming,
  executing,
  success,
  error,
}

/// Extension for user-friendly labels.
extension VoiceStateX on VoiceState {
  String get labelKey {
    switch (this) {
      case VoiceState.idle:
        return 'voice_state_idle';
      case VoiceState.listening:
        return 'voice_state_listening';
      case VoiceState.processing:
        return 'voice_state_processing';
      case VoiceState.understood:
        return 'voice_state_understood';
      case VoiceState.confirming:
        return 'voice_state_confirming';
      case VoiceState.executing:
        return 'voice_state_executing';
      case VoiceState.success:
        return 'voice_state_success';
      case VoiceState.error:
        return 'voice_state_error';
    }
  }

  IconData get icon {
    switch (this) {
      case VoiceState.idle:
        return Icons.mic_none;
      case VoiceState.listening:
        return Icons.mic;
      case VoiceState.processing:
        return Icons.hourglass_top;
      case VoiceState.understood:
        return Icons.check_circle_outline;
      case VoiceState.confirming:
        return Icons.help_outline;
      case VoiceState.executing:
        return Icons.play_arrow;
      case VoiceState.success:
        return Icons.check_circle;
      case VoiceState.error:
        return Icons.error_outline;
    }
  }

  Color get color {
    switch (this) {
      case VoiceState.idle:
        return Colors.grey;
      case VoiceState.listening:
        return Colors.red;
      case VoiceState.processing:
        return Colors.amber;
      case VoiceState.understood:
        return Colors.blue;
      case VoiceState.confirming:
        return Colors.orange;
      case VoiceState.executing:
        return Colors.blue;
      case VoiceState.success:
        return Colors.green;
      case VoiceState.error:
        return Colors.red;
    }
  }

  bool get isListening => this == VoiceState.listening;
  bool get isProcessing => this == VoiceState.processing;
  bool get isIdle => this == VoiceState.idle;
  bool get hasError => this == VoiceState.error;
}
