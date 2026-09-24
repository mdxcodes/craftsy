import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/widgets/primary_action_button.dart';
import '../../../core/widgets/secondary_action_button.dart';

class _GemStep {
  final String titleKey;
  final String descKey;
  final IconData icon;

  const _GemStep({
    required this.titleKey,
    required this.descKey,
    required this.icon,
  });
}

/// Government Selling Assistant screen.
///
/// This is an ASSISTED workflow — NOT a direct GeM API integration.
/// It guides the artisan through the process of preparing for GeM
/// and provides clear information about what is needed.
class GovernmentSellingScreen extends ConsumerStatefulWidget {
  final String? productId;

  const GovernmentSellingScreen({super.key, this.productId});

  @override
  ConsumerState<GovernmentSellingScreen> createState() =>
      _GovernmentSellingScreenState();
}

class _GovernmentSellingScreenState
    extends ConsumerState<GovernmentSellingScreen> {
  int _currentStep = 0;
  final bool _isLoading = false;

  final List<_GemStep> _steps = const [
    _GemStep(
      titleKey: 'gem_eligibility_check',
      descKey: 'gem_eligibility_desc',
      icon: Icons.fact_check_outlined,
    ),
    _GemStep(
      titleKey: 'gem_prepare_documents',
      descKey: 'gem_documents_required',
      icon: Icons.description_outlined,
    ),
    _GemStep(
      titleKey: 'gem_product_catalogue',
      descKey: 'gem_product_info',
      icon: Icons.inventory_2_outlined,
    ),
    _GemStep(
      titleKey: 'gem_review_and_submit',
      descKey: 'gem_ready_for_submission',
      icon: Icons.fact_check,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('gem_selling_title'.tr()),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: Column(
        children: [
          // Info banner
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            color: AppColors.amber.withValues(alpha: 0.1),
            child: Row(
              children: [
                const Icon(Icons.info_outline, color: AppColors.amber),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'gem_info_banner'.tr(),
                    style: TextStyle(fontSize: 13, color: AppColors.amberDark),
                  ),
                ),
              ],
            ),
          ),

          // Stepper
          Padding(padding: const EdgeInsets.all(24), child: _buildStepper()),

          // Step content
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: _buildStepContent(),
            ),
          ),

          // Bottom actions
          Container(
            padding: const EdgeInsets.all(24),
            child: Row(
              children: [
                if (_currentStep > 0)
                  Expanded(
                    child: SecondaryActionButton(
                      label: 'gem_back'.tr(),
                      onPressed: () {
                        setState(() {
                          _currentStep--;
                        });
                      },
                    ),
                  ),
                if (_currentStep > 0) const SizedBox(width: 16),
                Expanded(
                  child: PrimaryActionButton(
                    label: _currentStep < _steps.length - 1
                        ? 'gem_continue'.tr()
                        : 'gem_review_submit'.tr(),
                    onPressed: _isLoading ? null : _handleNext,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStepper() {
    return Row(
      children: List.generate(_steps.length, (index) {
        final isActive = index == _currentStep;
        final isCompleted = index < _currentStep;

        return Expanded(
          child: Row(
            children: [
              Container(
                width: 32,
                height: 32,
                decoration: BoxDecoration(
                  color: isCompleted
                      ? AppColors.success
                      : isActive
                      ? AppColors.indigo
                      : AppColors.inkFaint.withValues(alpha: 0.2),
                  shape: BoxShape.circle,
                ),
                child: Center(
                  child: isCompleted
                      ? const Icon(Icons.check, size: 18, color: Colors.white)
                      : Text(
                          '${index + 1}',
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                            color: isActive ? Colors.white : AppColors.inkSoft,
                          ),
                        ),
                ),
              ),
              if (index < _steps.length - 1)
                Expanded(
                  child: Container(
                    height: 2,
                    color: index < _currentStep
                        ? AppColors.success
                        : AppColors.inkFaint.withValues(alpha: 0.2),
                  ),
                ),
            ],
          ),
        );
      }),
    );
  }

  Widget _buildStepContent() {
    final step = _steps[_currentStep];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: AppColors.indigo.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(step.icon, size: 28, color: AppColors.indigo),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                step.titleKey.tr(),
                style: Theme.of(
                  context,
                ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w600),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Text(
          step.descKey.tr(),
          style: Theme.of(
            context,
          ).textTheme.bodyMedium?.copyWith(color: AppColors.textSecondary),
        ),
        const SizedBox(height: 24),
        ..._buildStepSpecificContent(),
      ],
    );
  }

  List<Widget> _buildStepSpecificContent() {
    switch (_currentStep) {
      case 0:
        return _buildEligibilityContent();
      case 1:
        return _buildDocumentsContent();
      case 2:
        return _buildProductCatalogueContent();
      case 3:
        return _buildReviewContent();
      default:
        return [];
    }
  }

  List<Widget> _buildEligibilityContent() {
    return [
      _buildInfoCard(
        'gem_business_registration',
        'gem_business_registration_desc',
        Icons.business,
      ),
      const SizedBox(height: 12),
      _buildInfoCard('gem_make_in_india', 'gem_make_in_india_desc', Icons.flag),
      const SizedBox(height: 12),
      _buildInfoCard(
        'gem_category_match',
        'gem_category_match_desc',
        Icons.category,
      ),
    ];
  }

  List<Widget> _buildDocumentsContent() {
    const documents = [
      'gem_gst_certificate',
      'gem_pan_card',
      'gem_aadhaar_card',
      'gem_business_address_proof',
      'gem_bank_account_details',
    ];

    return [
      Text(
        'gem_documents_title'.tr(),
        style: const TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.w600,
          color: AppColors.textPrimary,
        ),
      ),
      const SizedBox(height: 12),
      ...documents.map(
        (docKey) => Padding(
          padding: const EdgeInsets.symmetric(vertical: 4),
          child: Row(
            children: [
              const Icon(
                Icons.check_circle_outline,
                size: 20,
                color: AppColors.indigo,
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Text(docKey.tr(), style: const TextStyle(fontSize: 14)),
              ),
            ],
          ),
        ),
      ),
    ];
  }

  List<Widget> _buildProductCatalogueContent() {
    return [
      _buildInfoCard(
        'gem_product_title',
        'gem_product_title_desc',
        Icons.title,
      ),
      const SizedBox(height: 12),
      _buildInfoCard(
        'gem_technical_specs',
        'gem_technical_specs_desc',
        Icons.list_alt,
      ),
      const SizedBox(height: 12),
      _buildInfoCard(
        'gem_product_images',
        'gem_product_images_desc',
        Icons.image_outlined,
      ),
      const SizedBox(height: 12),
      _buildInfoCard('gem_pricing', 'gem_pricing_desc', Icons.currency_rupee),
    ];
  }

  List<Widget> _buildReviewContent() {
    return [
      _buildReviewSection('gem_review_business', [
        'gem_business_name: ${'gem_to_be_provided'.tr()}',
        'gem_gst_number: ${'gem_to_be_provided'.tr()}',
        'gem_pan: ${'gem_to_be_provided'.tr()}',
      ]),
      const SizedBox(height: 16),
      _buildReviewSection('gem_review_product', [
        'gem_product_title: ${'gem_from_craftsy'.tr()}',
        'gem_category: ${'gem_from_craftsy'.tr()}',
        'gem_pricing: ${'gem_from_craftsy'.tr()}',
      ]),
      const SizedBox(height: 16),
      _buildReviewSection('gem_review_documents', [
        'gem_gst_certificate: ${'gem_to_upload'.tr()}',
        'gem_pan_card: ${'gem_to_upload'.tr()}',
        'gem_aadhaar_card: ${'gem_to_upload'.tr()}',
      ]),
      const SizedBox(height: 24),
      Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.amber.withValues(alpha: 0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.amber.withValues(alpha: 0.3)),
        ),
        child: Row(
          children: [
            const Icon(Icons.warning_amber, color: AppColors.amber),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                'gem_proceed_dialog_msg'.tr(),
                style: TextStyle(fontSize: 13, color: AppColors.amberDark),
              ),
            ),
          ],
        ),
      ),
    ];
  }

  Widget _buildInfoCard(String titleKey, String descKey, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.cardSurface,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.oak.withValues(alpha: 0.3)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 24, color: AppColors.indigo),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  titleKey.tr(),
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  descKey.tr(),
                  style: const TextStyle(
                    fontSize: 13,
                    color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildReviewSection(String titleKey, List<String> items) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          titleKey.tr(),
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 8),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: AppColors.cardSurface,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: AppColors.oak.withValues(alpha: 0.3)),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: items
                .map(
                  (item) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 4),
                    child: Row(
                      children: [
                        const Icon(
                          Icons.circle,
                          size: 8,
                          color: AppColors.indigo,
                        ),
                        const SizedBox(width: 12),
                        Text(item, style: const TextStyle(fontSize: 14)),
                      ],
                    ),
                  ),
                )
                .toList(),
          ),
        ),
      ],
    );
  }

  void _handleNext() {
    if (_currentStep < _steps.length - 1) {
      setState(() {
        _currentStep++;
      });
    } else {
      _showProceedDialog();
    }
  }

  void _showProceedDialog() {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('gem_proceed_dialog_title'.tr()),
          content: Text('gem_proceed_dialog_msg'.tr()),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text('gem_cancel'.tr()),
            ),
            FilledButton(
              onPressed: () {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('gem_opening_instructions'.tr()),
                    backgroundColor: AppColors.indigo,
                  ),
                );
              },
              child: Text('gem_continue'.tr()),
            ),
          ],
        );
      },
    );
  }
}
