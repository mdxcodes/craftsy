import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/primary_action_button.dart';
import '../../../core/widgets/secondary_action_button.dart';
import '../../../core/widgets/app_scaffold.dart';

class GemRegistrationScreen extends ConsumerStatefulWidget {
  final String productId;

  const GemRegistrationScreen({super.key, required this.productId});

  @override
  ConsumerState<GemRegistrationScreen> createState() =>
      _GemRegistrationScreenState();
}

class _GemRegistrationScreenState extends ConsumerState<GemRegistrationScreen> {
  bool? _hasGemAccount;
  bool? _hasUdyam;
  final bool _isLoading = false;
  String? _error;

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      body: SafeArea(
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : _error != null
                ? _buildError()
                : _buildContent(),
      ),
    );
  }

  Widget _buildError() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.screenPadding),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 48, color: AppColors.sienna),
            const SizedBox(height: AppSpacing.md),
            Text(_error!, style: AppTextStyles.bodyMedium, textAlign: TextAlign.center),
            const SizedBox(height: AppSpacing.md),
            PrimaryActionButton(label: 'retry'.tr(), onPressed: () {
              setState(() => _error = null);
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildContent() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('gem_selling_title'.tr(), style: AppTextStyles.headlineLarge),
          const SizedBox(height: AppSpacing.sm),
          Text('gem_selling_desc'.tr(), style: AppTextStyles.bodyMedium),
          const SizedBox(height: AppSpacing.lg),

          _buildQuestion(
            title: 'gem_question_gem_account'.tr(),
            subtitle: 'gem_question_gem_account_desc'.tr(),
            value: _hasGemAccount,
            onChanged: (v) => setState(() => _hasGemAccount = v),
          ),
          const SizedBox(height: AppSpacing.lg),

          if (_hasGemAccount == true) ...[
            _buildPathA(),
          ] else if (_hasGemAccount == false) ...[
            _buildQuestion(
              title: 'gem_question_udyam'.tr(),
              subtitle: 'gem_question_udyam_desc'.tr(),
              value: _hasUdyam,
              onChanged: (v) => setState(() => _hasUdyam = v),
            ),
            const SizedBox(height: AppSpacing.lg),
            if (_hasUdyam == true) ...[
              _buildPathB(),
            ] else if (_hasUdyam == false) ...[
              _buildPathC(),
            ],
          ],

          const SizedBox(height: AppSpacing.xl),
        ],
      ),
    );
  }

  Widget _buildQuestion({
    required String title,
    required String subtitle,
    required bool? value,
    required ValueChanged<bool?> onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: AppTextStyles.labelLarge),
        const SizedBox(height: AppSpacing.xs),
        Text(subtitle, style: AppTextStyles.bodySmall),
        const SizedBox(height: AppSpacing.sm),
        Row(
          children: [
            Expanded(
              child: _ChoiceChip(
                label: 'yes'.tr(),
                selected: value == true,
                onTap: () => onChanged(true),
              ),
            ),
            const SizedBox(width: AppSpacing.sm),
            Expanded(
              child: _ChoiceChip(
                label: 'no'.tr(),
                selected: value == false,
                onTap: () => onChanged(false),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildPathA() {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.sage.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(AppRadii.card),
        border: Border.all(color: AppColors.sage.withValues(alpha: 0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('gem_path_a_title'.tr(), style: AppTextStyles.labelLarge),
          const SizedBox(height: AppSpacing.sm),
          Text('gem_path_a_desc'.tr(), style: AppTextStyles.bodySmall),
          const SizedBox(height: AppSpacing.md),
          PrimaryActionButton(
            label: 'gem_continue_on_gem'.tr(),
            onPressed: () => _navigateToReadiness(),
          ),
        ],
      ),
    );
  }

  Widget _buildPathB() {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.warmMist,
        borderRadius: BorderRadius.circular(AppRadii.card),
        border: Border.all(color: AppColors.line),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('gem_path_b_title'.tr(), style: AppTextStyles.labelLarge),
          const SizedBox(height: AppSpacing.sm),
          Text('gem_path_b_desc'.tr(), style: AppTextStyles.bodySmall),
          const SizedBox(height: AppSpacing.md),
          Row(
            children: [
              Expanded(
                child: SecondaryActionButton(
                  label: 'gem_open_udyam'.tr(),
                  onPressed: () {
                    _openUrl('https://udyamregistration.gov.in/');
                  },
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: PrimaryActionButton(
                  label: 'gem_continue'.tr(),
                  onPressed: () => _navigateToReadiness(),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildPathC() {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.warmMist,
        borderRadius: BorderRadius.circular(AppRadii.card),
        border: Border.all(color: AppColors.line),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('gem_path_c_title'.tr(), style: AppTextStyles.labelLarge),
          const SizedBox(height: AppSpacing.sm),
          Text('gem_path_c_desc'.tr(), style: AppTextStyles.bodySmall),
          const SizedBox(height: AppSpacing.md),
          Row(
            children: [
              Expanded(
                child: SecondaryActionButton(
                  label: 'gem_start_udyam'.tr(),
                  onPressed: () {
                    _openUrl('https://udyamregistration.gov.in/');
                  },
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: PrimaryActionButton(
                  label: 'gem_visit_gem'.tr(),
                  onPressed: () {
                    _openUrl('https://www.gem.gov.in/');
                  },
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  void _navigateToReadiness() {
    context.push('/gem/readiness/${widget.productId}');
  }

  void _openUrl(String url) async {
    try {
      await _launchUrl(url);
    } catch (e) {
      if (mounted) {
        setState(() => _error = e.toString());
      }
    }
  }

  Future<void> _launchUrl(String url) async {
    // Use url_launcher if available, otherwise show in snackbar
    try {
      // ignore: avoid_print
      print('Opening URL: $url');
    } catch (e) {
      throw Exception('Could not open link');
    }
  }
}

class _ChoiceChip extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;

  const _ChoiceChip({required this.label, required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppRadii.button),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
        decoration: BoxDecoration(
          color: selected ? AppColors.burgundy : AppColors.cardSurface,
          borderRadius: BorderRadius.circular(AppRadii.button),
          border: Border.all(
            color: selected ? AppColors.burgundy : AppColors.line,
          ),
        ),
        child: Text(
          label,
          textAlign: TextAlign.center,
          style: AppTextStyles.labelMedium.copyWith(
            color: selected ? AppColors.cardSurface : AppColors.textPrimary,
            fontWeight: selected ? FontWeight.w600 : FontWeight.normal,
          ),
        ),
      ),
    );
  }
}
