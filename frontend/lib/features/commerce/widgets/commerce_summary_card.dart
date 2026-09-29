import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/models/commerce_hub_models.dart';
import '../../../core/theme/app_colors.dart';

/// Commerce summary card showing key metrics.
class CommerceSummaryCard extends StatelessWidget {
  final CommerceSummary summary;

  const CommerceSummaryCard({super.key, required this.summary});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'commerce_hub_summary'.tr(),
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _buildRow(context, 'Total Products', '${summary.totalProducts}'),
            _buildRow(context, 'Live Products', '${summary.liveProducts}'),
            _buildRow(context, 'Total Orders', '${summary.totalOrders}'),
            if (summary.productsNeedingAttention > 0)
              _buildRow(
                context,
                'Needs Attention',
                '${summary.productsNeedingAttention}',
                color: AppColors.sienna,
              ),
            if (summary.lowStock > 0)
              _buildRow(
                context,
                'Low Stock',
                '${summary.lowStock}',
                color: AppColors.gold,
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildRow(
    BuildContext context,
    String label,
    String value, {
    Color? color,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: Theme.of(context).textTheme.bodyMedium),
          Text(
            value,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
              color: color,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}
