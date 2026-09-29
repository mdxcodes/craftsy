import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';

import '../../../core/services/commerce_service.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/widgets/app_image.dart';
import '../../../core/widgets/empty_state.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

/// Fetches the authenticated user's placed orders (server-side ownership).
final myPurchasesProvider = FutureProvider<List<ConsumerOrderSummary>>(
    (ref) => ref.watch(commerceServiceProvider).getMyOrders());

class MyPurchasesScreen extends ConsumerWidget {
  const MyPurchasesScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final ordersAsync = ref.watch(myPurchasesProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text('my_purchases_title'.tr()),
      ),
      body: SafeArea(
        child: ordersAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (error, _) => EmptyState(
            icon: Icons.wifi_off,
            title: 'orders_load_failed'.tr(),
            actionLabel: 'action_retry'.tr(),
            onAction: () => ref.invalidate(myPurchasesProvider),
          ),
          data: (orders) {
            if (orders.isEmpty) {
              return EmptyState(
                icon: Icons.receipt_long_outlined,
                title: 'my_purchases_empty'.tr(),
                message: 'my_purchases_empty_desc'.tr(),
                actionLabel: 'cart_continue_shopping'.tr(),
                onAction: () => context.go('/marketplace'),
              );
            }
            return RefreshIndicator(
              onRefresh: () async =>
                  ref.refresh(myPurchasesProvider.future),
              child: ListView.separated(
                padding: EdgeInsets.all(AppSpacing.screenPadding),
                itemCount: orders.length,
                separatorBuilder: (_, _) =>
                    const SizedBox(height: AppSpacing.md),
                itemBuilder: (context, index) {
                  final order = orders[index];
                  return _OrderSummaryCard(order: order);
                },
              ),
            );
          },
        ),
      ),
    );
  }
}

class _OrderSummaryCard extends StatelessWidget {
  final ConsumerOrderSummary order;

  const _OrderSummaryCard({required this.order});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/purchase/${order.id}'),
      child: Container(
        padding: EdgeInsets.all(AppSpacing.cardPadding),
        decoration: BoxDecoration(
          color: AppColors.cardSurface,
          borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
          border: Border.all(color: AppColors.warmMist),
        ),
        child: Row(
          children: [
            // First item image
            ClipRRect(
              borderRadius:
                  BorderRadius.circular(AccessibilityTokens.radiusMd),
              child: SizedBox(
                width: 64,
                height: 64,
                child: AppImage(
                  imageUrl: order.firstItemImageUrl,
                  fallbackWidget: Container(
                    color: AppColors.warmMist,
                    child: const Icon(Icons.image,
                        color: AppColors.taupe),
                  ),
                ),
              ),
            ),
            const SizedBox(width: AppSpacing.md),

            // Info
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    order.itemCount > 1
                        ? '$firstTitle  +${order.itemCount - 1} ${'order_more_items'.tr()}'
                        : firstTitle,
                    style: AppTextStyles.labelLarge,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    _placedLabel(order.placedAt),
                    style: AppTextStyles.labelSmall.copyWith(
                      color: AppColors.taupe,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(width: AppSpacing.sm),

            // Total + status
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  '₹${order.totalAmount.toStringAsFixed(0)}',
                  style: AppTextStyles.headlineSmall.copyWith(
                    color: AppColors.burgundy,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: AppSpacing.xs),
                _StatusPill(status: order.status),
              ],
            ),
          ],
        ),
      ),
    );
  }

  String get firstTitle => order.firstItemTitle.isNotEmpty
      ? order.firstItemTitle
      : 'order_item_unnamed'.tr();

  String _placedLabel(String? placedAt) {
    if (placedAt == null || placedAt.isEmpty) return '';
    final dt = DateTime.tryParse(placedAt);
    if (dt == null) return '';
    return 'order_placed_on'.tr(namedArgs: {
      'date': '${dt.day}/${dt.month}/${dt.year}',
    });
  }
}

/// Small status pill — only shows states that exist in backend data.
class _StatusPill extends StatelessWidget {
  final String status;

  const _StatusPill({required this.status});

  @override
  Widget build(BuildContext context) {
    final (bg, fg) = switch (status) {
      'delivered' => (AppColors.sageLight, AppColors.sage),
      'cancelled' => (AppColors.siennaLight, AppColors.siennaDark),
      'shipped' => (AppColors.burgundyLight, AppColors.burgundyDark),
      _ => (AppColors.goldLight, AppColors.goldDark),
    };

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusFull),
      ),
      child: Text(
        _label(),
        style: AppTextStyles.labelSmall.copyWith(
          color: fg,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }

  String _label() {
    switch (status) {
      case 'new':
        return 'order_status_new'.tr();
      case 'confirmed':
        return 'order_status_confirmed'.tr();
      case 'packed':
        return 'order_status_packed'.tr();
      case 'shipped':
        return 'order_status_shipped'.tr();
      case 'delivered':
        return 'order_status_delivered'.tr();
      case 'cancelled':
        return 'order_status_cancelled'.tr();
      default:
        return status;
    }
  }
}
