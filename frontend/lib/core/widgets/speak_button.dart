import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';
import '../../../core/services/app_tts_service.dart';

/// Reusable text-to-speech affordance button.
///
/// Supports selected/localized text, accessible label, and visual speaking state.
/// Uses the shared AppTtsService — does not create a second TTS instance.
class SpeakButton extends StatefulWidget {
  final String text;
  final String? label;
  final bool compact;
  final Color? color;

  const SpeakButton({
    super.key,
    required this.text,
    this.label,
    this.compact = false,
    this.color,
  });

  @override
  State<SpeakButton> createState() => _SpeakButtonState();
}

class _SpeakButtonState extends State<SpeakButton> {
  late AppTtsService _ttsService;

  @override
  void initState() {
    super.initState();
    _ttsService = AppTtsService();
    _ttsService.onStateChanged = () => setState(() {});
  }

  @override
  void dispose() {
    _ttsService.dispose();
    super.dispose();
  }

  Future<void> _toggle() async {
    if (_ttsService.isSpeaking) {
      await _ttsService.stop();
    } else {
      await _ttsService.speak(
        widget.text,
        languageCode: context.locale.languageCode,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final isSpeaking = _ttsService.isSpeaking;
    final effectiveColor = widget.color ?? AppColors.indigo;
    final effectiveLabel =
        widget.label ?? (isSpeaking ? 'stop_audio'.tr() : 'tap_to_hear'.tr());

    if (widget.compact) {
      return Semantics(
        button: true,
        label: effectiveLabel,
        child: InkWell(
          onTap: _toggle,
          borderRadius: BorderRadius.circular(AccessibilityTokens.radiusSm),
          child: Padding(
            padding: const EdgeInsets.all(6),
            child: Icon(
              isSpeaking ? Icons.stop_circle_outlined : Icons.volume_up_rounded,
              size: 20,
              color: effectiveColor,
            ),
          ),
        ),
      );
    }

    return Semantics(
      button: true,
      label: effectiveLabel,
      child: InkWell(
        onTap: _toggle,
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusMd),
        child: Container(
          padding: const EdgeInsets.symmetric(
            horizontal: AccessibilityTokens.spacingMd,
            vertical: AccessibilityTokens.spacingSm,
          ),
          decoration: BoxDecoration(
            color: effectiveColor.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(AccessibilityTokens.radiusMd),
            border: Border.all(
              color: effectiveColor.withValues(alpha: 0.3),
              width: 1,
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                isSpeaking
                    ? Icons.stop_circle_outlined
                    : Icons.volume_up_rounded,
                size: 18,
                color: effectiveColor,
              ),
              const SizedBox(width: AccessibilityTokens.spacingXs),
              Text(
                effectiveLabel,
                style: AppTextStyles.labelSmall.copyWith(
                  color: effectiveColor,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
