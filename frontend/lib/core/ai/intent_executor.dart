import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:easy_localization/easy_localization.dart';
import '../providers/app_providers.dart';
import '../../features/home/screens/home_shell.dart';
import '../../features/catalogue/providers/catalogue_filter_provider.dart';
import '../../features/orders/providers/orders_provider.dart';
import '../../features/auth/providers/auth_provider.dart';
import '../../data/models/product.dart';
import 'craftsy_intent.dart';
import 'intent_registry.dart';

/// Result of executing a CraftsyIntent.
class IntentResult {
  /// Whether execution succeeded.
  final bool success;

  /// Localized message describing the outcome.
  final String message;

  /// Whether the action was executed (vs. just confirmed).
  final bool executed;

  const IntentResult({
    required this.success,
    required this.message,
    this.executed = true,
  });

  factory IntentResult.success(String message) =>
      IntentResult(success: true, message: message);

  factory IntentResult.failure(String message) =>
      IntentResult(success: false, message: message);

  factory IntentResult.cancelled() =>
      const IntentResult(success: false, message: 'cancelled', executed: false);
}

/// Centralized executor for all Craftsy intents.
///
/// This is the single dispatch point for AI actions — voice, chat,
/// buttons, and tutorials all use the same executor.
class IntentExecutor {
  final Ref _ref;
  final BuildContext _context;

  IntentExecutor(this._ref, this._context);

  /// Execute an intent and return the result.
  Future<IntentResult> execute(CraftsyIntent intent) async {
    debugPrint('[IntentExecutor] Executing: ${intent.type}');

    // Check if intent is supported
    if (!IntentRegistry.isSupported(intent.type)) {
      return IntentResult.failure(
        _isHindi()
            ? 'यह काम अभी Craftsy में उपलब्ध नहीं है।'
            : 'This action is not available in Craftsy yet.',
      );
    }

    // Check if intent requires confirmation
    if (intent.isDestructive) {
      final confirmed = await _requestConfirmation(intent);
      if (!confirmed) {
        return IntentResult.cancelled();
      }
    }

    // Execute based on intent type
    switch (intent.type) {
      // ── Navigation ──────────────────────────────────────────────────
      case 'OPEN_HOME':
        return _executeOpenHome();
      case 'OPEN_CATALOGUE':
        return _executeOpenCatalogue();
      case 'OPEN_ORDERS':
        return _executeOpenOrders();
      case 'OPEN_EARNINGS':
        return _executeOpenEarnings();
      case 'OPEN_PROFILE':
        return _executeOpenProfile();
      case 'OPEN_NOTIFICATIONS':
        return _executeOpenNotifications();
      case 'OPEN_CRAFTMITRA':
        return _executeOpenCraftMitra();
      case 'OPEN_SOCIAL_HELPER':
        return _executeOpenSocialHelper();
      case 'OPEN_LANGUAGE_SETTINGS':
        return _executeOpenLanguageSettings();
      case 'OPEN_TUTORIAL':
        return _executeOpenTutorial();

      // ── Product Actions ─────────────────────────────────────────────
      case 'ADD_PRODUCT':
        return _executeAddProduct();
      case 'OPEN_PRODUCT':
        return _executeOpenProduct(intent);
      case 'EDIT_PRODUCT':
        return _executeEditProduct(intent);
      case 'DELETE_PRODUCT':
        return await _executeDeleteProduct(intent);
      case 'CHECK_PRODUCT_PRICE':
        return _executeCheckProductPrice(intent);

      // ── Order Actions ───────────────────────────────────────────────
      case 'CHECK_ORDER_STATUS':
        return _executeCheckOrderStatus(intent);

      // ── Draft Actions ───────────────────────────────────────────────
      case 'RESUME_DRAFT':
        return _executeResumeDraft();

      // ── App Actions ─────────────────────────────────────────────────
      case 'CHANGE_LANGUAGE':
        return _executeChangeLanguage();
      case 'LOGOUT':
        return _executeLogout();

      // ── Sync Actions ────────────────────────────────────────────────
      case 'SYNC_PENDING':
        return _executeSyncPending();

      default:
        return IntentResult.failure(
          _isHindi()
              ? 'यह काम अभी Craftsy में उपलब्ध नहीं है।'
              : 'This action is not available in Craftsy yet.',
        );
    }
  }

  // ── Navigation Executors ────────────────────────────────────────────

  IntentResult _executeOpenHome() {
    _ref.read(homeTabIndexProvider.notifier).state = 0;
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'होम स्क्रीन खोल रहा हूँ।' : 'Opening home screen.');
  }

  IntentResult _executeOpenCatalogue() {
    _context.push('/catalogue');
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'आपका कैटलॉग खोल रहा हूँ।' : 'Opening your catalogue.');
  }

  IntentResult _executeOpenOrders() {
    _ref.read(homeTabIndexProvider.notifier).state = 1;
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'आपके ऑर्डर खोल रहा हूँ।' : 'Opening your orders.');
  }

  IntentResult _executeOpenEarnings() {
    _ref.read(homeTabIndexProvider.notifier).state = 3;
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'आपकी कमाई खोल रहा हूँ।' : 'Opening your earnings.');
  }

  IntentResult _executeOpenProfile() {
    _ref.read(homeTabIndexProvider.notifier).state = 4;
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'आपकी प्रोफ़ाइल खोल रहा हूँ।' : 'Opening your profile.');
  }

  IntentResult _executeOpenNotifications() {
    _context.push('/notifications');
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'नोटिफिकेशन खोल रहा हूँ।' : 'Opening notifications.');
  }

  IntentResult _executeOpenCraftMitra() {
    // Already in chatbot — just acknowledge
    return IntentResult.success(_isHindi() ? 'मैं यहाँ हूँ, बात करें।' : 'I am here, let\'s talk.');
  }

  IntentResult _executeOpenSocialHelper() {
    _context.push('/social-media-helper');
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'सोशल मीडिया सहायक खोल रहा हूँ।' : 'Opening social media helper.');
  }

  IntentResult _executeOpenLanguageSettings() {
    _context.push('/language-settings');
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'भाषा सेटिंग्स खोल रहा हूँ।' : 'Opening language settings.');
  }

  IntentResult _executeOpenTutorial() {
    _context.push('/listing-tutorial');
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'ट्यूटोरियल शुरू कर रहा हूँ।' : 'Starting tutorial.');
  }

  // ── Product Executors ───────────────────────────────────────────────

  IntentResult _executeAddProduct() {
    _ref.read(homeTabIndexProvider.notifier).state = 2;
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'नया सामान जोड़ते हैं।' : 'Let\'s add a new product.');
  }

  IntentResult _executeOpenProduct(CraftsyIntent intent) {
    final productName = intent.parameters['product_name'] as String?;
    if (productName == null || productName.isEmpty) {
      return IntentResult.failure(_isHindi() ? 'उत्पाद का नाम बताएं।' : 'Please specify a product name.');
    }

    // Find product in catalogue
    final products = _ref.read(productListProvider).value ?? [];
    Product? matched;
    for (final p in products) {
      if (p.title.toLowerCase().contains(productName.toLowerCase()) ||
          p.titleHi.toLowerCase().contains(productName.toLowerCase())) {
        matched = p;
        break;
      }
    }

    if (matched == null) {
      return IntentResult.failure(
        _isHindi()
            ? 'कैटलॉग में "$productName" नाम का कोई उत्पाद नहीं मिला।'
            : 'Could not find "$productName" in your catalogue.',
      );
    }

    _context.push('/product/${matched.id}');
    _closeChatbotSheet();
    return IntentResult.success(
      _isHindi() ? '"${matched.title}" खोल रहा हूँ।' : 'Opening "${matched.title}".',
    );
  }

  IntentResult _executeEditProduct(CraftsyIntent intent) {
    final productName = intent.parameters['product_name'] as String?;
    if (productName == null || productName.isEmpty) {
      return IntentResult.failure(_isHindi() ? 'उत्पाद का नाम बताएं।' : 'Please specify a product name.');
    }

    // Navigate to catalogue with search
    _ref.read(catalogueFilterProvider.notifier).setFilter(query: productName, category: null);
    _context.push('/catalogue');
    _closeChatbotSheet();
    return IntentResult.success(
      _isHindi() ? '"$productName" खोल रहा हूँ।' : 'Opening "$productName".',
    );
  }

  Future<IntentResult> _executeDeleteProduct(CraftsyIntent intent) async {
    final productName = intent.parameters['product_name'] as String?;
    if (productName == null || productName.isEmpty) {
      return IntentResult.failure(_isHindi() ? 'उत्पाद का नाम बताएं।' : 'Please specify a product name.');
    }

    // Find and delete product
    final products = _ref.read(productListProvider).value ?? [];
    Product? matched;
    for (final p in products) {
      if (p.title.toLowerCase().contains(productName.toLowerCase()) ||
          p.titleHi.toLowerCase().contains(productName.toLowerCase())) {
        matched = p;
        break;
      }
    }

    if (matched == null) {
      return IntentResult.failure(
        _isHindi()
            ? 'कैटलॉग में "$productName" नाम का कोई उत्पाद नहीं मिला।'
            : 'Could not find "$productName" in your catalogue.',
      );
    }

    await _ref.read(productListProvider.notifier).deleteProduct(matched.id);
    return IntentResult.success(
      _isHindi() ? '"${matched.title}" हटा दिया गया।' : '"${matched.title}" has been deleted.',
    );
  }

  IntentResult _executeCheckProductPrice(CraftsyIntent intent) {
    final productName = intent.parameters['product_name'] as String?;
    if (productName == null || productName.isEmpty) {
      return IntentResult.failure(_isHindi() ? 'उत्पाद का नाम बताएं।' : 'Please specify a product name.');
    }

    final products = _ref.read(productListProvider).value ?? [];
    Product? matched;
    for (final p in products) {
      if (p.title.toLowerCase().contains(productName.toLowerCase()) ||
          p.titleHi.toLowerCase().contains(productName.toLowerCase())) {
        matched = p;
        break;
      }
    }

    if (matched == null) {
      return IntentResult.failure(
        _isHindi()
            ? 'कैटलॉग में "$productName" नाम का कोई उत्पाद नहीं मिला।'
            : 'Could not find "$productName" in your catalogue.',
      );
    }

    return IntentResult.success(
      _isHindi()
          ? '"${matched.title}" की कीमत ₹${matched.price.toStringAsFixed(0)} है।'
          : '"${matched.title}" is priced at ₹${matched.price.toStringAsFixed(0)}.',
    );
  }

  // ── Order Executors ─────────────────────────────────────────────────

  IntentResult _executeCheckOrderStatus(CraftsyIntent intent) {
    final orderId = intent.parameters['order_id'] as String?;
    if (orderId == null || orderId.isEmpty) {
      // Navigate to orders screen
      _ref.read(homeTabIndexProvider.notifier).state = 1;
      _closeChatbotSheet();
      return IntentResult.success(_isHindi() ? 'आपके ऑर्डर खोल रहा हूँ।' : 'Opening your orders.');
    }

    // Find specific order
    final orders = _ref.read(ordersProvider);
    final order = orders.firstWhere(
      (o) => o.id == orderId,
      orElse: () => throw Exception('Order not found'),
    );

    return IntentResult.success(
      _isHindi()
          ? 'ऑर्डर #${order.id} की स्थिति: ${order.status.name}'
          : 'Order #${order.id} status: ${order.status.name}',
    );
  }

  // ── Draft Executors ─────────────────────────────────────────────────

  IntentResult _executeResumeDraft() {
    _ref.read(homeTabIndexProvider.notifier).state = 2;
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'ड्राफ्ट फिर से शुरू कर रहा हूँ।' : 'Resuming your draft.');
  }

  // ── App Executors ───────────────────────────────────────────────────

  IntentResult _executeChangeLanguage() {
    _context.push('/language-settings');
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'भाषा सेटिंग्स खोल रहा हूँ।' : 'Opening language settings.');
  }

  IntentResult _executeLogout() {
    _ref.read(authStateProvider.notifier).signOut();
    _closeChatbotSheet();
    return IntentResult.success(_isHindi() ? 'लॉग आउट कर रहा हूँ।' : 'Logging out.');
  }

  // ── Sync Executors ──────────────────────────────────────────────────

  Future<IntentResult> _executeSyncPending() async {
    final isOnline = _ref.read(connectivityProvider).value ?? true;
    if (!isOnline) {
      return IntentResult.failure(
        _isHindi()
            ? 'आप वर्तमान में ऑफ़लाइन हैं। इंटरनेट बहाल होते ही आपके लंबित उत्पाद स्वतः सिंक हो जाएंगे।'
            : 'You are currently offline. Your pending products will sync automatically when internet is restored.',
      );
    }

    try {
      final count = await _ref.read(productListProvider.notifier).syncQueue();
      if (count > 0) {
        return IntentResult.success(
          _isHindi()
              ? '$count ऑफ़लाइन उत्पाद सफलतापूर्वक सिंक हो गए हैं!'
              : '$count offline product${count > 1 ? 's' : ''} synced successfully!',
        );
      } else {
        return IntentResult.success(
          _isHindi()
              ? 'आपका कैटलॉग पूरी तरह सिंक है! कोई लंबित उत्पाद नहीं है।'
              : 'Your catalogue is fully synced! No pending products.',
        );
      }
    } catch (e) {
      return IntentResult.failure(
        _isHindi()
            ? 'सिंक करने में समस्या आई। कृपया पुनः प्रयास करें।'
            : 'Failed to sync. Please try again.',
      );
    }
  }

  // ── Helper Methods ──────────────────────────────────────────────────

  bool _isHindi() {
    return EasyLocalization.of(_context)?.locale.languageCode == 'hi' ||
        Localizations.maybeLocaleOf(_context)?.languageCode == 'hi';
  }

  void _closeChatbotSheet() {
    if (Navigator.of(_context, rootNavigator: true).canPop()) {
      Navigator.of(_context, rootNavigator: true).pop();
    }
  }

  Future<bool> _requestConfirmation(CraftsyIntent intent) async {
    final isHi = _isHindi();
    final description = IntentRegistry.getDescription(intent.type, isHindi: isHi);

    final result = await showDialog<bool>(
      context: _context,
      builder: (context) => AlertDialog(
        title: Text(isHi ? 'पुष्टि करें' : 'Confirm'),
        content: Text(
          isHi
              ? 'क्या आप "$description" करना चाहते हैं?'
              : 'Do you want to "$description"?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: Text(isHi ? 'नहीं' : 'No'),
          ),
          TextButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: Text(isHi ? 'हाँ' : 'Yes'),
          ),
        ],
      ),
    );

    return result ?? false;
  }
}
