import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/router/app_route_constants.dart';
import '../../../core/widgets/app_button.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../providers/auth_provider.dart';
import '../../../core/widgets/language_picker.dart';

class NgoAuthScreen extends ConsumerStatefulWidget {
  const NgoAuthScreen({super.key});

  @override
  ConsumerState<NgoAuthScreen> createState() => _NgoAuthScreenState();
}

class _NgoAuthScreenState extends ConsumerState<NgoAuthScreen> {
  final _coordinatorIdController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  bool _isSubmitting = false;

  @override
  void dispose() {
    _coordinatorIdController.dispose();
    super.dispose();
  }

  Future<void> _handleAssistedSignIn() async {
    if (!(_formKey.currentState?.validate() ?? false)) return;
    setState(() => _isSubmitting = true);
    final coordinatorId = _coordinatorIdController.text.trim();

    await ref
        .read(authStateProvider.notifier)
        .signInWithCoordinator(coordinatorId);

    if (mounted) {
      setState(() => _isSubmitting = false);
      context.goNamed(AppRouteConstants.home);
    }
  }

  @override
  Widget build(BuildContext context) {
    final screenPadding = AppSpacing.getScreenPadding(context);

    return AppScaffold(
      showConnectivityPill: false,
      showBackgroundPattern: false,
      rawAppBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded),
          onPressed: () => context.pop(),
        ),
        actions: const [
          Padding(
            padding: EdgeInsets.only(right: AppSpacing.sm),
            child: LanguagePicker(),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(screenPadding),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: AppSpacing.sm),
            Center(
              child: Container(
                width: 64,
                height: 64,
                decoration: BoxDecoration(
                  color: AppColors.goldLight,
                  borderRadius: BorderRadius.circular(AppRadii.lg),
                ),
                child: const Center(
                  child: Icon(
                    Icons.support_agent_rounded,
                    size: 36,
                    color: AppColors.goldDark,
                  ),
                ),
              ),
            ),
            const SizedBox(height: AppSpacing.md),
            Text(
              'ngo_assist_title'.tr(),
              style: AppTextStyles.headlineLarge,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: AppSpacing.sm),
            Text(
              'ngo_assist_description'.tr(),
              style: AppTextStyles.bodyMedium.copyWith(
                color: AppColors.warmGray,
                height: 1.5,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: AppSpacing.lg),

            Center(
              child: Container(
                height: 210,
                width: 210,
                alignment: Alignment.center,
                decoration: BoxDecoration(
                  color: AppColors.cardSurface,
                  borderRadius: BorderRadius.circular(AppRadii.card),
                  border: Border.all(color: AppColors.warmMist, width: 1.5),
                  boxShadow: AppElevation.cardShadow,
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.qr_code_2_rounded,
                      size: 100,
                      color: AppColors.espresso,
                    ),
                    const SizedBox(height: AppSpacing.xs),
                    Padding(
                      padding: const EdgeInsets.symmetric(
                        horizontal: AppSpacing.sm,
                      ),
                      child: Text(
                        'qr_placeholder_label'.tr(),
                        style: AppTextStyles.labelSmall.copyWith(
                          color: AppColors.warmGray,
                          fontWeight: FontWeight.w600,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: AppSpacing.md),

            Container(
              padding: const EdgeInsets.symmetric(
                horizontal: AppSpacing.md,
                vertical: AppSpacing.sm + 2,
              ),
              decoration: BoxDecoration(
                color: AppColors.goldLight,
                borderRadius: BorderRadius.circular(AppRadii.card),
                border: Border.all(
                  color: AppColors.gold.withValues(alpha: 0.35),
                ),
              ),
              child: Row(
                children: [
                  const Icon(
                    Icons.info_outline_rounded,
                    size: 20,
                    color: AppColors.goldDark,
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: Text(
                      'ngo_assist_explanation'.tr(),
                      style: AppTextStyles.bodySmall.copyWith(
                        color: AppColors.espresso,
                        fontWeight: FontWeight.w600,
                        height: 1.4,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.lg),

            Row(
              children: [
                Expanded(
                  child: Divider(
                    color: AppColors.warmMist,
                    thickness: 1,
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.md,
                  ),
                  child: Text(
                    'or_enter_coordinator_id'.tr(),
                    style: AppTextStyles.labelSmall.copyWith(
                      color: AppColors.warmGray,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                Expanded(
                  child: Divider(
                    color: AppColors.warmMist,
                    thickness: 1,
                  ),
                ),
              ],
            ),

            const SizedBox(height: AppSpacing.md),

            Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  TextFormField(
                    controller: _coordinatorIdController,
                    style: AppTextStyles.bodyMedium.copyWith(
                      color: AppColors.espresso,
                    ),
                    decoration: InputDecoration(
                      labelText: 'coordinator_id_label'.tr(),
                      hintText: 'coordinator_id_hint'.tr(),
                      labelStyle: AppTextStyles.bodyMedium.copyWith(
                        color: AppColors.warmGray,
                      ),
                      hintStyle: AppTextStyles.bodyMedium.copyWith(
                        color: AppColors.taupe,
                      ),
                      prefixIcon: const Icon(
                        Icons.badge_outlined,
                        color: AppColors.burgundy,
                      ),
                      filled: true,
                      fillColor: AppColors.cardSurface,
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 14,
                      ),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(AppRadii.button),
                        borderSide: BorderSide(color: AppColors.warmMist, width: 1.5),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(AppRadii.button),
                        borderSide: BorderSide(color: AppColors.warmMist, width: 1.5),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(AppRadii.button),
                        borderSide: BorderSide(color: AppColors.burgundy, width: 2),
                      ),
                    ),
                    validator: (value) {
                      if (value == null || value.trim().isEmpty) {
                        return 'coordinator_id_required'.tr();
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.xs,
                    ),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Icon(
                          Icons.info_outline_rounded,
                          size: 14,
                          color: AppColors.warmGray,
                        ),
                        const SizedBox(width: AppSpacing.xs),
                        Expanded(
                          child: Text(
                            'ngo_assist_explained'.tr(),
                            style: AppTextStyles.bodySmall.copyWith(
                              color: AppColors.warmGray,
                              fontSize: 12,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.lg),

            AppButton(
              label: 'start_assisted_signin_btn'.tr(),
              icon: Icons.how_to_reg_rounded,
              isLoading: _isSubmitting,
              onPressed: _handleAssistedSignIn,
            ),

            const SizedBox(height: AppSpacing.xl),
          ],
        ),
      ),
    );
  }
}
