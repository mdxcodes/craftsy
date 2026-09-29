import 'package:flutter/material.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/motifs/tanka_stitch_painter.dart';

/// V2 Step Progress Bar — visual journey indicator.
///
/// Shows the 5-step selling journey with emoji icons and visual progress.
/// Current step is highlighted with a glow effect.
/// Completed steps show a checkmark.
/// Does NOT show "Step X of Y" text — communicates visually.
class StepProgressBar extends StatelessWidget {
  final int currentStep; // 0 to 4
  final int totalSteps;
  final ValueChanged<int>? onStepTapped;

  const StepProgressBar({
    super.key,
    required this.currentStep,
    this.totalSteps = 5,
    this.onStepTapped,
  });

  static const List<String> _stepEmojis = [
    '📸', // Capture
    '🎤', // Describe
    '✨', // AI Review
    '💰', // Pricing
    '✅', // Confirm
  ];

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.sm,
      ),
      child: Row(
        children: List.generate(totalSteps * 2 - 1, (index) {
          if (index.isOdd) {
            final stepIndex = index ~/ 2;
            final isCompleted = stepIndex < currentStep;
            return Expanded(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 2.0),
                child: SizedBox(
                  height: 3,
                  child: isCompleted
                      ? const CustomPaint(
                          painter: TankaStitchPainter(
                            color: AppColors.sage,
                            strokeWidth: 2,
                            dashLength: 5,
                            dashGap: 4,
                          ),
                        )
                      : Container(height: 2, color: AppColors.warmMist),
                ),
              ),
            );
          } else {
            final stepIndex = index ~/ 2;
            final isCompleted = stepIndex < currentStep;
            final isCurrent = stepIndex == currentStep;
            final emoji = stepIndex < _stepEmojis.length
                ? _stepEmojis[stepIndex]
                : '⚪';

            Color bgColor = AppColors.cardSurface;
            Color borderColor = AppColors.warmMist;
            List<BoxShadow>? shadows;

            if (isCompleted) {
              bgColor = AppColors.sage;
              borderColor = AppColors.sage;
            } else if (isCurrent) {
              bgColor = AppColors.burgundy;
              borderColor = AppColors.burgundy;
              shadows = [
                BoxShadow(
                  color: AppColors.burgundyLight,
                  spreadRadius: 4,
                  blurRadius: 0,
                ),
              ];
            }

            final canNavigateBack = isCompleted;

            return GestureDetector(
              onTap: (canNavigateBack && onStepTapped != null)
                  ? () => onStepTapped!(stepIndex)
                  : null,
              behavior: canNavigateBack
                  ? HitTestBehavior.opaque
                  : HitTestBehavior.deferToChild,
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 250),
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: bgColor,
                  border: Border.all(color: borderColor, width: 2),
                  boxShadow: shadows,
                ),
                alignment: Alignment.center,
                child: Text(emoji, style: const TextStyle(fontSize: 18)),
              ),
            );
          }
        }),
      ),
    );
  }
}
