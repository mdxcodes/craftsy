import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:easy_localization/easy_localization.dart';
import '../services/language_service.dart';

/// Voice interaction button with state display.
///
/// Shows visual feedback for each voice state:
/// IDLE → LISTENING → PROCESSING → UNDERSTOOD → CONFIRMING → EXECUTING → SUCCESS/ERROR
///
/// Large touch target (56dp) for accessibility.
class VoiceInteractionButton extends StatelessWidget {
  final VoiceState state;
  final VoidCallback? onTap;
  final bool enabled;
  final double size;

  const VoiceInteractionButton({
    super.key,
    required this.state,
    this.onTap,
    this.enabled = true,
    this.size = 56,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: state.labelKey.tr(),
      button: true,
      enabled: enabled,
      child: GestureDetector(
        onTap: enabled ? onTap : null,
        child: Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: _backgroundColor(context),
            border: Border.all(color: _borderColor(context), width: 2),
            boxShadow: [
              BoxShadow(
                color: state.color.withValues(alpha: 0.3),
                blurRadius: state == VoiceState.listening ? 12 : 6,
                spreadRadius: state == VoiceState.listening ? 2 : 0,
              ),
            ],
          ),
          child: Center(
            child: AnimatedSwitcher(
              duration: const Duration(milliseconds: 200),
              child: _buildChild(context),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildChild(BuildContext context) {
    if (state == VoiceState.processing) {
      return SizedBox(
        key: const ValueKey('processing'),
        width: size * 0.4,
        height: size * 0.4,
        child: CircularProgressIndicator(strokeWidth: 2.5, color: state.color),
      );
    }

    return Icon(
      state.icon,
      key: ValueKey(state.name),
      size: size * 0.42,
      color: _iconColor(context),
    );
  }

  Color _backgroundColor(BuildContext context) {
    if (!enabled) return Colors.grey.shade200;
    if (state == VoiceState.listening) return Colors.red.shade50;
    if (state == VoiceState.error) return Colors.red.shade50;
    if (state == VoiceState.success) return Colors.green.shade50;
    return Theme.of(context).colorScheme.primaryContainer;
  }

  Color _borderColor(BuildContext context) {
    if (!enabled) return Colors.grey.shade300;
    return state.color;
  }

  Color _iconColor(BuildContext context) {
    if (!enabled) return Colors.grey;
    return state.color;
  }
}

/// Voice state display widget.
///
/// Shows the current voice interaction state with icon, label, and optional message.
class VoiceStateDisplay extends StatelessWidget {
  final VoiceState state;
  final String? message;
  final VoidCallback? onDismiss;

  const VoiceStateDisplay({
    super.key,
    required this.state,
    this.message,
    this.onDismiss,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: state.color.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: state.color.withValues(alpha: 0.3)),
      ),
      child: Row(
        children: [
          VoiceInteractionButton(state: state, onTap: onDismiss, size: 48),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  state.labelKey.tr(),
                  style: Theme.of(context).textTheme.titleSmall?.copyWith(
                    fontWeight: FontWeight.w600,
                    color: state.color,
                  ),
                ),
                if (message != null && message!.isNotEmpty) ...[
                  const SizedBox(height: 4),
                  Text(
                    message!,
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Colors.grey.shade700,
                    ),
                  ),
                ],
              ],
            ),
          ),
          if (onDismiss != null && state != VoiceState.idle)
            IconButton(
              icon: const Icon(Icons.close, size: 18),
              onPressed: onDismiss,
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(),
            ),
        ],
      ),
    );
  }
}

/// Voice transcript display.
///
/// Shows what the user said (transcript) with optional confidence indicator.
class VoiceTranscriptDisplay extends StatelessWidget {
  final String transcript;
  final String? languageCode;
  final double? confidence;

  const VoiceTranscriptDisplay({
    super.key,
    required this.transcript,
    this.languageCode,
    this.confidence,
  });

  @override
  Widget build(BuildContext context) {
    if (transcript.isEmpty) return const SizedBox.shrink();

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.blue.shade50,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.blue.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.record_voice_over, size: 16, color: Colors.blue),
              const SizedBox(width: 6),
              Text(
                'You said:',
                style: Theme.of(context).textTheme.labelSmall?.copyWith(
                  color: Colors.blue.shade700,
                  fontWeight: FontWeight.w600,
                ),
              ),
              if (languageCode != null) ...[
                const SizedBox(width: 6),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 4,
                    vertical: 1,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.blue.shade100,
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    languageCode!.toUpperCase(),
                    style: const TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w700,
                      color: Colors.blue,
                    ),
                  ),
                ),
              ],
            ],
          ),
          const SizedBox(height: 6),
          Text(transcript, style: Theme.of(context).textTheme.bodyMedium),
          if (confidence != null) ...[
            const SizedBox(height: 4),
            LinearProgressIndicator(
              value: confidence!,
              backgroundColor: Colors.blue.shade100,
              valueColor: AlwaysStoppedAnimation<Color>(
                confidence! > 0.8 ? Colors.green : Colors.orange,
              ),
              minHeight: 3,
            ),
          ],
        ],
      ),
    );
  }
}

/// Voice action confirmation dialog.
///
/// Shows a confirmation prompt for destructive or external actions.
class VoiceConfirmationDialog extends StatelessWidget {
  final String title;
  final String message;
  final String confirmLabel;
  final String cancelLabel;
  final bool isDestructive;
  final VoidCallback onConfirm;
  final VoidCallback onCancel;

  const VoiceConfirmationDialog({
    super.key,
    required this.title,
    required this.message,
    required this.confirmLabel,
    required this.cancelLabel,
    required this.onConfirm,
    required this.onCancel,
    this.isDestructive = false,
  });

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      title: Row(
        children: [
          Icon(
            isDestructive ? Icons.warning_amber_rounded : Icons.help_outline,
            color: isDestructive ? Colors.orange : Colors.blue,
          ),
          const SizedBox(width: 8),
          Expanded(child: Text(title)),
        ],
      ),
      content: Text(message),
      actions: [
        TextButton(onPressed: onCancel, child: Text(cancelLabel)),
        FilledButton(
          onPressed: onConfirm,
          style: FilledButton.styleFrom(
            backgroundColor: isDestructive ? Colors.red : Colors.blue,
          ),
          child: Text(confirmLabel),
        ),
      ],
    );
  }
}
