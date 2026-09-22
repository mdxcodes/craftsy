import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../services/app_tts_service.dart';
import 'craftsy_intent.dart';
import 'intent_executor.dart';
import 'intent_parser.dart';
import 'intent_registry.dart';

/// Provider for the intent executor.
final intentExecutorProvider = Provider<IntentExecutor>((ref) {
  // This will be overridden in the widget tree with a proper BuildContext.
  // We use a placeholder here — the actual executor is created in the widget.
  throw UnimplementedError('IntentExecutor must be created with a BuildContext');
});

/// Handles AI action execution from chat/voice input.
///
/// This is the bridge between the chat layer and the intent executor.
/// It parses user input, executes intents, and manages the response flow.
class IntentActionHandler {
  final Ref _ref;
  final BuildContext _context;
  final AppTtsService _tts;

  IntentActionHandler(this._ref, this._context, this._tts);

  /// Process user input (text or transcribed voice) and execute any matching intent.
  ///
  /// Returns true if an intent was executed, false otherwise.
  Future<bool> processInput(String input, {String languageCode = 'en'}) async {
    final intent = IntentParser.parse(input, languageCode: languageCode);
    if (intent == null) return false;

    // Execute the intent
    final executor = IntentExecutor(_ref, _context);
    final result = await executor.execute(intent);

    // Handle the result
    await _handleResult(result, intent, languageCode);

    return true;
  }

  /// Handle the result of an intent execution.
  Future<void> _handleResult(IntentResult result, CraftsyIntent intent, String languageCode) async {
    final isHi = languageCode == 'hi';

    if (!result.executed) {
      // Action was cancelled or not executed
      if (!result.success && result.message.isNotEmpty) {
        _showSnackBar(result.message);
      }
      return;
    }

    if (result.success) {
      // Show success message
      _showSnackBar(result.message);

      // Speak the result
      await _tts.speak(
        result.message,
        languageCode: isHi ? 'hi' : 'en',
      );
    } else {
      // Show error message
      _showSnackBar(result.message);
    }
  }

  void _showSnackBar(String message) {
    if (!_context.mounted) return;
    ScaffoldMessenger.of(_context).showSnackBar(
      SnackBar(
        content: Text(message),
        duration: const Duration(seconds: 3),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  /// Check if an intent requires confirmation and show the confirmation dialog.
  ///
  /// Returns true if the user confirmed, false otherwise.
  Future<bool> confirmDestructiveAction(CraftsyIntent intent) async {
    final isHi = EasyLocalization.of(_context)?.locale.languageCode == 'hi';
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

/// Provider for the intent action handler.
final intentActionHandlerProvider = Provider<IntentActionHandler>((ref) {
  throw UnimplementedError('IntentActionHandler must be created with a BuildContext');
});
