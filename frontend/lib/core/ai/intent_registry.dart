import 'package:flutter/foundation.dart';
import 'craftsy_intent.dart';

/// Metadata describing a registered intent type.
@immutable
class IntentMetadata {
  /// Intent type identifier (e.g., 'OPEN_ORDERS').
  final String type;

  /// Default English description.
  final String descriptionEn;

  /// Hindi description.
  final String descriptionHi;

  /// Safety classification.
  final IntentSafety safety;

  /// Whether this intent requires a parameter (e.g., product name).
  final bool requiresParameter;

  const IntentMetadata({
    required this.type,
    required this.descriptionEn,
    required this.descriptionHi,
    this.safety = IntentSafety.safe,
    this.requiresParameter = false,
  });
}

/// Central registry of all supported Craftsy intents.
///
/// This is the single source of truth for what actions the AI can execute.
/// Each intent maps to existing app functionality — no invented capabilities.
class IntentRegistry {
  IntentRegistry._();

  /// All registered intents.
  static final Map<String, IntentMetadata> _intents = {
    // ── Commerce / Channel Intents ─────────────────────────────────────
    'SELL_ON_ONDC': const IntentMetadata(
      type: 'SELL_ON_ONDC',
      descriptionEn: 'Sell a product on ONDC',
      descriptionHi: 'उत्पाद को ONDC पर बेचें',
      safety: IntentSafety.confirmRequired,
    ),
    'CHECK_ONDC_STATUS': const IntentMetadata(
      type: 'CHECK_ONDC_STATUS',
      descriptionEn: 'Check ONDC selling status',
      descriptionHi: 'ONDC बेचने की स्थिति जांचें',
    ),
    'GET_ONDC_HELP': const IntentMetadata(
      type: 'GET_ONDC_HELP',
      descriptionEn: 'Get help with ONDC selling',
      descriptionHi: 'ONDC बेचने में मदद लें',
    ),

    // ── Navigation Intents (SAFE) ──────────────────────────────────────
    'OPEN_HOME': const IntentMetadata(
      type: 'OPEN_HOME',
      descriptionEn: 'Open home screen',
      descriptionHi: 'होम स्क्रीन खोलें',
    ),
    'OPEN_CATALOGUE': const IntentMetadata(
      type: 'OPEN_CATALOGUE',
      descriptionEn: 'Open my catalogue',
      descriptionHi: 'मेरा कैटलॉग खोलें',
    ),
    'OPEN_ORDERS': const IntentMetadata(
      type: 'OPEN_ORDERS',
      descriptionEn: 'Open my orders',
      descriptionHi: 'मेरे ऑर्डर खोलें',
    ),
    'OPEN_EARNINGS': const IntentMetadata(
      type: 'OPEN_EARNINGS',
      descriptionEn: 'Open my earnings',
      descriptionHi: 'मेरी कमाई खोलें',
    ),
    'OPEN_PROFILE': const IntentMetadata(
      type: 'OPEN_PROFILE',
      descriptionEn: 'Open my profile',
      descriptionHi: 'मेरी प्रोफ़ाइल खोलें',
    ),
    'OPEN_NOTIFICATIONS': const IntentMetadata(
      type: 'OPEN_NOTIFICATIONS',
      descriptionEn: 'Open notifications',
      descriptionHi: 'नोटिफिकेशन खोलें',
    ),
    'OPEN_CRAFTMITRA': const IntentMetadata(
      type: 'OPEN_CRAFTMITRA',
      descriptionEn: 'Open CraftMitra assistant',
      descriptionHi: 'क्राफ्ट-मित्र सहायक खोलें',
    ),
    'OPEN_SOCIAL_HELPER': const IntentMetadata(
      type: 'OPEN_SOCIAL_HELPER',
      descriptionEn: 'Open social media helper',
      descriptionHi: 'सोशल मीडिया सहायक खोलें',
    ),
    'OPEN_LANGUAGE_SETTINGS': const IntentMetadata(
      type: 'OPEN_LANGUAGE_SETTINGS',
      descriptionEn: 'Open language settings',
      descriptionHi: 'भाषा सेटिंग्स खोलें',
    ),
    'OPEN_TUTORIAL': const IntentMetadata(
      type: 'OPEN_TUTORIAL',
      descriptionEn: 'Start listing tutorial',
      descriptionHi: 'लिस्टिंग ट्यूटोरियल शुरू करें',
    ),

    // ── Advanced Assistance Intents ────────────────────────────────────
    'OPEN_PACKAGING_HELP': const IntentMetadata(
      type: 'OPEN_PACKAGING_HELP',
      descriptionEn: 'Open packaging help',
      descriptionHi: 'पैकेजिंग मदद खोलें',
    ),
    'OPEN_LABEL_MAKER': const IntentMetadata(
      type: 'OPEN_LABEL_MAKER',
      descriptionEn: 'Open label maker',
      descriptionHi: 'लेबल मेकर खोलें',
    ),

    // ── Product Intents ────────────────────────────────────────────────
    'ADD_PRODUCT': const IntentMetadata(
      type: 'ADD_PRODUCT',
      descriptionEn: 'Add a new product',
      descriptionHi: 'नया उत्पाद जोड़ें',
    ),
    'OPEN_PRODUCT': const IntentMetadata(
      type: 'OPEN_PRODUCT',
      descriptionEn: 'Open a product',
      descriptionHi: 'उत्पाद खोलें',
      requiresParameter: true,
    ),
    'EDIT_PRODUCT': const IntentMetadata(
      type: 'EDIT_PRODUCT',
      descriptionEn: 'Edit a product',
      descriptionHi: 'उत्पाद संपादित करें',
      requiresParameter: true,
    ),
    'DELETE_PRODUCT': const IntentMetadata(
      type: 'DELETE_PRODUCT',
      descriptionEn: 'Delete a product',
      descriptionHi: 'उत्पाद हटाएं',
      safety: IntentSafety.confirmRequired,
      requiresParameter: true,
    ),
    'CHECK_PRODUCT_PRICE': const IntentMetadata(
      type: 'CHECK_PRODUCT_PRICE',
      descriptionEn: 'Check product price',
      descriptionHi: 'उत्पाद की कीमत जांचें',
      requiresParameter: true,
    ),

    // ── Order Intents ──────────────────────────────────────────────────
    'CHECK_ORDER_STATUS': const IntentMetadata(
      type: 'CHECK_ORDER_STATUS',
      descriptionEn: 'Check order status',
      descriptionHi: 'ऑर्डर की स्थिति जांचें',
      requiresParameter: true,
    ),

    // ── Draft Intents ─────────────────────────────────────────────────
    'RESUME_DRAFT': const IntentMetadata(
      type: 'RESUME_DRAFT',
      descriptionEn: 'Resume draft product',
      descriptionHi: 'ड्राफ्ट उत्पाद फिर से शुरू करें',
    ),

    // ── App Intents ───────────────────────────────────────────────────
    'CHANGE_LANGUAGE': const IntentMetadata(
      type: 'CHANGE_LANGUAGE',
      descriptionEn: 'Change app language',
      descriptionHi: 'ऐप की भाषा बदलें',
    ),
    'LOGOUT': const IntentMetadata(
      type: 'LOGOUT',
      descriptionEn: 'Log out',
      descriptionHi: 'लॉग आउट करें',
      safety: IntentSafety.confirmRequired,
    ),

    // ── Sync Intents ──────────────────────────────────────────────────
    'SYNC_PENDING': const IntentMetadata(
      type: 'SYNC_PENDING',
      descriptionEn: 'Sync pending offline products',
      descriptionHi: 'लंबित उत्पाद सिंक करें',
    ),
  };

  /// Get metadata for an intent type.
  static IntentMetadata? get(String type) => _intents[type];

  /// Check if an intent type is supported.
  static bool isSupported(String type) => _intents.containsKey(type);

  /// Get all supported intent types.
  static List<String> get supportedTypes => _intents.keys.toList();

  /// Get all safe intents (no confirmation required).
  static List<IntentMetadata> get safeIntents =>
      _intents.values.where((i) => i.safety == IntentSafety.safe).toList();

  /// Get all intents requiring confirmation.
  static List<IntentMetadata> get confirmRequiredIntents =>
      _intents.values.where((i) => i.safety == IntentSafety.confirmRequired).toList();

  /// Get description in the appropriate language.
  static String getDescription(String type, {bool isHindi = false}) {
    final metadata = _intents[type];
    if (metadata == null) return type;
    return isHindi ? metadata.descriptionHi : metadata.descriptionEn;
  }
}
