import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

/// Processing state indicator — shows when AI is working.
///
/// Clear visual feedback that the app is processing. Does not rely on color alone.
class ProcessingState extends StatefulWidget {
  final String? label;
  final bool isProcessing;

  const ProcessingState({super.key, this.label, this.isProcessing = true});

  @override
  State<ProcessingState> createState() => _ProcessingStateState();
}

class _ProcessingStateState extends State<ProcessingState>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final effectiveLabel = widget.label ?? 'processing'.tr();

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
              color: AppColors.amber.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
              border: Border.all(
                color: AppColors.amber.withValues(alpha: 0.3),
                width: 1.5,
              ),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Spinning indicator
                SizedBox(
                  width: 24,
                  height: 24,
                  child: CircularProgressIndicator(
                    strokeWidth: 2.5,
                    color: AppColors.amber,
                  ),
                ),
                const SizedBox(width: AccessibilityTokens.spacingMd),
                Text(
                  effectiveLabel,
                  style: AppTextStyles.labelLarge.copyWith(
                    color: AppColors.amber,
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
