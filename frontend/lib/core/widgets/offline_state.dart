import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

/// Offline state indicator — shown when there is no internet connection.
///
/// Clear, non-alarming. Explains what will happen when connectivity returns.
class OfflineState extends StatelessWidget {
  final String? label;
  final String? message;
  final bool isOffline;

  const OfflineState({
    super.key,
    this.label,
    this.message,
    this.isOffline = true,
  });

  @override
  Widget build(BuildContext context) {
    final effectiveLabel = label ?? 'offline'.tr();
    final effectiveMessage = message ?? 'offline_message'.tr();

    return Semantics(
      label: effectiveLabel,
      liveRegion: true,
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: AccessibilityTokens.spacingLg,
          vertical: AccessibilityTokens.spacingMd,
        ),
        decoration: BoxDecoration(
          color: AppColors.warmMist,
          borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
          border: Border.all(
            color: AppColors.taupe.withValues(alpha: 0.2),
            width: 1,
          ),
        ),
        child: Row(
          children: [
            Icon(Icons.wifi_off_rounded, size: 24, color: AppColors.taupe),
            const SizedBox(width: AccessibilityTokens.spacingMd),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    effectiveLabel,
                    style: AppTextStyles.labelLarge.copyWith(
                      color: AppColors.espresso,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  if (message != null) ...[
                    const SizedBox(height: AccessibilityTokens.spacingXs),
                    Text(
                      effectiveMessage,
                      style: AppTextStyles.bodySmall.copyWith(
                        color: AppColors.taupe,
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
