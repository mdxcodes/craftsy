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
import '../../../core/providers/app_providers.dart';
import '../providers/auth_provider.dart';

class OtpScreen extends ConsumerStatefulWidget {
  final String phoneNumber;
  final bool isNewUser;

  const OtpScreen({
    super.key,
    required this.phoneNumber,
    this.isNewUser = false,
  });

  @override
  ConsumerState<OtpScreen> createState() => _OtpScreenState();
}

class _OtpScreenState extends ConsumerState<OtpScreen> {
  final List<TextEditingController> _controllers = List.generate(
    6,
    (_) => TextEditingController(),
  );
  final List<FocusNode> _focusNodes = List.generate(6, (_) => FocusNode());

  @override
  void dispose() {
    for (var controller in _controllers) {
      controller.dispose();
    }
    for (var node in _focusNodes) {
      node.dispose();
    }
    super.dispose();
  }

  void _handleOtpComplete() async {
    final otp = _controllers.map((c) => c.text).join();
    if (otp.isEmpty) {
      return;
    }
    final notifier = ref.read(authStateProvider.notifier);
    await notifier.verifyOtp(
      widget.phoneNumber.isEmpty ? '9876543210' : widget.phoneNumber,
      otp,
    );
    await ref.read(userProfileProvider.notifier).reloadProfile();
    if (mounted && ref.read(authStateProvider).isAuthenticated) {
      context.goNamed(AppRouteConstants.home);
    }
  }

  Future<void> _handleResendOtp() async {
    final authState = ref.read(authStateProvider);
    if (authState.resendCooldownSeconds != null && authState.resendCooldownSeconds! > 0) {
      return;
    }
    final notifier = ref.read(authStateProvider.notifier);
    await notifier.resendOtp(
      widget.phoneNumber.isEmpty ? '9876543210' : widget.phoneNumber,
    );
    if (mounted) {
      final result = ref.read(authStateProvider);
      if (result.errorMessage == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'otp_resent'.tr(),
              style: AppTextStyles.bodySmall.copyWith(
                color: AppColors.textOnPrimary,
              ),
            ),
            backgroundColor: AppColors.teal,
            behavior: SnackBarBehavior.floating,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(AppRadii.md),
            ),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authStateProvider);
    final cooldown = authState.resendCooldownSeconds ?? 0;

    return AppScaffold(
      rawAppBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            if (context.canPop()) {
              context.pop();
            } else if (widget.isNewUser) {
              context.goNamed(AppRouteConstants.register);
            } else {
              context.goNamed(AppRouteConstants.signIn);
            }
          },
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppSpacing.screenPadding),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: AppSpacing.lg),
            Text(
              'verify_phone_title'.tr(),
              style: AppTextStyles.displayMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: AppSpacing.sm),
            Text(
              widget.isNewUser
                  ? 'verify_phone_subtitle_new'.tr()
                  : 'verify_phone_subtitle'.tr(),
              style: AppTextStyles.bodyMedium.copyWith(
                color: AppColors.textSecondary,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: AppSpacing.xxl),

            if (authState.errorMessage != null)
              Container(
                padding: const EdgeInsets.all(AppSpacing.md),
                decoration: BoxDecoration(
                  color: AppColors.coralLight,
                  borderRadius: BorderRadius.circular(AppRadii.md),
                  border: Border.all(color: AppColors.error, width: 1),
                ),
                child: Text(
                  authState.errorMessage!,
                  style: AppTextStyles.bodySmall.copyWith(
                    color: AppColors.coralDark,
                    fontWeight: FontWeight.w600,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
            if (authState.errorMessage != null)
              const SizedBox(height: AppSpacing.md),

            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: List.generate(6, (index) {
                return SizedBox(
                  width: 48,
                  height: 56,
                  child: TextField(
                    controller: _controllers[index],
                    focusNode: _focusNodes[index],
                    keyboardType: TextInputType.number,
                    textAlign: TextAlign.center,
                    maxLength: 1,
                    style: AppTextStyles.headlineLarge,
                    decoration: InputDecoration(
                      counterText: '',
                      contentPadding: EdgeInsets.zero,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(AppRadii.md),
                      ),
                    ),
                    onChanged: (value) {
                      if (value.isNotEmpty && index < 5) {
                        _focusNodes[index + 1].requestFocus();
                      } else if (value.isEmpty && index > 0) {
                        _focusNodes[index - 1].requestFocus();
                      }
                      if (index == 5 && value.isNotEmpty) {
                        _handleOtpComplete();
                      }
                    },
                  ),
                );
              }),
            ),

            const SizedBox(height: AppSpacing.xl),

            AppButton(
              label: 'verify_btn'.tr(),
              onPressed: _handleOtpComplete,
              isLoading: authState.isLoading,
            ),

            const SizedBox(height: AppSpacing.md),

            TextButton(
              onPressed: cooldown > 0 ? null : _handleResendOtp,
              child: Text(
                cooldown > 0
                    ? 'resend_otp_cooldown'.tr(args: [cooldown.toString()])
                    : 'resend_otp'.tr(),
              ),
            ),

            const SizedBox(height: AppSpacing.xxl),
          ],
        ),
      ),
    );
  }
}
