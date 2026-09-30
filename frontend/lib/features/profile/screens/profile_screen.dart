import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/router/app_route_constants.dart';
import '../../../core/widgets/accessibility_toggle.dart';
import '../../../core/widgets/app_button.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../../../core/widgets/app_confirmation_dialog.dart';
import '../../../core/providers/app_providers.dart';
import '../../auth/providers/auth_provider.dart';
import '../../orders/providers/orders_provider.dart';
import '../../orders/models/order.dart';
import '../../../data/models/user_profile.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authStateProvider);
    final profile = ref.watch(userProfileProvider);

    return AppScaffold(
      title: 'profile_title'.tr(),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppSpacing.screenPadding),
        child: Column(
          children: [
            // Compact Profile Header Card — V2 design
            Container(
              padding: const EdgeInsets.all(AppSpacing.cardPadding),
                 decoration: BoxDecoration(
                color: AppColors.cardSurface,
                borderRadius: BorderRadius.circular(AppRadii.card),
                border: Border.all(color: AppColors.warmMist),
              ),
              child: Row(
                children: [
                  Semantics(
                    label: 'profile_avatar'.tr(),
                    child: CircleAvatar(
                      radius: 28,
                      backgroundColor: AppColors.burgundy,
                      child: const Icon(
                        Icons.person,
                        size: 32,
                        color: AppColors.cardSurface,
                      ),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          profile.name.isNotEmpty ? profile.name : 'Namaste',
                          style: AppTextStyles.headlineMedium.copyWith(
                            fontSize: 18,
                            fontWeight: FontWeight.w700,
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 2),
                        Text(
                          profile.phone.isNotEmpty
                              ? profile.phone
                              : (authState.phoneNumber ?? 'no_phone'.tr()),
                           style: AppTextStyles.bodySmall.copyWith(
                            color: AppColors.taupe,
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        if (profile.craftType.isNotEmpty) ...[
                          const SizedBox(height: 6),
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 2,
                            ),
                            decoration: BoxDecoration(
                              color: AppColors.burgundyLight,
                              borderRadius: BorderRadius.circular(
                                AppRadii.chip,
                              ),
                              border: Border.all(
                                color: AppColors.burgundy,
                              ),
                            ),
                            child: Text(
                              profile.craftType,
                              style: AppTextStyles.labelSmall.copyWith(
                                color: AppColors.burgundy,
                                fontWeight: FontWeight.w600,
                                fontSize: 11,
                              ),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                        if (profile.state.isNotEmpty) ...[
                          const SizedBox(height: 4),
                          Text(
                            profile.state,
                            style: AppTextStyles.bodySmall.copyWith(
                              color: AppColors.taupe,
                              fontSize: 11,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                        if (profile.locationCluster.isNotEmpty) ...[
                          const SizedBox(height: 2),
                          Text(
                            profile.locationCluster,
                            style: AppTextStyles.bodySmall.copyWith(
                              color: AppColors.taupe,
                              fontSize: 11,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ],
                      ],
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.edit_outlined),
                    tooltip: 'edit_profile'.tr(),
                    onPressed: () => _showEditProfileDialog(context, ref, profile),
                  ),
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.md),

            // Accessibility settings
            const AccessibilityToggle(),

            const SizedBox(height: AppSpacing.md),

            // Menu items
            _MenuTile(
              icon: Icons.language,
              title: 'language_settings_title'.tr(),
              subtitle:
                  'lang_${EasyLocalization.of(context)?.locale.languageCode ?? 'en'}'
                      .tr(),
              onTap: () =>
                  context.pushNamed(AppRouteConstants.languageSettings),
            ),
            _MenuTile(
              icon: Icons.trending_up,
              title: 'my_stats_title'.tr(),
              subtitle: 'my_stats_subtitle'.tr(),
              onTap: () => context.pushNamed(AppRouteConstants.myStats),
            ),
            _MenuTile(
              icon: Icons.menu_book_rounded,
              title: 'tutorial_guide_menu'.tr(),
              subtitle: 'how_to_list_btn'.tr(),
              onTap: () => context.pushNamed(AppRouteConstants.listingTutorial),
            ),
            _MenuTile(
              icon: Icons.help_outline,
              title: 'help_support'.tr(),
              onTap: () {
                showAboutDialog(
                  context: context,
                  applicationName: 'Craftsy',
                  applicationVersion: '1.0.0',
                  applicationLegalese: 'about_desc'.tr(),
                );
              },
            ),
            _MenuTile(
              icon: Icons.info_outline,
              title: 'about_craftsy'.tr(),
              onTap: () {
                showDialog(
                  context: context,
                  builder: (ctx) => Dialog(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(AppRadii.dialog),
                    ),
                    backgroundColor: AppColors.cardSurface,
                    insetPadding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.screenPadding,
                      vertical: AppSpacing.lg,
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(AppSpacing.cardPadding),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Text(
                            'about_craftsy'.tr(),
                            style: AppTextStyles.headlineMedium.copyWith(
                              fontSize: 19,
                            ),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: AppSpacing.sm),
                          Text(
                            'about_desc'.tr(),
                            style: AppTextStyles.bodyMedium,
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: AppSpacing.lg),
                          AppButton(
                            label: 'close'.tr(),
                            onPressed: () => Navigator.pop(ctx),
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),

            const SizedBox(height: AppSpacing.xl),

            AppButton(
              label: 'sign_out'.tr(),
              type: AppButtonType.outlined,
              customColor: AppColors.error,
              icon: Icons.logout,
              onPressed: () async {
                showAppConfirmationDialog(
                  context: context,
                  title: 'sign_out_confirm_title'.tr(),
                  message: 'sign_out_confirm_msg'.tr(),
                  icon: Icons.logout_rounded,
                  confirmLabel: 'sign_out'.tr(),
                  confirmColor: AppColors.error,
                  isDestructive: true,
                  onConfirm: () async {
                    Navigator.of(context, rootNavigator: true).pop();
                    ref.read(selectedOrderFilterProvider.notifier).state =
                        OrderStatus.newOrder;
                    await ref.read(authStateProvider.notifier).signOut();
                    if (context.mounted) {
                      context.goNamed(AppRouteConstants.signIn);
                    }
                  },
                );
              },
            ),

            const SizedBox(height: AppSpacing.xl),
          ],
        ),
      ),
    );
  }
}

void _showEditProfileDialog(BuildContext context, WidgetRef ref, UserProfile profile) {
  final nameController = TextEditingController(text: profile.name);
  final craftController = TextEditingController(text: profile.craftType);
  final clusterController = TextEditingController(text: profile.locationCluster);
  final stateController = TextEditingController(text: profile.state);
  final experienceController = TextEditingController(text: profile.experienceYears ?? '');
  final pehchanController = TextEditingController(text: profile.pehchanId ?? '');
  final formKey = GlobalKey<FormState>();

  showDialog(
    context: context,
    builder: (ctx) => AlertDialog(
      title: Text('edit_profile'.tr()),
      content: Form(
        key: formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: nameController,
                decoration: InputDecoration(
                  labelText: 'full_name_label'.tr(),
                  hintText: 'full_name_hint'.tr(),
                ),
              ),
              const SizedBox(height: AppSpacing.md),
              TextFormField(
                controller: craftController,
                decoration: InputDecoration(
                  labelText: 'craft_type_label'.tr(),
                  hintText: 'craft_type_hint'.tr(),
                ),
              ),
              const SizedBox(height: AppSpacing.md),
              TextFormField(
                controller: clusterController,
                decoration: InputDecoration(
                  labelText: 'cluster_location_label'.tr(),
                  hintText: 'cluster_location_hint'.tr(),
                ),
              ),
              const SizedBox(height: AppSpacing.md),
              TextFormField(
                controller: stateController,
                decoration: InputDecoration(
                  labelText: 'state_label'.tr(),
                  hintText: 'state_hint'.tr(),
                ),
              ),
              const SizedBox(height: AppSpacing.md),
              TextFormField(
                controller: experienceController,
                decoration: InputDecoration(
                  labelText: 'experience_label'.tr(),
                  hintText: 'experience_hint'.tr(),
                ),
              ),
              const SizedBox(height: AppSpacing.md),
              TextFormField(
                controller: pehchanController,
                decoration: InputDecoration(
                  labelText: 'pehchan_id_label'.tr(),
                  hintText: 'pehchan_id_hint'.tr(),
                ),
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(ctx),
          child: Text('cancel_btn'.tr()),
        ),
        FilledButton(
          onPressed: () async {
            final form = formKey.currentState;
            if (form == null || !form.validate()) return;
            final updated = profile.copyWith(
              name: nameController.text.trim(),
              craftType: craftController.text.trim(),
              locationCluster: clusterController.text.trim(),
              state: stateController.text.trim(),
              experienceYears: experienceController.text.trim().isEmpty
                  ? null
                  : experienceController.text.trim(),
              pehchanId: pehchanController.text.trim().isEmpty
                  ? null
                  : pehchanController.text.trim(),
            );
            final result = await ref.read(authStateProvider.notifier).updateProfile(updated);
            if (context.mounted) {
              Navigator.pop(ctx);
              if (result != null) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('profile_updated'.tr())),
                );
              }
            }
          },
          child: Text('save_btn'.tr()),
        ),
      ],
    ),
  );
}

class _MenuTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? subtitle;
  final VoidCallback onTap;

  const _MenuTile({
    required this.icon,
    required this.title,
    this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      button: true,
      label: title,
      child: Card(
        margin: const EdgeInsets.only(bottom: AppSpacing.sm),
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.card),
          side: const BorderSide(color: AppColors.warmMist),
        ),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(AppRadii.card),
          child: Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.md,
              vertical: AppSpacing.sm,
            ),
            child: Row(
              children: [
                Icon(icon, color: AppColors.burgundy, size: 24),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(title, style: AppTextStyles.bodyMedium),
                      if (subtitle != null) ...[
                        const SizedBox(height: 2),
                        Text(
                          subtitle!,
                           style: AppTextStyles.bodySmall.copyWith(
                            color: AppColors.taupe,
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ],
                  ),
                ),
                const Icon(Icons.chevron_right, color: AppColors.taupe),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
