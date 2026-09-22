import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

/// Visual status chip for success/warning/pending/error/offline states.
///
/// Icon-first, text-second pattern for quick visual recognition.
/// Does not rely on color alone — always includes an icon.
enum VisualStatusType { success, warning, pending, error, offline }

class VisualStatusChip extends StatelessWidget {
  final VisualStatusType type;
  final String label;
  final bool compact;

  const VisualStatusChip({
    super.key,
    required this.type,
    required this.label,
    this.compact = false,
  });

  @override
  Widget build(BuildContext context) {
    final config = _getConfig(type);

    return Semantics(
      label: '${config.semanticLabel}: $label',
      child: Container(
        padding: EdgeInsets.symmetric(
          horizontal: compact
              ? AccessibilityTokens.spacingSm
              : AccessibilityTokens.spacingMd,
          vertical: compact
              ? AccessibilityTokens.spacingXs
              : AccessibilityTokens.spacingSm,
        ),
        decoration: BoxDecoration(
          color: config.backgroundColor,
          borderRadius: BorderRadius.circular(AccessibilityTokens.radiusFull),
          border: Border.all(color: config.borderColor, width: 1),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              config.icon,
              size: compact ? 14 : 16,
              color: config.foregroundColor,
            ),
            const SizedBox(width: AccessibilityTokens.spacingXs),
            Text(
              label,
              style:
                  (compact
                          ? AppTextStyles.labelSmall
                          : AppTextStyles.labelMedium)
                      .copyWith(
                        color: config.foregroundColor,
                        fontWeight: FontWeight.w600,
                      ),
            ),
          ],
        ),
      ),
    );
  }

  _StatusConfig _getConfig(VisualStatusType type) {
    switch (type) {
      case VisualStatusType.success:
        return _StatusConfig(
          icon: Icons.check_circle_outline_rounded,
          backgroundColor: AppColors.successLight,
          foregroundColor: AppColors.success,
          borderColor: AppColors.success.withValues(alpha: 0.3),
          semanticLabel: 'status_success'.tr(),
        );
      case VisualStatusType.warning:
        return _StatusConfig(
          icon: Icons.warning_amber_rounded,
          backgroundColor: AppColors.amberLight,
          foregroundColor: AppColors.amber,
          borderColor: AppColors.amber.withValues(alpha: 0.3),
          semanticLabel: 'status_warning'.tr(),
        );
      case VisualStatusType.pending:
        return _StatusConfig(
          icon: Icons.hourglass_top_rounded,
          backgroundColor: AppColors.amberLight,
          foregroundColor: AppColors.amber,
          borderColor: AppColors.amber.withValues(alpha: 0.3),
          semanticLabel: 'status_pending'.tr(),
        );
      case VisualStatusType.error:
        return _StatusConfig(
          icon: Icons.error_outline_rounded,
          backgroundColor: AppColors.coralLight,
          foregroundColor: AppColors.coral,
          borderColor: AppColors.coral.withValues(alpha: 0.3),
          semanticLabel: 'status_error'.tr(),
        );
      case VisualStatusType.offline:
        return _StatusConfig(
          icon: Icons.wifi_off_rounded,
          backgroundColor: AppColors.parchmentDeep,
          foregroundColor: AppColors.inkSoft,
          borderColor: AppColors.inkSoft.withValues(alpha: 0.3),
          semanticLabel: 'status_offline'.tr(),
        );
    }
  }
}

class _StatusConfig {
  final IconData icon;
  final Color backgroundColor;
  final Color foregroundColor;
  final Color borderColor;
  final String semanticLabel;

  const _StatusConfig({
    required this.icon,
    required this.backgroundColor,
    required this.foregroundColor,
    required this.borderColor,
    required this.semanticLabel,
  });
}
