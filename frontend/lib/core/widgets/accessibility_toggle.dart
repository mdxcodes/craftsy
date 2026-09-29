import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';
import '../../../core/services/app_sound_service.dart';

/// Accessibility toggle — allows users to enable/disable sound and haptics.
///
/// Persists settings via Hive. Simple on/off with clear labels.
class AccessibilityToggle extends ConsumerWidget {
  const AccessibilityToggle({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final soundService = AppSoundService.instance;

    return Container(
      padding: const EdgeInsets.all(AccessibilityTokens.spacingMd),
      decoration: BoxDecoration(
        color: AppColors.cardSurface,
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
        border: Border.all(color: AppColors.line, width: 1),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'accessibility_settings'.tr(),
            style: AppTextStyles.labelLarge.copyWith(
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: AccessibilityTokens.spacingMd),
          // Sound toggle
          _buildToggleRow(
            context,
            icon: soundService.isSoundEnabled
                ? Icons.volume_up_rounded
                : Icons.volume_off_rounded,
            label: 'sound_effects'.tr(),
            value: soundService.isSoundEnabled,
            onChanged: (value) async {
              await soundService.setSoundEnabled(value);
            },
          ),
          const SizedBox(height: AccessibilityTokens.spacingSm),
          // Haptics toggle
          _buildToggleRow(
            context,
            icon: soundService.isHapticsEnabled
                ? Icons.vibration_rounded
                : Icons.phone_iphone_rounded,
            label: 'haptic_feedback'.tr(),
            value: soundService.isHapticsEnabled,
            onChanged: (value) async {
              await soundService.setHapticsEnabled(value);
            },
          ),
        ],
      ),
    );
  }

  Widget _buildToggleRow(
    BuildContext context, {
    required IconData icon,
    required String label,
    required bool value,
    required ValueChanged<bool> onChanged,
  }) {
    return Semantics(
      toggled: value,
      label: label,
      child: InkWell(
        onTap: () => onChanged(!value),
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusMd),
        child: Padding(
          padding: const EdgeInsets.symmetric(
            vertical: AccessibilityTokens.spacingSm,
          ),
          child: Row(
            children: [
              Icon(
                icon,
                size: 22,
                color: value ? AppColors.burgundy : AppColors.taupe,
              ),
              const SizedBox(width: AccessibilityTokens.spacingMd),
              Expanded(
                child: Text(
                  label,
                  style: AppTextStyles.bodyMedium.copyWith(
                    color: value ? AppColors.espresso : AppColors.taupe,
                  ),
                ),
              ),
              // Toggle switch
              Switch(
                value: value,
                onChanged: onChanged,
                activeThumbColor: AppColors.burgundy,
                inactiveThumbColor: AppColors.taupe,
                inactiveTrackColor: AppColors.warmMist,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
