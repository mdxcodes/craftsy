import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/widgets/primary_action_button.dart';
import '../../../core/widgets/secondary_action_button.dart';

class _GemStep {
  final String title;
  final String description;
  final IconData icon;

  const _GemStep({
    required this.title,
    required this.description,
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

  const GovernmentSellingScreen({
    super.key,
    this.productId,
  });

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
      title: 'Check Eligibility',
      description: 'Verify your business meets GeM seller requirements.',
      icon: Icons.fact_check_outlined,
    ),
    _GemStep(
      title: 'Prepare Documents',
      description: 'Gather required documents: GST, PAN, Aadhaar, business proof.',
      icon: Icons.description_outlined,
    ),
    _GemStep(
      title: 'Product Catalogue',
      description: 'Prepare product information for GeM listing.',
      icon: Icons.inventory_2_outlined,
    ),
    _GemStep(
      title: 'Review & Submit',
      description: 'Review everything before proceeding to GeM.',
      icon: Icons.fact_check,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Government Selling'),
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
                    'This assistant helps you prepare for Government Selling. '
                    'You will complete the final steps on the official GeM portal.',
                    style: TextStyle(
                      fontSize: 13,
                      color: AppColors.amberDark,
                    ),
                  ),
                ),
              ],
            ),
          ),

          // Stepper
          Padding(
            padding: const EdgeInsets.all(24),
            child: _buildStepper(),
          ),

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
                      label: 'Back',
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
                        ? 'Continue'
                        : 'Review & Proceed',
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
                step.title,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 16),
        Text(
          step.description,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: AppColors.textSecondary,
              ),
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
        'Business Registration',
        'Your business must be registered with a valid GST number.',
        Icons.business,
      ),
      const SizedBox(height: 12),
      _buildInfoCard(
        'Make in India',
        'Products must be manufactured in India.',
        Icons.flag),
      const SizedBox(height: 12),
      _buildInfoCard(
        'Category Match',
        'Your craft category must match GeM\'s approved categories.',
        Icons.category,
      ),
    ];
  }

  List<Widget> _buildDocumentsContent() {
    const documents = [
      'GST Certificate',
      'PAN Card',
      'Aadhaar Card',
      'Business Address Proof',
      'Bank Account Details',
    ];

    return [
      const Text(
        'Required Documents',
        style: TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.w600,
          color: AppColors.textPrimary,
        ),
      ),
      const SizedBox(height: 12),
      ...documents.map(
        (doc) => Padding(
          padding: const EdgeInsets.symmetric(vertical: 4),
          child: Row(
            children: [
              const Icon(Icons.check_circle_outline,
                  size: 20, color: AppColors.indigo),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  doc,
                  style: const TextStyle(fontSize: 14),
                ),
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
        'Product Title',
        'Clear, descriptive title that matches GeM naming conventions.',
        Icons.title,
      ),
      const SizedBox(height: 12),
      _buildInfoCard(
        'Technical Specifications',
        'Detailed specifications: dimensions, weight, material, color.',
        Icons.list_alt,
      ),
      const SizedBox(height: 12),
      _buildInfoCard(
        'Product Images',
        'High-quality images from multiple angles.',
        Icons.image_outlined,
      ),
      const SizedBox(height: 12),
      _buildInfoCard(
        'Pricing',
        'Competitive pricing including GST.',
        Icons.currency_rupee,
      ),
    ];
  }

  List<Widget> _buildReviewContent() {
    return [
      _buildReviewSection('Business', [
        'Business Name: [To be provided]',
        'GST Number: [To be provided]',
        'PAN: [To be provided]',
      ]),
      const SizedBox(height: 16),
      _buildReviewSection('Product', [
        'Title: [From Craftsy listing]',
        'Category: [From Craftsy listing]',
        'Price: [From Craftsy listing]',
      ]),
      const SizedBox(height: 16),
      _buildReviewSection('Documents', [
        'GST Certificate: [To upload]',
        'PAN Card: [To upload]',
        'Aadhaar Card: [To upload]',
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
                'After proceeding, you will be guided to the official GeM portal '
                'to complete your seller registration and product listing.',
                style: TextStyle(
                  fontSize: 13,
                  color: AppColors.amberDark,
                ),
              ),
            ),
          ],
        ),
      ),
    ];
  }

  Widget _buildInfoCard(String title, String description, IconData icon) {
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
                  title,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: AppColors.textPrimary,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  description,
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

  Widget _buildReviewSection(String title, List<String> items) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
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
                        const Icon(Icons.circle, size: 8, color: AppColors.indigo),
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
          title: const Text('Proceed to GeM Portal'),
          content: const Text(
            'You are about to proceed to the official GeM portal to complete '
            'your Government Selling registration. Craftsy will not store any '
            'of your GeM credentials.\n\n'
            'Do you want to continue?',
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            FilledButton(
              onPressed: () {
                Navigator.pop(context);
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Opening GeM portal instructions...'),
                    backgroundColor: AppColors.indigo,
                  ),
                );
              },
              child: const Text('Continue'),
            ),
          ],
        );
      },
    );
  }
}
