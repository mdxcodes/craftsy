import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';
import '../providers/app_providers.dart';
import '../router/app_route_constants.dart';
import '../services/app_tts_service.dart';
import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';
import '../theme/app_text_styles.dart';
import 'app_button.dart';

/// Prominent draft resume card shown on Home when an unfinished listing exists.
///
/// Lets the artisan continue where they left off without searching for the draft.
class DraftResumeCard extends ConsumerWidget {
  const DraftResumeCard({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final draft = ref.watch(addProductFlowProvider);

    // Only show if there's actual draft content (image or text)
    final hasDraftContent =
        draft.originalImagePath.isNotEmpty ||
        draft.titleEn.isNotEmpty ||
        draft.titleHi.isNotEmpty ||
        draft.descriptionEn.isNotEmpty;

    if (!hasDraftContent) return const SizedBox.shrink();

    final ttsService = AppTtsService();

    return Semantics(
      button: true,
      label: 'draft_resume_title'.tr(),
      child: Card(
        margin: const EdgeInsets.only(bottom: AppSpacing.md),
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.card),
          side: BorderSide(color: AppColors.gold.withValues(alpha: 0.4)),
        ),
        child: InkWell(
          onTap: () {
            ttsService.speak(
              'draft_resume_title'.tr(),
              languageCode: context.locale.languageCode,
            );
            context.pushNamed(AppRouteConstants.addProduct);
          },
          borderRadius: BorderRadius.circular(AppRadii.card),
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.md),
            child: Row(
              children: [
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: AppColors.goldLight,
                    borderRadius: BorderRadius.circular(AppRadii.sm),
                  ),
                  child: const Icon(
                    Icons.edit_note_rounded,
                    color: AppColors.gold,
                    size: 24,
                  ),
                ),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'draft_resume_title'.tr(),
                        style: AppTextStyles.bodyMedium.copyWith(
                          fontWeight: FontWeight.w600,
                          color: AppColors.espresso,
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        'draft_resume_desc'.tr(),
                        style: AppTextStyles.bodySmall.copyWith(
                          color: AppColors.taupe,
                        ),
                      ),
                    ],
                  ),
                ),
    const SizedBox(width: AppSpacing.sm),
    Flexible(
      child: AppButton(
        label: 'draft_resume_action'.tr(),
        icon: Icons.arrow_forward_rounded,
        type: AppButtonType.primary,
        onPressed: () {
          context.pushNamed(AppRouteConstants.addProduct);
        },
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
