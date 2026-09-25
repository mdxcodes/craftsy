import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';

import '../../../core/services/commerce_service.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/widgets/app_image.dart';
import '../../../core/widgets/speak_button.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

/// Fetches one consumer order — server enforces ownership (404 otherwise).
final purchaseDetailProvider = FutureProvider.autoDispose
    .family<ConsumerOrderDetail, String>((ref, orderId) {
  return ref.watch(commerceServiceProvider).getMyOrder(orderId);
});

class PurchaseDetailScreen extends ConsumerWidget {
  final String orderId;

  const PurchaseDetailScreen({super.key, required this.orderId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final orderAsync = ref.watch(purchaseDetailProvider(orderId));

    return Scaffold(
      appBar: AppBar(
        title: Text('purchase_detail_title'.tr()),
      ),
      body: SafeArea(
        child: orderAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (error, _) => Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text('orders_load_failed'.tr()),
                const SizedBox(height: AccessibilityTokens.spacingMd),
                TextButton.icon(
                  onPressed: () =>
                      ref.invalidate(purchaseDetailProvider(orderId)),
                  icon: const Icon(Icons.refresh),
                  label: Text('action_retry'.tr()),
                ),
              ],
            ),
          ),
          data: (order) => _PurchaseDetailBody(order: order),
        ),
      ),
    );
  }
}

class _PurchaseDetailBody extends StatelessWidget {
  final ConsumerOrderDetail order;

  const _PurchaseDetailBody({required this.order});

  String _statusLabel(String status) {
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

  @override
  Widget build(BuildContext context) {
    final ttsText = [
      'purchase_detail_title'.tr(),
      _statusLabel(order.status),
      '₹${order.totalAmount.toStringAsFixed(0)}',
    ].join('. ');

    return SingleChildScrollView(
      padding: EdgeInsets.all(AppSpacing.screenPadding),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ── Header: order id + status + read aloud ──────────────
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      order.id,
                      style: AppTextStyles.headlineMedium,
                    ),
                    const SizedBox(height: AppSpacing.xs),
                    _StatusPill(status: order.status),
                  ],
                ),
              ),
              SpeakButton(compact: true, text: ttsText),
            ],
          ),

          // ── Tracking timeline (honest, backend-data only) ───────
          const SizedBox(height: AppSpacing.lg),
          _TrackingTimeline(status: order.status),

          // ── Items ────────────────────────────────────────────────
          const SizedBox(height: AppSpacing.lg),
          Text('purchase_items'.tr(), style: AppTextStyles.headlineMedium),
          const SizedBox(height: AppSpacing.md),
          ...order.items.map(
            (item) => Container(
              margin: const EdgeInsets.only(bottom: AppSpacing.md),
              padding: EdgeInsets.all(AppSpacing.cardPadding),
              decoration: BoxDecoration(
                color: AppColors.cardSurface,
                borderRadius:
                    BorderRadius.circular(AccessibilityTokens.radiusLg),
                border: Border.all(color: AppColors.parchmentDeep),
              ),
              child: Row(
                children: [
                  ClipRRect(
                    borderRadius: BorderRadius.circular(
                        AccessibilityTokens.radiusMd),
                    child: SizedBox(
                      width: 56,
                      height: 56,
                      child: AppImage(
                        imageUrl: item.imageUrl,
                        fallbackWidget: Container(
                          color: AppColors.parchmentDeep,
                          child: const Icon(Icons.image,
                              color: AppColors.textSecondary),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          item.title,
                          style: AppTextStyles.labelLarge,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: AppSpacing.xs),
                        Text(
                          '₹${item.unitPrice.toStringAsFixed(0)} × ${item.quantity}',
                          style: AppTextStyles.labelMedium.copyWith(
                            color: AppColors.textSecondary,
                          ),
                        ),
                      ],
                    ),
                  ),
                  Text(
                    '₹${item.totalPrice.toStringAsFixed(0)}',
                    style: AppTextStyles.labelLarge.copyWith(
                      color: AppColors.indigo,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ],
              ),
            ),
          ),

          // ── Payment ──────────────────────────────────────────────
          const SizedBox(height: AppSpacing.sm),
          Text('checkout_payment_method'.tr(),
              style: AppTextStyles.headlineMedium),
          const SizedBox(height: AppSpacing.md),
          _InfoCard(
            children: [
              _InfoRow(
                icon: Icons.payments_outlined,
                label: order.payment?.method == 'cod'
                    ? 'checkout_cod'.tr()
                    : (order.payment?.method ?? ''),
                value: order.payment != null
                    ? (order.payment!.status == 'pending'
                        ? 'payment_cod_pending'.tr()
                        : order.payment!.status)
                    : '',
              ),
              const SizedBox(height: AppSpacing.sm),
              _InfoRow(
                icon: Icons.receipt,
                label: 'cart_subtotal'.tr(),
                value: '₹${order.totalAmount.toStringAsFixed(0)}',
                isTotal: true,
              ),
            ],
          ),

          // ── Delivery address ─────────────────────────────────────
          const SizedBox(height: AppSpacing.lg),
          Text('checkout_delivery_address'.tr(),
              style: AppTextStyles.headlineMedium),
          const SizedBox(height: AppSpacing.md),
          if (order.address != null)
            _InfoCard(
              children: [
                Text(
                  '${order.address!.name} · ${order.address!.phone}',
                  style: AppTextStyles.labelLarge,
                ),
                const SizedBox(height: AppSpacing.xs),
                Text(
                  order.address!.oneLine,
                  style: AppTextStyles.bodyMedium.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
              ],
            )
          else
            Text(
              'order_address_unavailable'.tr(),
              style: AppTextStyles.bodyMedium,
            ),
          const SizedBox(height: AppSpacing.xl),
        ],
      ),
    );
  }
}

// ── Tracking timeline — honest internal states only ─────────────────────────

class _TrackingTimeline extends StatelessWidget {
  final String status;

  const _TrackingTimeline({required this.status});

  static const _stages = ['new', 'confirmed', 'packed', 'shipped', 'delivered'];

  @override
  Widget build(BuildContext context) {
    // Cancelled orders show a simple cancelled banner, not a fake timeline.
    if (status == 'cancelled') {
      return Container(
        width: double.infinity,
        padding: EdgeInsets.all(AppSpacing.cardPadding),
        decoration: BoxDecoration(
          color: AppColors.coralLight,
          borderRadius:
              BorderRadius.circular(AccessibilityTokens.radiusMd),
        ),
        child: Row(
          children: [
            const Icon(Icons.cancel_outlined, color: AppColors.coral),
            const SizedBox(width: AppSpacing.sm),
            Text(
              'order_status_cancelled'.tr(),
              style: AppTextStyles.labelLarge.copyWith(
                color: AppColors.coralDark,
              ),
            ),
          ],
        ),
      );
    }

    final currentIndex = _stages.indexOf(status);

    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.cardSurface,
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
        border: Border.all(color: AppColors.parchmentDeep),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          for (var i = 0; i < _stages.length; i++) ...[
            _TimelineStep(
              label: _statusLabel(_stages[i]),
              icon: switch (_stages[i]) {
                'new' => Icons.receipt_long,
                'confirmed' => Icons.check_circle_outline,
                'packed' => Icons.inventory_2_outlined,
                'shipped' => Icons.local_shipping_outlined,
                _ => Icons.home_outlined,
              },
              isDone: currentIndex >= i && currentIndex != -1,
              isLast: i == _stages.length - 1,
            ),
          ],
        ],
      ),
    );
  }

  String _statusLabel(String status) {
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
      default:
        return status;
    }
  }
}

class _TimelineStep extends StatelessWidget {
  final String label;
  final IconData icon;
  final bool isDone;
  final bool isLast;

  const _TimelineStep({
    required this.label,
    required this.icon,
    required this.isDone,
    required this.isLast,
  });

  @override
  Widget build(BuildContext context) {
    final color = isDone ? AppColors.teal : AppColors.inkFaint;

    return IntrinsicHeight(
      child: Row(
        children: [
          Column(
            children: [
              Icon(icon, size: 22, color: color),
              if (!isLast)
                Expanded(
                  child: Container(
                    width: 2,
                    color: isDone
                        ? AppColors.teal.withValues(alpha: 0.4)
                        : AppColors.parchmentDeep,
                  ),
                ),
            ],
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Padding(
              padding: const EdgeInsets.only(bottom: AppSpacing.md),
              child: Text(
                label,
                style: AppTextStyles.bodyMedium.copyWith(
                  color: isDone ? AppColors.textPrimary : AppColors.textTertiary,
                  fontWeight: isDone ? FontWeight.w700 : FontWeight.w400,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ── Shared bits ──────────────────────────────────────────────────────────────

class _InfoCard extends StatelessWidget {
  final List<Widget> children;

  const _InfoCard({required this.children});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.cardSurface,
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
        border: Border.all(color: AppColors.parchmentDeep),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: children,
      ),
    );
  }
}

class _InfoRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final bool isTotal;

  const _InfoRow({
    required this.icon,
    required this.label,
    required this.value,
    this.isTotal = false,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 20, color: AppColors.textSecondary),
        const SizedBox(width: AppSpacing.sm),
        Expanded(child: Text(label, style: AppTextStyles.bodyMedium)),
        Text(
          value,
          style: isTotal
              ? AppTextStyles.headlineMedium.copyWith(
                  color: AppColors.indigo,
                  fontWeight: FontWeight.w800,
                )
              : AppTextStyles.bodyMedium,
        ),
      ],
    );
  }
}

class _StatusPill extends StatelessWidget {
  final String status;

  const _StatusPill({required this.status});

  @override
  Widget build(BuildContext context) {
    final (bg, fg) = switch (status) {
      'delivered' => (AppColors.tealLight, AppColors.teal),
      'cancelled' => (AppColors.coralLight, AppColors.coralDark),
      'shipped' => (AppColors.indigoLight, AppColors.indigoDark),
      _ => (AppColors.amberLight, AppColors.amberDark),
    };

    String label() {
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

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusFull),
      ),
      child: Text(
        label(),
        style: AppTextStyles.labelSmall.copyWith(
          color: fg,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}
