import 'package:flutter/material.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';
import '../../../core/services/app_sound_service.dart';

/// Primary action button — the single dominant action per screen.
///
/// Centralized button styling with large touch target and no duplicated sizing values.
class PrimaryActionButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final IconData? icon;
  final bool isLoading;
  final bool fullWidth;
  final Color? backgroundColor;

  const PrimaryActionButton({
    super.key,
    required this.label,
    this.onPressed,
    this.icon,
    this.isLoading = false,
    this.fullWidth = true,
    this.backgroundColor,
  });

  @override
  Widget build(BuildContext context) {
    final effectiveOnPressed = AppSoundFeedback.wrap(onPressed);
    final bgColor = backgroundColor ?? AppColors.burgundy;

    return Semantics(
      button: true,
      label: label,
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: isLoading ? null : effectiveOnPressed,
          borderRadius: BorderRadius.circular(AccessibilityTokens.radiusFull),
          child: AnimatedContainer(
            duration: AccessibilityTokens.animationNormal,
            constraints: BoxConstraints(
              minHeight: AccessibilityTokens.minTouchTargetLarge,
              minWidth: fullWidth
                  ? double.infinity
                  : AccessibilityTokens.minTouchTargetLarge * 2,
            ),
            padding: const EdgeInsets.symmetric(
              horizontal: AccessibilityTokens.spacingLg,
              vertical: AccessibilityTokens.spacingMd,
            ),
            decoration: BoxDecoration(
              color: isLoading ? AppColors.warmMist : bgColor,
              borderRadius: BorderRadius.circular(
                AccessibilityTokens.radiusFull,
              ),
              boxShadow: isLoading
                  ? []
                  : [
                      BoxShadow(
                        color: bgColor.withValues(alpha: 0.3),
                        blurRadius: 8,
                        offset: const Offset(0, 3),
                      ),
                    ],
            ),
            child: isLoading
                ? Center(
                    child: SizedBox(
                      width: 24,
                      height: 24,
                      child: CircularProgressIndicator(
                        strokeWidth: 2.5,
                        color: AppColors.cardSurface,
                      ),
                    ),
                  )
                : Row(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      if (icon != null) ...[
                        Icon(icon, size: 24, color: AppColors.cardSurface),
                        const SizedBox(width: AccessibilityTokens.spacingSm),
                      ],
                      Flexible(
                        child: Text(
                          label,
                          style: AppTextStyles.labelLarge.copyWith(
                            color: AppColors.cardSurface,
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
    );
  }
}
