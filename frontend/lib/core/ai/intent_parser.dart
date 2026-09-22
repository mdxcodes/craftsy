import 'craftsy_intent.dart';
import 'intent_registry.dart';

/// Parses user text (from chat or voice transcription) into a [CraftsyIntent].
///
/// This is the bridge between the chat/voice layer and the action executor.
/// It uses keyword matching and parameter extraction to identify the user's
/// intent from natural language input.
class IntentParser {
  IntentParser._();

  /// Parse user text into a CraftsyIntent.
  ///
  /// Returns null if no intent could be identified.
  static CraftsyIntent? parse(String text, {String languageCode = 'en'}) {
    final clean = text.trim().toLowerCase();
    if (clean.isEmpty) return null;

    final isHindi = _isHindiText(clean) || languageCode == 'hi';

    // ── Navigation Intents ────────────────────────────────────────────
    if (_matchesAny(clean, ['home', 'होम', 'ghar', 'घर'])) {
      return _intent('OPEN_HOME', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['catalogue', 'कैटलॉग', 'catalog', 'सामान', 'saman', 'items', 'inventory', 'stock', 'dukaan', 'दुकान'])) {
      return _intent('OPEN_CATALOGUE', isHindi: isHindi);
    }

    // ── Order Intents ─────────────────────────────────────────────────
    // Check for specific order status check before general order navigation
    if (_matchesAny(clean, ['order status', 'ऑर्डर स्थिति', 'order check', 'track order', 'tracking']) ||
        _extractOrderId(clean) != null) {
      final orderId = _extractOrderId(clean);
      return _intent('CHECK_ORDER_STATUS', parameters: orderId != null ? {'order_id': orderId} : {}, isHindi: isHindi);
    }

    if (_matchesAny(clean, ['order', 'ऑर्डर', 'orders'])) {
      return _intent('OPEN_ORDERS', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['earning', 'कमाई', 'kamai', 'revenue', 'sales', 'bikri', 'बिक्री', 'income', 'stats', 'statistics', 'आंकड़े'])) {
      return _intent('OPEN_EARNINGS', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['profile', 'प्रोफ़ाइल', 'account', 'mera profile', 'details', 'pehchan', 'cluster'])) {
      return _intent('OPEN_PROFILE', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['notification', 'नोटिफिकेशन', 'notifications', 'alert', 'alerts'])) {
      return _intent('OPEN_NOTIFICATIONS', isHindi: isHindi);
    }

    // ── Advanced Assistance Intents (check before CraftMitra) ──────────
    if (_matchesAny(clean, ['packaging', 'packing', 'पैकेजिंग', 'package', 'pack', 'पैक', 'kaise pack', 'कैसे पैक'])) {
      return _intent('OPEN_PACKAGING_HELP', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['label', 'लेबल', 'sticker', 'sticker', 'label maker', 'label banao', 'लेबल बनाओ', 'label banana'])) {
      return _intent('OPEN_LABEL_MAKER', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['social', 'सोशल', 'share', 'sharing', 'promote', 'promotion'])) {
      return _intent('OPEN_SOCIAL_HELPER', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['language', 'भाषा', 'bhasha', 'hindi', 'tamil', 'bengali', 'english', 'change language'])) {
      return _intent('OPEN_LANGUAGE_SETTINGS', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['tutorial', 'ट्यूटोरियल', 'guide', 'how to', 'कैसे', 'kaise', 'learn', 'सीखें'])) {
      return _intent('OPEN_TUTORIAL', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['craftmitra', 'क्राफ्ट-मित्र', 'assistant', 'सहायक', 'help', 'मदद', 'madad'])) {
      return _intent('OPEN_CRAFTMITRA', isHindi: isHindi);
    }

    // ── Product Intents ───────────────────────────────────────────────
    if (_matchesAny(clean, ['add product', 'add a product', 'add new product', 'naya saman', 'नया सामान', 'upload', 'bechna', 'बेचना', 'list', 'jodna', 'जोड़ना', 'create product', 'photo', 'फोटो']) ||
        (clean.contains('add') && (clean.contains('product') || clean.contains('item') || clean.contains('craft') || clean.contains('saman')))) {
      return _intent('ADD_PRODUCT', isHindi: isHindi);
    }

    // Open specific product: "open X", "show X", "dikhao X", "दिखाओ X"
    final openProductMatch = _extractProductName(clean, ['open', 'show', 'dikhao', 'दिखाओ', 'kholo', 'खोलो']);
    if (openProductMatch != null) {
      return _intent('OPEN_PRODUCT', parameters: {'product_name': openProductMatch}, isHindi: isHindi);
    }

    // Edit product: "edit X", "change X", "modify X"
    final editProductMatch = _extractProductName(clean, ['edit', 'change', 'modify', 'संपादित', 'बदलें']);
    if (editProductMatch != null) {
      return _intent('EDIT_PRODUCT', parameters: {'product_name': editProductMatch}, isHindi: isHindi);
    }

    // Delete product: "delete X", "remove X", "hatao X", "हटाओ X"
    final deleteProductMatch = _extractProductName(clean, ['delete', 'remove', 'hatao', 'हटाओ', 'hata', 'हटा']);
    if (deleteProductMatch != null) {
      return _intent('DELETE_PRODUCT', parameters: {'product_name': deleteProductMatch}, isHindi: isHindi);
    }

    // Check price: "price of X", "cost of X", "kimat X", "कीमत X"
    final priceMatch = _extractProductName(clean, ['price of', 'cost of', 'kimat', 'कीमत', 'keemat', 'rate of']);
    if (priceMatch != null) {
      return _intent('CHECK_PRODUCT_PRICE', parameters: {'product_name': priceMatch}, isHindi: isHindi);
    }

    // ── Order Intents ─────────────────────────────────────────────────
    if (_matchesAny(clean, ['order status', 'ऑर्डर स्थिति', 'order check', 'track order', 'tracking'])) {
      final orderId = _extractOrderId(clean);
      return _intent('CHECK_ORDER_STATUS', parameters: orderId != null ? {'order_id': orderId} : {}, isHindi: isHindi);
    }

    // ── Draft Intents ─────────────────────────────────────────────────
    if (_matchesAny(clean, ['resume draft', 'continue draft', 'draft', 'ड्राफ्ट', 'adhaura', 'अधूरा'])) {
      return _intent('RESUME_DRAFT', isHindi: isHindi);
    }

    // ── App Intents ───────────────────────────────────────────────────
    if (_matchesAny(clean, ['change language', 'भाषा बदलें', 'language change', 'switch language'])) {
      return _intent('CHANGE_LANGUAGE', isHindi: isHindi);
    }

    if (_matchesAny(clean, ['logout', 'log out', 'लॉग आउट', 'sign out', 'बाहर निकलें'])) {
      return _intent('LOGOUT', isHindi: isHindi);
    }

    // ── Sync Intents ──────────────────────────────────────────────────
    if (_matchesAny(clean, ['sync', 'सिंक', 'sync pending', 'sync offline', 'sync now', 'sync products', 'upload offline', 'upload pending', 'pending sync', 'offline sync', 'sync karo'])) {
      return _intent('SYNC_PENDING', isHindi: isHindi);
    }

    // No intent matched
    return null;
  }

  // ── Helper Methods ──────────────────────────────────────────────────

  static CraftsyIntent _intent(String type, {Map<String, dynamic> parameters = const {}, bool isHindi = false}) {
    final metadata = IntentRegistry.get(type);
    return CraftsyIntent(
      type: type,
      description: metadata != null
          ? (isHindi ? metadata.descriptionHi : metadata.descriptionEn)
          : type,
      parameters: parameters,
      safety: metadata?.safety ?? IntentSafety.safe,
    );
  }

  static bool _matchesAny(String text, List<String> keywords) {
    return keywords.any((kw) => text.contains(kw.toLowerCase()));
  }

  static bool _isHindiText(String text) {
    return RegExp(r'[\u0900-\u097F]').hasMatch(text);
  }

  /// Extract a product name from text after a trigger word.
  static String? _extractProductName(String text, List<String> triggers) {
    for (final trigger in triggers) {
      final idx = text.indexOf(trigger);
      if (idx != -1) {
        final after = text.substring(idx + trigger.length).trim();
        // Remove common filler words
        final cleaned = after
            .replaceAll(RegExp(r'^(my|the|this|mera|meri|ye|apna|apni|ka|ki)\s+', caseSensitive: false), '')
            .replaceAll(RegExp(r'\s+(please|plz|bhai|yaar)\s*$', caseSensitive: false), '')
            .trim();
        if (cleaned.isNotEmpty && cleaned.length > 1) {
          return cleaned;
        }
      }
    }
    return null;
  }

  /// Extract an order ID from text.
  static String? _extractOrderId(String text) {
    // Match patterns like "ORD-1001", "order 1001", "#1001"
    final match = RegExp(r'(ORD[- ]?(\d+)|order\s+(\d+)|#(\d+))', caseSensitive: false).firstMatch(text);
    if (match != null) {
      final number = match.group(2) ?? match.group(3) ?? match.group(4);
      if (number != null) {
        return 'ORD-$number';
      }
    }
    return null;
  }
}
