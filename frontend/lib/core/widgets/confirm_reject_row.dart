import 'package:flutter/material.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';
import '../../../core/services/app_sound_service.dart';

/// Clear positive/negative action row.
///
/// Strong visual distinction between confirm and reject actions.
/// Accessible semantics for screen readers.
class ConfirmRejectRow extends StatelessWidget {
  final String confirmLabel;
  final String rejectLabel;
  final VoidCallback? onConfirm;
  final VoidCallback? onReject;
  final bool isLoading;

  const ConfirmRejectRow({
    super.key,
    required this.confirmLabel,
    required this.rejectLabel,
    this.onConfirm,
    this.onReject,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        // Reject button (negative action)
        Expanded(
          child: Semantics(
            button: true,
            label: rejectLabel,
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: isLoading ? null : AppSoundFeedback.wrap(onReject),
                borderRadius: BorderRadius.circular(
                  AccessibilityTokens.radiusFull,
                ),
                child: AnimatedContainer(
                  duration: AccessibilityTokens.animationNormal,
                  constraints: const BoxConstraints(
                    minHeight: AccessibilityTokens.minTouchTargetLarge,
                  ),
                  padding: const EdgeInsets.symmetric(
                    horizontal: AccessibilityTokens.spacingMd,
                    vertical: AccessibilityTokens.spacingMd,
                  ),
                  decoration: BoxDecoration(
                    color: AppColors.cardSurface,
                    borderRadius: BorderRadius.circular(
                      AccessibilityTokens.radiusFull,
                    ),
                    border: Border.all(
                      color: AppColors.error.withValues(alpha: 0.4),
                      width: 2,
                    ),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.close_rounded,
                        size: 22,
                        color: AppColors.error,
                      ),
                      const SizedBox(width: AccessibilityTokens.spacingSm),
                      Flexible(
                        child: Text(
                          rejectLabel,
                          style: AppTextStyles.labelLarge.copyWith(
                            color: AppColors.error,
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
        ),
        const SizedBox(width: AccessibilityTokens.spacingMd),
        // Confirm button (positive action)
        Expanded(
          child: Semantics(
            button: true,
            label: confirmLabel,
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: isLoading ? null : AppSoundFeedback.wrap(onConfirm),
                borderRadius: BorderRadius.circular(
                  AccessibilityTokens.radiusFull,
                ),
                child: AnimatedContainer(
                  duration: AccessibilityTokens.animationNormal,
                  constraints: const BoxConstraints(
                    minHeight: AccessibilityTokens.minTouchTargetLarge,
                  ),
                  padding: const EdgeInsets.symmetric(
                    horizontal: AccessibilityTokens.spacingMd,
                    vertical: AccessibilityTokens.spacingMd,
                  ),
                  decoration: BoxDecoration(
                    color: isLoading
                        ? AppColors.parchmentDeep
                        : AppColors.success,
                    borderRadius: BorderRadius.circular(
                      AccessibilityTokens.radiusFull,
                    ),
                    boxShadow: isLoading
                        ? []
                        : [
                            BoxShadow(
                              color: AppColors.success.withValues(alpha: 0.3),
                              blurRadius: 8,
                              offset: const Offset(0, 3),
                            ),
                          ],
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      if (isLoading)
                        SizedBox(
                          width: 22,
                          height: 22,
                          child: CircularProgressIndicator(
                            strokeWidth: 2.5,
                            color: AppColors.textOnPrimary,
                          ),
                        )
                      else
                        Icon(
                          Icons.check_rounded,
                          size: 22,
                          color: AppColors.textOnPrimary,
                        ),
                      const SizedBox(width: AccessibilityTokens.spacingSm),
                      Flexible(
                        child: Text(
                          confirmLabel,
                          style: AppTextStyles.labelLarge.copyWith(
                            color: AppColors.textOnPrimary,
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
        ),
      ],
    );
  }
}
