import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';

import '../../../core/services/commerce_service.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/widgets/app_image.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

class OrderConfirmationScreen extends StatelessWidget {
  final PlacedOrder order;

  const OrderConfirmationScreen({super.key, required this.order});

  @override
  Widget build(BuildContext context) {
    final cod = order.payment?.method == 'cod';

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(AppSpacing.screenPadding),
          child: Column(
            children: [
              const SizedBox(height: AppSpacing.lg),

              // Success icon
              Container(
                width: 88,
                height: 88,
                decoration: const BoxDecoration(
                  color: AppColors.sageLight,
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.check_circle_outline,
                  size: 48,
                  color: AppColors.sage,
                ),
              ),
              const SizedBox(height: AppSpacing.lg),

              Text(
                'order_confirmed_title'.tr(),
                style: AppTextStyles.headlineLarge,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSpacing.sm),
              Text(
                // COD: money is NOT yet received — say so honestly
                cod
                    ? 'order_confirmed_cod_note'.tr()
                    : 'order_confirmed_paid_note'.tr(),
                style: AppTextStyles.bodyMedium,
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: AppSpacing.xl),

              // Order summary card — real backend data only
              Container(
                width: double.infinity,
                padding: EdgeInsets.all(AppSpacing.cardPadding),
                decoration: BoxDecoration(
                  color: AppColors.cardSurface,
                  borderRadius:
                      BorderRadius.circular(AccessibilityTokens.radiusLg),
                  border: Border.all(color: AppColors.warmMist),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          'order_id_label'.tr(),
                          style: AppTextStyles.labelMedium.copyWith(
                            color: AppColors.taupe,
                          ),
                        ),
                        const Spacer(),
                        Expanded(
                          child: Text(
                            order.id,
                            style: AppTextStyles.labelLarge,
                            textAlign: TextAlign.end,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                    Divider(color: AppColors.warmMist),
                    ...order.items.map(
                      (item) => Padding(
                        padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                        child: Row(
                          children: [
                            ClipRRect(
                              borderRadius: BorderRadius.circular(
                                  AccessibilityTokens.radiusSm),
                              child: SizedBox(
                                width: 44,
                                height: 44,
                                child: AppImage(
                                  imageUrl: item.imageUrl,
                                  fallbackWidget: Container(
                                    color: AppColors.warmMist,
                                    child: const Icon(Icons.image,
                                        size: 20,
                                        color: AppColors.taupe),
                                  ),
                                ),
                              ),
                            ),
                            const SizedBox(width: AppSpacing.sm),
                            Expanded(
                              child: Text(
                                '${item.title}  ×${item.quantity}',
                                style: AppTextStyles.bodyMedium,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                            Text(
                              '₹${item.totalPrice.toStringAsFixed(0)}',
                              style: AppTextStyles.bodyMedium,
                            ),
                          ],
                        ),
                      ),
                    ),
                    Divider(color: AppColors.warmMist),
                    _SummaryRow(
                      label: 'cart_subtotal'.tr(),
                      value: '₹${order.totalAmount.toStringAsFixed(0)}',
                      isTotal: true,
                    ),
                    const SizedBox(height: AppSpacing.sm),
                    _SummaryRow(
                      label: 'order_payment_status'.tr(),
                      value: 'payment_method_cod'.tr(),
                    ),
                    if (order.shipment != null) ...[
                      const SizedBox(height: AppSpacing.sm),
                      _SummaryRow(
                        label: 'order_status_label'.tr(),
                        value: _statusLabel(order.status),
                      ),
                    ],
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Next actions
              FilledButton(
                onPressed: () => context.pushReplacement('/my-purchases'),
                style: FilledButton.styleFrom(
                  backgroundColor: AppColors.burgundy,
                  foregroundColor: AppColors.textOnPrimary,
                  minimumSize: const Size.fromHeight(
                      AccessibilityTokens.minTouchTarget),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(
                        AccessibilityTokens.radiusFull),
                  ),
                ),
                child: Text('order_view_my_orders'.tr()),
              ),
              const SizedBox(height: AppSpacing.md),
              OutlinedButton(
                onPressed: () => context.go('/marketplace'),
                style: OutlinedButton.styleFrom(
                  foregroundColor: AppColors.burgundy,
                  minimumSize: const Size.fromHeight(
                      AccessibilityTokens.minTouchTarget),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(
                        AccessibilityTokens.radiusFull),
                  ),
                ),
                child: Text('cart_continue_shopping'.tr()),
              ),
            ],
          ),
        ),
      ),
    );
  }

  static String _statusLabel(String status) {
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

class _SummaryRow extends StatelessWidget {
  final String label;
  final String value;
  final bool isTotal;

  const _SummaryRow({
    required this.label,
    required this.value,
    this.isTotal = false,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(
          label,
          style: AppTextStyles.labelLarge,
        ),
        const Spacer(),
        Text(
          value,
          style: isTotal
              ? AppTextStyles.headlineMedium.copyWith(
                  color: AppColors.burgundy,
                  fontWeight: FontWeight.w800,
                )
              : AppTextStyles.bodyMedium,
        ),
      ],
    );
  }
}
