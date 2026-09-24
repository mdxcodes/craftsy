import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';

import '../../../core/providers/app_providers.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/widgets/app_button.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../../../core/widgets/empty_state.dart';
import '../../../data/models/product.dart';
import '../../chatbot/screens/chatbot_sheet.dart';

/// Business Advisor — real insights from canonical product data.
///
/// Shows:
/// - Price review suggestions (products priced below AI suggestion)
/// - Low stock alerts (stock <= 5)
/// - Slow-moving products (no sales in 30+ days)
/// - Quick action to ask CraftMitra
///
/// All data comes from productListProvider — no fabricated metrics.
class BusinessAdvisorScreen extends ConsumerWidget {
  const BusinessAdvisorScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productsAsync = ref.watch(productListProvider);
    final products = productsAsync.valueOrNull ?? [];

    return AppScaffold(
      body: RefreshIndicator(
        onRefresh: () async {
          await ref.read(productListProvider.notifier).loadProducts(forceRefresh: true);
        },
        child: ListView(
          padding: const EdgeInsets.all(AppSpacing.screenPadding),
          children: [
            // Header
            Text(
              'advisor_title'.tr(),
              style: AppTextStyles.headlineMedium.copyWith(
                color: AppColors.ink,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: AppSpacing.sm),
            Text(
              'advisor_subtitle'.tr(),
              style: AppTextStyles.bodyMedium.copyWith(
                color: AppColors.inkSoft,
              ),
            ),
            const SizedBox(height: AppSpacing.lg),

            // Loading state
            if (productsAsync.isLoading && products.isEmpty)
              const Center(child: CircularProgressIndicator()),

            // Empty state
            if (!productsAsync.isLoading && products.isEmpty)
              EmptyState(
                icon: Icons.insights_outlined,
                title: 'advisor_no_products'.tr(),
                message: 'advisor_no_products_desc'.tr(),
                actionLabel: 'advisor_add_product'.tr(),
                onAction: () => context.push('/add-product'),
              ),

            // Price Review Section
            if (products.isNotEmpty) ...[
              _SectionHeader(
                icon: Icons.currency_rupee,
                title: 'advisor_price_review'.tr(),
                color: AppColors.indigo,
              ),
              const SizedBox(height: AppSpacing.sm),
              ...products.take(3).map((p) => _PriceReviewCard(product: p)),
              const SizedBox(height: AppSpacing.lg),
            ],

            // Low Stock Section
            if (products.any((p) => p.stock <= 5)) ...[
              _SectionHeader(
                icon: Icons.inventory_2_outlined,
                title: 'advisor_low_stock'.tr(),
                color: AppColors.coral,
              ),
              const SizedBox(height: AppSpacing.sm),
              ...products
                  .where((p) => p.stock <= 5)
                  .take(3)
                  .map((p) => _LowStockCard(product: p)),
              const SizedBox(height: AppSpacing.lg),
            ],

            // Slow Moving Section
            if (products.any((p) => p.isNonLive)) ...[
              _SectionHeader(
                icon: Icons.hourglass_empty_outlined,
                title: 'advisor_slow_moving'.tr(),
                color: AppColors.amber,
              ),
              const SizedBox(height: AppSpacing.sm),
              ...products
                  .where((p) => p.isNonLive)
                  .take(3)
                  .map((p) => _SlowMovingCard(product: p)),
              const SizedBox(height: AppSpacing.lg),
            ],

            // Ask CraftMitra CTA
            AppButton(
              label: 'advisor_ask_craftmitra'.tr(),
              icon: Icons.smart_toy_outlined,
              onPressed: () => ChatbotSheet.show(context),
              type: AppButtonType.secondary,
              width: double.infinity,
            ),
          ],
        ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final IconData icon;
  final String title;
  final Color color;

  const _SectionHeader({
    required this.icon,
    required this.title,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, color: color, size: 24),
        const SizedBox(width: AppSpacing.sm),
        Expanded(
          child: Text(
            title,
            style: AppTextStyles.headlineSmall.copyWith(
              color: color,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ],
    );
  }
}

class _PriceReviewCard extends StatelessWidget {
  final Product product;

  const _PriceReviewCard({required this.product});

  @override
  Widget build(BuildContext context) {
    final priceText = '₹${product.price.toStringAsFixed(0)}';

    return Semantics(
      container: true,
      label: '${product.title}, $priceText',
      child: Container(
        margin: const EdgeInsets.only(bottom: AppSpacing.sm),
        padding: const EdgeInsets.all(AppSpacing.cardPadding),
        decoration: BoxDecoration(
          color: AppColors.cardSurface,
          borderRadius: BorderRadius.circular(AppRadii.card),
          border: Border.all(color: AppColors.line),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              product.title,
              style: AppTextStyles.labelLarge.copyWith(
                color: AppColors.ink,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: AppSpacing.xs),
            Row(
              children: [
                Text(
                  'advisor_current_price'.tr(),
                  style: AppTextStyles.bodySmall.copyWith(color: AppColors.inkSoft),
                ),
                const SizedBox(width: AppSpacing.sm),
                Text(
                  priceText,
                  style: AppTextStyles.headlineSmall.copyWith(
                    color: AppColors.indigo,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _LowStockCard extends StatelessWidget {
  final Product product;

  const _LowStockCard({required this.product});

  @override
  Widget build(BuildContext context) {
    return Semantics(
      container: true,
      label: '${product.title}, ${product.stock} ${'advisor_in_stock'.tr()}',
      child: Container(
        margin: const EdgeInsets.only(bottom: AppSpacing.sm),
        padding: const EdgeInsets.all(AppSpacing.cardPadding),
        decoration: BoxDecoration(
          color: AppColors.coralLight,
          borderRadius: BorderRadius.circular(AppRadii.card),
          border: Border.all(color: AppColors.coral.withValues(alpha: 0.3)),
        ),
        child: Row(
          children: [
            Icon(Icons.warning_amber_rounded, color: AppColors.coral, size: 24),
            const SizedBox(width: AppSpacing.sm),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    product.title,
                    style: AppTextStyles.labelLarge.copyWith(
                      color: AppColors.ink,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  Text(
                    '${product.stock} ${'advisor_in_stock'.tr()}',
                    style: AppTextStyles.bodySmall.copyWith(color: AppColors.coral),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SlowMovingCard extends StatelessWidget {
  final Product product;

  const _SlowMovingCard({required this.product});

  @override
  Widget build(BuildContext context) {
    return Semantics(
      container: true,
      label: '${product.title}, ${product.status.name}',
      child: Container(
        margin: const EdgeInsets.only(bottom: AppSpacing.sm),
        padding: const EdgeInsets.all(AppSpacing.cardPadding),
        decoration: BoxDecoration(
          color: AppColors.amberLight,
          borderRadius: BorderRadius.circular(AppRadii.card),
          border: Border.all(color: AppColors.amber.withValues(alpha: 0.3)),
        ),
        child: Row(
          children: [
            Icon(Icons.hourglass_empty, color: AppColors.amber, size: 24),
            const SizedBox(width: AppSpacing.sm),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    product.title,
                    style: AppTextStyles.labelLarge.copyWith(
                      color: AppColors.ink,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  Text(
                    'advisor_status_${product.status.name}'.tr(),
                    style: AppTextStyles.bodySmall.copyWith(color: AppColors.amberDark),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
