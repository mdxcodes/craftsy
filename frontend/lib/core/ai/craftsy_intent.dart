import 'package:flutter/foundation.dart';

/// Safety classification for AI-executed actions.
enum IntentSafety {
  /// Safe to execute immediately (navigation, viewing).
  safe,

  /// Requires explicit user confirmation before execution.
  confirmRequired,

  /// Not supported by the app — AI must decline.
  unsupported,
}

/// Centralized intent model for all Craftsy AI actions.
///
/// Every action that CraftMitra can execute (via text, voice, or button)
/// is represented as a [CraftsyIntent]. This ensures voice, chat, and
/// UI buttons all share the same action layer.
@immutable
class CraftsyIntent {
  /// Stable identifier (e.g., 'OPEN_ORDERS', 'ADD_PRODUCT').
  final String type;

  /// Human-readable localized description of the action.
  final String description;

  /// Parameters required for execution (e.g., product name, order ID).
  final Map<String, dynamic> parameters;

  /// Safety classification.
  final IntentSafety safety;

  /// Whether this action is destructive (requires confirmation).
  bool get isDestructive => safety == IntentSafety.confirmRequired;

  /// Whether this action requires a parameter to be present.
  bool get requiresParameter => parameters.isNotEmpty;

  const CraftsyIntent({
    required this.type,
    required this.description,
    this.parameters = const {},
    this.safety = IntentSafety.safe,
  });

  /// Create a copy with updated fields.
  CraftsyIntent copyWith({
    String? type,
    String? description,
    Map<String, dynamic>? parameters,
    IntentSafety? safety,
  }) {
    return CraftsyIntent(
      type: type ?? this.type,
      description: description ?? this.description,
      parameters: parameters ?? this.parameters,
      safety: safety ?? this.safety,
    );
  }

  @override
  String toString() => 'CraftsyIntent($type, safety: $safety)';
}
