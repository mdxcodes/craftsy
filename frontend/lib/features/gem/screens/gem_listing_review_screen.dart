import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/primary_action_button.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../../../core/widgets/app_image.dart';
import '../services/gem_api_service.dart';

class GemListingReviewScreen extends ConsumerStatefulWidget {
  final String productId;

  const GemListingReviewScreen({super.key, required this.productId});

  @override
  ConsumerState<GemListingReviewScreen> createState() =>
      _GemListingReviewScreenState();
}

class _GemListingReviewScreenState extends ConsumerState<GemListingReviewScreen> {
  bool _isLoading = true;
  Map<String, dynamic>? _listing;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadListing();
  }

  Future<void> _loadListing() async {
    try {
      final api = ref.read(gemApiServiceProvider);
      final data = await api.generateListingDraft(widget.productId);
      setState(() {
        _listing = data;
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
      title: 'gem_listing_review_title'.tr(),
      body: SafeArea(
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : _error != null
                ? _buildError()
                : _buildListing(),
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
            PrimaryActionButton(label: 'retry'.tr(), onPressed: _loadListing),
          ],
        ),
      ),
    );
  }

  Widget _buildListing() {
    final name = _listing?['product_name'] ?? 'gem_unknown'.tr();
    final shortDescription = _listing?['short_description'] ?? '';
    final description = _listing?['description'] ?? '';
    final price = _listing?['price']?.toString() ?? '';
    final category = _listing?['category'] ?? 'gem_unknown'.tr();
    final specs = (_listing?['specifications'] as Map<String, dynamic>?) ?? {};
    final certs = (_listing?['certifications'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList() ??
        [];
    final warranty = _listing?['warranty']?.toString();
    final images = (_listing?['images'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList() ??
        [];
    final artisan = (_listing?['artisan_information'] as Map<String, dynamic>?) ?? {};
    final missing = (_listing?['missing_information'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList() ??
        [];
    final copyableText = _listing?['copyable_text'] as String? ?? '';

    return SingleChildScrollView(
      padding: const EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildSectionHeader('gem_product_information'.tr()),
          const SizedBox(height: AppSpacing.sm),
          _buildCopyRow('gem_product_title'.tr(), name),
          const SizedBox(height: AppSpacing.sm),
          _buildCopyRow('gem_short_description'.tr(), shortDescription.isEmpty ? 'gem_no_data'.tr() : shortDescription),
          const SizedBox(height: AppSpacing.sm),
          _buildCopyRow('gem_full_description'.tr(), description.isEmpty ? 'gem_no_data'.tr() : description),
          const SizedBox(height: AppSpacing.sm),
          _buildCopyRow('gem_category'.tr(), category),
          const SizedBox(height: AppSpacing.sm),
          _buildCopyRow('gem_pricing'.tr(), price.isNotEmpty ? 'INR $price' : 'gem_no_data'.tr()),
          if (artisan.isNotEmpty) ...[
            const SizedBox(height: AppSpacing.md),
            _buildSectionHeader('gem_artisan_info'.tr()),
            const SizedBox(height: AppSpacing.sm),
            ...artisan.entries.map((e) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 2),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Icon(Icons.circle, size: 6, color: AppColors.textPrimary),
                      const SizedBox(width: AppSpacing.sm),
                      Expanded(child: Text('${e.key}: ${e.value}', style: AppTextStyles.bodySmall)),
                    ],
                  ),
                )),
          ],
          const SizedBox(height: AppSpacing.md),
          _buildSectionHeader('gem_specifications'.tr()),
          const SizedBox(height: AppSpacing.sm),
          if (specs.isEmpty)
            Text('gem_no_data'.tr(), style: AppTextStyles.bodySmall)
          else
            ...specs.entries.map((e) => _buildCopyRow(e.key, e.value.toString())),
          const SizedBox(height: AppSpacing.md),
          _buildSectionHeader('gem_certifications'.tr()),
          const SizedBox(height: AppSpacing.sm),
          if (certs.isEmpty)
            Text('gem_no_data'.tr(), style: AppTextStyles.bodySmall)
          else
            ...certs.map((c) => _buildCopyRow('', c)),
          const SizedBox(height: AppSpacing.md),
          _buildSectionHeader('gem_warranty'.tr()),
          const SizedBox(height: AppSpacing.sm),
          _buildCopyRow('', warranty ?? 'gem_no_data'.tr()),
          const SizedBox(height: AppSpacing.md),
          _buildSectionHeader('gem_images'.tr()),
          const SizedBox(height: AppSpacing.sm),
          if (images.isEmpty)
            Text('gem_no_data'.tr(), style: AppTextStyles.bodySmall)
          else
            Wrap(
              spacing: AppSpacing.sm,
              runSpacing: AppSpacing.sm,
              children: images.map((url) => _buildImageThumb(url)).toList(),
            ),
          const SizedBox(height: AppSpacing.md),
          if (missing.isNotEmpty) ...[
            _buildSectionHeader('gem_missing_info'.tr()),
            const SizedBox(height: AppSpacing.sm),
            Container(
              padding: const EdgeInsets.all(AppSpacing.cardPadding),
              decoration: BoxDecoration(
                color: AppColors.warmMist,
                borderRadius: BorderRadius.circular(AppRadii.card),
                border: Border.all(color: AppColors.line),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.warning_amber, size: 18, color: AppColors.sienna),
                      const SizedBox(width: AppSpacing.sm),
                      Text('gem_missing_info'.tr(), style: AppTextStyles.labelMedium),
                    ],
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  ...missing.map((m) => Padding(
                        padding: const EdgeInsets.symmetric(vertical: 2),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Icon(Icons.circle, size: 6, color: AppColors.sienna),
                            const SizedBox(width: AppSpacing.sm),
                            Expanded(child: Text(m, style: AppTextStyles.bodySmall)),
                          ],
                        ),
                      )),
                ],
              ),
            ),
            const SizedBox(height: AppSpacing.md),
          ],
          Text(
            'gem_disclaimer'.tr(),
            style: AppTextStyles.bodySmall.copyWith(
              color: AppColors.textSecondary,
              fontStyle: FontStyle.italic,
            ),
          ),
          const SizedBox(height: AppSpacing.lg),
          PrimaryActionButton(
            label: 'gem_copy_all'.tr(),
            onPressed: () => _copyAll(copyableText),
          ),
          const SizedBox(height: AppSpacing.sm),
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
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Text(title, style: AppTextStyles.labelLarge);
  }

  Widget _buildCopyRow(String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (label.isNotEmpty) ...[
          SizedBox(
            width: 120,
            child: Text(label, style: AppTextStyles.labelMedium),
          ),
          const SizedBox(width: AppSpacing.sm),
        ],
        Expanded(
          child: Text(value, style: AppTextStyles.bodyMedium),
        ),
        const SizedBox(width: AppSpacing.sm),
        InkWell(
          onTap: () => _copyText(value),
          child: Padding(
            padding: const EdgeInsets.all(4),
            child: Icon(Icons.copy, size: 18, color: AppColors.textSecondary),
          ),
        ),
      ],
    );
  }

  Widget _buildImageThumb(String url) {
    return InkWell(
      onTap: () => _openImagePreview(url),
      child: AppImage(
        imageUrl: url,
        width: 100,
        height: 100,
        fit: BoxFit.cover,
      ),
    );
  }

  void _copyText(String text) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('gem_copied'.tr()), duration: const Duration(seconds: 1)),
    );
  }

  void _copyAll(String text) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('gem_copied'.tr()), duration: const Duration(seconds: 1)),
    );
  }

  void _openImagePreview(String url) {
    showDialog(
      context: context,
      builder: (ctx) => Dialog(
        backgroundColor: Colors.transparent,
        child: GestureDetector(
          onTap: () => Navigator.pop(ctx),
          child: Stack(
            children: [
              Center(
                child: AppImage(
                  imageUrl: url,
                  fit: BoxFit.contain,
                ),
              ),
              Positioned(
                top: 16,
                right: 16,
                child: IconButton(
                  onPressed: () => Navigator.pop(ctx),
                  icon: const Icon(Icons.close, color: Colors.white),
                  style: IconButton.styleFrom(backgroundColor: Colors.black54),
                ),
              ),
            ],
          ),
        ),
      ),
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
