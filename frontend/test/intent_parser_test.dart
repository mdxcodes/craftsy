import 'package:flutter_test/flutter_test.dart';
import 'package:craftsy/core/ai/craftsy_intent.dart';
import 'package:craftsy/core/ai/intent_registry.dart';
import 'package:craftsy/core/ai/intent_parser.dart';

void main() {
  group('CraftsyIntent', () {
    test('creates intent with default values', () {
      const intent = CraftsyIntent(
        type: 'OPEN_ORDERS',
        description: 'Open my orders',
      );

      expect(intent.type, 'OPEN_ORDERS');
      expect(intent.description, 'Open my orders');
      expect(intent.parameters, isEmpty);
      expect(intent.safety, IntentSafety.safe);
      expect(intent.isDestructive, false);
      expect(intent.requiresParameter, false);
    });

    test('creates intent with confirmation required', () {
      const intent = CraftsyIntent(
        type: 'DELETE_PRODUCT',
        description: 'Delete a product',
        safety: IntentSafety.confirmRequired,
        parameters: {'product_name': 'test'},
      );

      expect(intent.isDestructive, true);
      expect(intent.requiresParameter, true);
    });

    test('copyWith updates fields correctly', () {
      const intent = CraftsyIntent(
        type: 'OPEN_ORDERS',
        description: 'Open my orders',
      );

      final updated = intent.copyWith(
        type: 'OPEN_CATALOGUE',
        description: 'Open catalogue',
      );

      expect(updated.type, 'OPEN_CATALOGUE');
      expect(updated.description, 'Open catalogue');
    });
  });

  group('IntentRegistry', () {
    test('returns metadata for supported intent', () {
      final metadata = IntentRegistry.get('OPEN_ORDERS');
      expect(metadata, isNotNull);
      expect(metadata!.type, 'OPEN_ORDERS');
      expect(metadata.safety, IntentSafety.safe);
    });

    test('returns null for unsupported intent', () {
      final metadata = IntentRegistry.get('UNSUPPORTED_ACTION');
      expect(metadata, isNull);
    });

    test('isSupported returns correct values', () {
      expect(IntentRegistry.isSupported('OPEN_ORDERS'), true);
      expect(IntentRegistry.isSupported('UNSUPPORTED'), false);
    });

    test('returns all supported types', () {
      final types = IntentRegistry.supportedTypes;
      expect(types, contains('OPEN_ORDERS'));
      expect(types, contains('OPEN_CATALOGUE'));
      expect(types, contains('ADD_PRODUCT'));
      expect(types, contains('DELETE_PRODUCT'));
    });

    test('returns localized descriptions', () {
      final enDesc = IntentRegistry.getDescription('OPEN_ORDERS', isHindi: false);
      final hiDesc = IntentRegistry.getDescription('OPEN_ORDERS', isHindi: true);

      expect(enDesc, 'Open my orders');
      expect(hiDesc, 'मेरे ऑर्डर खोलें');
    });

    test('safe intents do not require confirmation', () {
      final safeIntents = IntentRegistry.safeIntents;
      for (final intent in safeIntents) {
        expect(intent.safety, IntentSafety.safe);
      }
    });

    test('confirm-required intents are marked correctly', () {
      final confirmIntents = IntentRegistry.confirmRequiredIntents;
      expect(confirmIntents, isNotEmpty);
      for (final intent in confirmIntents) {
        expect(intent.safety, IntentSafety.confirmRequired);
      }
    });
  });

  group('IntentParser', () {
    test('parses OPEN_ORDERS intent', () {
      final intent = IntentParser.parse('open my orders');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_ORDERS');
      expect(intent.safety, IntentSafety.safe);
    });

    test('parses OPEN_CATALOGUE intent', () {
      final intent = IntentParser.parse('show my catalogue');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_CATALOGUE');
    });

    test('parses OPEN_EARNINGS intent', () {
      final intent = IntentParser.parse('show my earnings');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_EARNINGS');
    });

    test('parses OPEN_PROFILE intent', () {
      final intent = IntentParser.parse('open my profile');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_PROFILE');
    });

    test('parses ADD_PRODUCT intent', () {
      final intent = IntentParser.parse('add a new product');
      expect(intent, isNotNull);
      expect(intent!.type, 'ADD_PRODUCT');
    });

    test('parses DELETE_PRODUCT intent with confirmation', () {
      final intent = IntentParser.parse('delete my pottery');
      expect(intent, isNotNull);
      expect(intent!.type, 'DELETE_PRODUCT');
      expect(intent.safety, IntentSafety.confirmRequired);
      expect(intent.parameters['product_name'], 'pottery');
    });

    test('parses OPEN_PRODUCT intent with product name', () {
      final intent = IntentParser.parse('open my terracotta pot');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_PRODUCT');
      expect(intent.parameters['product_name'], 'terracotta pot');
    });

    test('parses CHECK_PRODUCT_PRICE intent', () {
      final intent = IntentParser.parse('price of my vase');
      expect(intent, isNotNull);
      expect(intent!.type, 'CHECK_PRODUCT_PRICE');
      expect(intent.parameters['product_name'], 'vase');
    });

    test('parses SYNC_PENDING intent', () {
      final intent = IntentParser.parse('sync my pending products');
      expect(intent, isNotNull);
      expect(intent!.type, 'SYNC_PENDING');
    });

    test('parses LOGOUT intent with confirmation', () {
      final intent = IntentParser.parse('logout');
      expect(intent, isNotNull);
      expect(intent!.type, 'LOGOUT');
      expect(intent.safety, IntentSafety.confirmRequired);
    });

    test('parses Hindi intents', () {
      final intent = IntentParser.parse('मेरे ऑर्डर खोलें');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_ORDERS');
    });

    test('returns null for unrecognized input', () {
      final intent = IntentParser.parse('hello world');
      expect(intent, isNull);
    });

    test('returns null for empty input', () {
      final intent = IntentParser.parse('');
      expect(intent, isNull);
    });

    test('parses CHECK_ORDER_STATUS with order ID', () {
      final intent = IntentParser.parse('check order ORD-1001');
      expect(intent, isNotNull);
      expect(intent!.type, 'CHECK_ORDER_STATUS');
      expect(intent.parameters['order_id'], 'ORD-1001');
    });

    test('parses OPEN_TUTORIAL intent', () {
      final intent = IntentParser.parse('start tutorial');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_TUTORIAL');
    });

    test('parses OPEN_LANGUAGE_SETTINGS intent', () {
      final intent = IntentParser.parse('change language');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_LANGUAGE_SETTINGS');
    });

    test('parses OPEN_PACKAGING_HELP intent', () {
      final intent = IntentParser.parse('packaging help');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_PACKAGING_HELP');
    });

    test('parses OPEN_LABEL_MAKER intent', () {
      final intent = IntentParser.parse('label maker');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_LABEL_MAKER');
    });

    test('parses Hindi packaging intent', () {
      final intent = IntentParser.parse('पैकेजिंग मदद');
      expect(intent, isNotNull);
      expect(intent!.type, 'OPEN_PACKAGING_HELP');
    });
  });
}
