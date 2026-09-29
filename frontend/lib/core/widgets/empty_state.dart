import 'package:flutter/material.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

/// Empty state — shown when there is no content to display.
///
/// Icon + short message + optional action. Clear and non-alarming.
class EmptyState extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? message;
  final String? actionLabel;
  final VoidCallback? onAction;

  const EmptyState({
    super.key,
    required this.icon,
    required this.title,
    this.message,
    this.actionLabel,
    this.onAction,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AccessibilityTokens.spacingXl),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Icon
            Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(
                color: AppColors.warmMist,
                borderRadius: BorderRadius.circular(
                  AccessibilityTokens.radiusLg,
                ),
              ),
              child: Icon(icon, size: 40, color: AppColors.taupe),
            ),
            const SizedBox(height: AccessibilityTokens.spacingLg),
            // Title
            Text(
              title,
              style: AppTextStyles.headlineMedium.copyWith(
                color: AppColors.espresso,
              ),
              textAlign: TextAlign.center,
            ),
            // Message
            if (message != null) ...[
              const SizedBox(height: AccessibilityTokens.spacingSm),
              Text(
                message!,
                style: AppTextStyles.bodyMedium.copyWith(
                  color: AppColors.taupe,
                ),
                textAlign: TextAlign.center,
              ),
            ],
            // Action
            if (actionLabel != null && onAction != null) ...[
              const SizedBox(height: AccessibilityTokens.spacingLg),
              Semantics(
                button: true,
                label: actionLabel,
                child: Material(
                  color: Colors.transparent,
                  child: InkWell(
                    onTap: onAction,
                    borderRadius: BorderRadius.circular(
                      AccessibilityTokens.radiusFull,
                    ),
                    child: Container(
                      constraints: const BoxConstraints(
                        minHeight: AccessibilityTokens.minTouchTargetLarge,
                      ),
                      padding: const EdgeInsets.symmetric(
                        horizontal: AccessibilityTokens.spacingLg,
                        vertical: AccessibilityTokens.spacingMd,
                      ),
                      decoration: BoxDecoration(
                        color: AppColors.burgundy,
                        borderRadius: BorderRadius.circular(
                          AccessibilityTokens.radiusFull,
                        ),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.add_rounded,
                            size: 20,
                            color: Colors.white,
                          ),
                          const SizedBox(width: AccessibilityTokens.spacingSm),
                          Text(
                            actionLabel!,
                            style: AppTextStyles.labelLarge.copyWith(
                              color: Colors.white,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
