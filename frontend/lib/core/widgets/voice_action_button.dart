import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';
import '../../../core/services/app_tts_service.dart';

/// Primary voice interaction button for Craftsy V2.
///
/// Large touch target with clear idle/listening/processing/error states.
/// Works with existing voice infrastructure — does not create a second voice service.
class VoiceActionButton extends ConsumerStatefulWidget {
  final String label;
  final String? hintText;
  final VoidCallback? onPressed;
  final bool isListening;
  final bool isProcessing;
  final bool hasError;
  final String? errorMessage;
  final IconData icon;
  final bool useLargeSize;

  const VoiceActionButton({
    super.key,
    required this.label,
    this.hintText,
    this.onPressed,
    this.isListening = false,
    this.isProcessing = false,
    this.hasError = false,
    this.errorMessage,
    this.icon = Icons.mic_none_rounded,
    this.useLargeSize = true,
  });

  @override
  ConsumerState<VoiceActionButton> createState() => _VoiceActionButtonState();
}

class _VoiceActionButtonState extends ConsumerState<VoiceActionButton> {
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

  String get _stateLabel {
    if (widget.hasError) {
      return widget.errorMessage ?? 'voice_error'.tr();
    }
    if (widget.isProcessing) {
      return 'processing'.tr();
    }
    if (widget.isListening) {
      return 'listening'.tr();
    }
    return widget.label;
  }

  IconData get _stateIcon {
    if (widget.hasError) return Icons.error_outline_rounded;
    if (widget.isProcessing) return Icons.hourglass_top_rounded;
    if (widget.isListening) return Icons.mic_rounded;
    return widget.icon;
  }

  Color get _stateColor {
    if (widget.hasError) return AppColors.error;
    if (widget.isProcessing) return AppColors.warning;
    if (widget.isListening) return AppColors.coral;
    return AppColors.indigo;
  }

  Future<void> _speakHint() async {
    final text = widget.hintText ?? _stateLabel;
    await _ttsService.speak(text, languageCode: context.locale.languageCode);
  }

  @override
  Widget build(BuildContext context) {
    final isSpeaking = _ttsService.isSpeaking;
    final buttonHeight = widget.useLargeSize
        ? AccessibilityTokens.minTouchTargetLarge
        : AccessibilityTokens.minTouchTarget;

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Semantics(
          button: true,
          label: _stateLabel,
          hint: widget.hintText,
          liveRegion: true,
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              onTap: widget.onPressed,
              borderRadius: BorderRadius.circular(
                AccessibilityTokens.radiusFull,
              ),
              child: AnimatedContainer(
                duration: AccessibilityTokens.animationNormal,
                constraints: BoxConstraints(
                  minHeight: buttonHeight,
                  minWidth: widget.useLargeSize ? 200.0 : 120.0,
                ),
                padding: EdgeInsets.symmetric(
                  horizontal: widget.useLargeSize
                      ? AccessibilityTokens.spacingLg
                      : AccessibilityTokens.spacingMd,
                  vertical: AccessibilityTokens.spacingMd,
                ),
                decoration: BoxDecoration(
                  color: _stateColor.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(
                    AccessibilityTokens.radiusFull,
                  ),
                  border: Border.all(
                    color: _stateColor.withValues(alpha: 0.4),
                    width: 2,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: _stateColor.withValues(alpha: 0.15),
                      blurRadius: 8,
                      offset: const Offset(0, 2),
                    ),
                  ],
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Animated voice indicator
                    _buildVoiceIndicator(),
                    const SizedBox(width: AccessibilityTokens.spacingSm),
                    Flexible(
                      child: Text(
                        _stateLabel,
                        style: AppTextStyles.labelLarge.copyWith(
                          color: _stateColor,
                          fontWeight: FontWeight.w700,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
        // TTS hint button
        if (widget.hintText != null || widget.isListening)
          Padding(
            padding: const EdgeInsets.only(top: AccessibilityTokens.spacingXs),
            child: Semantics(
              button: true,
              label: isSpeaking ? 'stop_audio'.tr() : 'tap_to_hear'.tr(),
              child: InkWell(
                onTap: isSpeaking ? _ttsService.stop : _speakHint,
                borderRadius: BorderRadius.circular(
                  AccessibilityTokens.radiusSm,
                ),
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: AccessibilityTokens.spacingSm,
                    vertical: AccessibilityTokens.spacingXs,
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        isSpeaking
                            ? Icons.stop_circle_outlined
                            : Icons.volume_up_rounded,
                        size: 16,
                        color: AppColors.indigo,
                      ),
                      const SizedBox(width: AccessibilityTokens.spacingXs),
                      Text(
                        isSpeaking ? 'stop_audio'.tr() : 'tap_to_hear'.tr(),
                        style: AppTextStyles.labelSmall.copyWith(
                          color: AppColors.indigo,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
      ],
    );
  }

  Widget _buildVoiceIndicator() {
    if (widget.isListening) {
      return _AnimatedVoiceIndicator(color: _stateColor);
    }
    return Icon(_stateIcon, size: 24, color: _stateColor);
  }
}

/// Animated voice indicator shown when listening.
class _AnimatedVoiceIndicator extends StatefulWidget {
  final Color color;
  const _AnimatedVoiceIndicator({required this.color});

  @override
  State<_AnimatedVoiceIndicator> createState() =>
      _AnimatedVoiceIndicatorState();
}

class _AnimatedVoiceIndicatorState extends State<_AnimatedVoiceIndicator>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1200),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Container(
          width: 24,
          height: 24,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: widget.color.withValues(
              alpha: 0.2 + 0.3 * _controller.value,
            ),
            border: Border.all(color: widget.color, width: 2),
          ),
          child: Center(
            child: Container(
              width: 8,
              height: 8,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: widget.color,
              ),
            ),
          ),
        );
      },
    );
  }
}
