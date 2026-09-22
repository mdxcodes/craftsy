import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

/// Listening state indicator — shows when the app is listening to voice input.
///
/// Large, animated, and clearly visible. Does not rely on color alone.
class ListeningState extends StatefulWidget {
  final String? label;
  final bool isListening;

  const ListeningState({super.key, this.label, this.isListening = true});

  @override
  State<ListeningState> createState() => _ListeningStateState();
}

class _ListeningStateState extends State<ListeningState>
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
    final effectiveLabel = widget.label ?? 'listening'.tr();

    return Semantics(
      label: effectiveLabel,
      liveRegion: true,
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AccessibilityTokens.spacingLg,
              vertical: AccessibilityTokens.spacingMd,
            ),
            decoration: BoxDecoration(
              color: AppColors.coral.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
              border: Border.all(
                color: AppColors.coral.withValues(alpha: 0.3),
                width: 1.5,
              ),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Animated listening indicator
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: AppColors.coral.withValues(
                      alpha: 0.2 + 0.3 * _controller.value,
                    ),
                    border: Border.all(color: AppColors.coral, width: 2),
                  ),
                  child: Center(
                    child: Container(
                      width: 12,
                      height: 12,
                      decoration: const BoxDecoration(
                        shape: BoxShape.circle,
                        color: AppColors.coral,
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: AccessibilityTokens.spacingMd),
                Text(
                  effectiveLabel,
                  style: AppTextStyles.labelLarge.copyWith(
                    color: AppColors.coral,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
