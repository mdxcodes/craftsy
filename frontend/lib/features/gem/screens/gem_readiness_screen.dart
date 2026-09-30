import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/primary_action_button.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../services/gem_api_service.dart';

class GemReadinessScreen extends ConsumerStatefulWidget {
  final String productId;

  const GemReadinessScreen({super.key, required this.productId});

  @override
  ConsumerState<GemReadinessScreen> createState() => _GemReadinessScreenState();
}

class _GemReadinessScreenState extends ConsumerState<GemReadinessScreen> {
  bool _isLoading = true;
  Map<String, dynamic>? _readiness;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadReadiness();
  }

  Future<void> _loadReadiness() async {
    try {
      final api = ref.read(gemApiServiceProvider);
      final data = await api.getReadiness(widget.productId);
      setState(() {
        _readiness = data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'gem_readiness_title'.tr(),
      body: SafeArea(
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : _error != null
                ? _buildError()
                : _buildReadiness(),
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
            PrimaryActionButton(label: 'retry'.tr(), onPressed: _loadReadiness),
          ],
        ),
      ),
    );
  }

  Widget _buildReadiness() {
    final ready = _readiness?['ready'] as bool? ?? false;
    final missing = (_readiness?['missing_fields'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList() ??
        [];
    final warnings = (_readiness?['warnings'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList() ??
        [];
    final available = (_readiness?['available_fields'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList() ??
        [];
    final nextActions = (_readiness?['next_actions'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList() ??
        [];

    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(AppSpacing.cardPadding),
            decoration: BoxDecoration(
              color: ready ? AppColors.sage.withValues(alpha: 0.1) : AppColors.warmMist,
              borderRadius: BorderRadius.circular(AppRadii.card),
              border: Border.all(
                color: ready ? AppColors.sage.withValues(alpha: 0.3) : AppColors.line,
              ),
            ),
            child: Row(
              children: [
                Icon(
                  ready ? Icons.check_circle : Icons.info,
                  color: ready ? AppColors.sage : AppColors.sienna,
                ),
                const SizedBox(width: AppSpacing.sm),
                Text(
                  ready ? 'gem_ready_status'.tr() : 'gem_not_ready_status'.tr(),
                  style: AppTextStyles.labelLarge,
                ),
              ],
            ),
          ),
          const SizedBox(height: AppSpacing.lg),

          if (missing.isNotEmpty) ...[
            _buildSection('gem_missing_fields'.tr(), missing, AppColors.sienna),
            const SizedBox(height: AppSpacing.md),
          ],
          if (warnings.isNotEmpty) ...[
            _buildSection('gem_warnings'.tr(), warnings, AppColors.sienna),
            const SizedBox(height: AppSpacing.md),
          ],
          if (available.isNotEmpty) ...[
            _buildSection('gem_available_fields'.tr(), available, AppColors.sage),
            const SizedBox(height: AppSpacing.md),
          ],
          if (nextActions.isNotEmpty) ...[
            _buildSection('gem_next_actions'.tr(), nextActions, AppColors.textPrimary),
            const SizedBox(height: AppSpacing.md),
          ],

          const SizedBox(height: AppSpacing.xl),
          if (missing.isEmpty)
            PrimaryActionButton(
              label: 'gem_open_gem'.tr(),
              onPressed: () async {
                try {
                  final api = ref.read(gemApiServiceProvider);
                  await api.openGemPortal(widget.productId);
                  if (mounted) {
                    _openUrl('https://www.gem.gov.in/');
                  }
                } catch (e) {
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('gem_error'.tr())),
                    );
                  }
                }
              },
            )
          else
            PrimaryActionButton(
              label: 'gem_add_missing_info'.tr(),
              onPressed: () {
                  context.push('/gem/listing-review/${widget.productId}');
              },
            ),
        ],
      ),
    );
  }

  Widget _buildSection(String title, List<String> items, Color color) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: AppTextStyles.labelLarge.copyWith(color: color)),
        const SizedBox(height: AppSpacing.xs),
        ...items.map((item) => Padding(
              padding: const EdgeInsets.symmetric(vertical: 2),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.circle, size: 6, color: color),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(child: Text(item, style: AppTextStyles.bodySmall)),
                ],
              ),
            )),
      ],
    );
  }

  Future<void> _openUrl(String url) async {
    try {
      // Use url_launcher if available
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Could not open link: $url')),
        );
      }
    }
  }
}
