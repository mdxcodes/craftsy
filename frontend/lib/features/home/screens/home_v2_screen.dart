import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';
import '../../../core/providers/app_providers.dart';
import '../../../core/router/app_route_constants.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../../../core/widgets/app_image.dart';
import '../../../core/widgets/visual_status_chip.dart';
import '../../../core/widgets/large_action_card.dart';
import '../../../core/widgets/empty_state.dart';
import '../../../core/widgets/offline_state.dart';
import '../../../core/widgets/sync_status_banner.dart';
import '../../../core/widgets/draft_resume_card.dart';
import '../../orders/models/order.dart';
import '../../orders/providers/orders_provider.dart';
import 'business_advisor_screen.dart';

/// V2 Home Screen — the artisan's daily command center.
///
/// Shows greeting, quick actions, recent orders, and earnings snapshot.
/// Uses V2 design components (LargeActionCard, VisualStatusChip, etc.).
class HomeV2Screen extends ConsumerWidget {
  const HomeV2Screen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final userProfile = ref.watch(userProfileProvider);
    final orders = ref.watch(filteredOrdersProvider);
    final isOnline = ref.watch(connectivityProvider).value ?? true;

    final artisanName = userProfile.name.isNotEmpty
        ? userProfile.name.split(' ').first
        : null;

    return AppScaffold(
      body: RefreshIndicator(
        onRefresh: () async {
          // Data is mock for now — no refresh needed
        },
        child: ListView(
          padding: const EdgeInsets.only(bottom: AppSpacing.xxl),
          children: [
            // Greeting header
            _GreetingHeader(name: artisanName),

            // Offline banner
            if (!isOnline) ...[
              const SizedBox(height: AppSpacing.md),
              const OfflineState(),
            ],

            // Draft resume card
            const SizedBox(height: AppSpacing.md),
            const DraftResumeCard(),

            // Sync queue status
            const SizedBox(height: AppSpacing.md),
            const SyncStatusBanner(),

            const SizedBox(height: AppSpacing.lg),

            // Quick actions
            _QuickActions(),

            const SizedBox(height: AppSpacing.lg),

            // Recent orders
            _RecentOrdersSection(orders: orders),

            const SizedBox(height: AppSpacing.lg),

            // Earnings snapshot
            _EarningsSnapshot(),
          ],
        ),
      ),
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Greeting Header
// ─────────────────────────────────────────────────────────────────────────────

class _GreetingHeader extends StatelessWidget {
  final String? name;

  const _GreetingHeader({this.name});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [AppColors.burgundy, AppColors.burgundyLight],
        ),
        borderRadius: const BorderRadius.only(
          bottomLeft: Radius.circular(24),
          bottomRight: Radius.circular(24),
        ),
      ),
      child: SafeArea(
        bottom: false,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                       if (name != null && name!.isNotEmpty)
                         Semantics(
                           label: 'home_greeting'.tr(args: [name!]),
                           child: Text(
                             'home_greeting'.tr(args: [name!]),
                             style: AppTextStyles.headlineLarge.copyWith(
                               color: AppColors.cardSurface,
                             ),
                           ),
                         )
                       else
                         Semantics(
                           label: 'home_greeting_no_name'.tr(),
                           child: Text(
                             'home_greeting_no_name'.tr(),
                             style: AppTextStyles.headlineLarge.copyWith(
                               color: AppColors.cardSurface,
                             ),
                           ),
                         ),
                      const SizedBox(height: AppSpacing.xs),
                       Text(
                         'home_subtitle'.tr(),
                         style: AppTextStyles.bodyLarge.copyWith(
                           color: AppColors.cream,
                         ),
                       ),
                    ],
                  ),
                ),
                // Profile avatar
                 Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: AppColors.gold,
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    Icons.person,
                    color: AppColors.burgundy,
                    size: 28,
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

// ─────────────────────────────────────────────────────────────────────────────
// Quick Actions
// ─────────────────────────────────────────────────────────────────────────────

class _QuickActions extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('home_quick_actions'.tr(), style: AppTextStyles.headlineSmall),
          const SizedBox(height: AppSpacing.md),
          Row(
            children: [
              Expanded(
                child: LargeActionCard(
                  label: 'home_add_product'.tr(),
                  icon: Icons.add_a_photo,
                  onTap: () => context.pushNamed(AppRouteConstants.addProduct),
                  backgroundColor: AppColors.goldLight,
                  iconColor: AppColors.gold,
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: LargeActionCard(
                  label: 'home_my_catalogue'.tr(),
                  icon: Icons.grid_view,
                  onTap: () => context.pushNamed(AppRouteConstants.catalogue),
                  backgroundColor: AppColors.sageLight,
                  iconColor: AppColors.sage,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.md),
           Row(
             children: [
                Expanded(
                  child: LargeActionCard(
                    label: 'home_my_orders'.tr(),
                    icon: Icons.receipt_long,
                    onTap: () => context.pushNamed(AppRouteConstants.myOrders),
                    backgroundColor: AppColors.burgundyLight,
                    iconColor: AppColors.burgundy,
                  ),
                ),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: LargeActionCard(
                    label: 'home_my_stats'.tr(),
                    icon: Icons.trending_up,
                    onTap: () => context.pushNamed(AppRouteConstants.myStats),
                    backgroundColor: AppColors.sageLight,
                    iconColor: AppColors.sage,
                  ),
                ),
             ],
           ),
            Row(
              children: [
                Expanded(
                  child: LargeActionCard(
                    label: 'advisor_title'.tr(),
                    icon: Icons.lightbulb,
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => BusinessAdvisorScreen(),
                        ),
                      );
                    },
                    backgroundColor: AppColors.goldLight,
                    iconColor: AppColors.gold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.md),
            Row(
              children: [
                Expanded(
                  child: LargeActionCard(
                    label: 'marketplace_title'.tr(),
                    icon: Icons.storefront,
                    onTap: () => context.pushNamed(AppRouteConstants.marketplace),
                    backgroundColor: AppColors.goldLight,
                    iconColor: AppColors.gold,
                  ),
                ),
              ],
            ),
         ],
      ),
    );
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Recent Orders Section
// ─────────────────────────────────────────────────────────────────────────────

class _RecentOrdersSection extends StatelessWidget {
  final List<Order> orders;

  const _RecentOrdersSection({required this.orders});

  @override
  Widget build(BuildContext context) {
    final recentOrders = orders.take(3).toList();

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'home_recent_orders'.tr(),
                style: AppTextStyles.headlineSmall,
              ),
              if (orders.isNotEmpty)
                TextButton(
                  onPressed: () =>
                      context.pushNamed(AppRouteConstants.myOrders),
                  child: Text('home_view_all'.tr()),
                ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          if (recentOrders.isEmpty)
            EmptyState(
              icon: Icons.receipt_long,
              title: 'home_empty_orders_title'.tr(),
              message: 'home_empty_orders_desc'.tr(),
              actionLabel: 'home_start_listing'.tr(),
              onAction: () => context.pushNamed(AppRouteConstants.addProduct),
            )
          else
            ...recentOrders.map((order) => _OrderCard(order: order)),
        ],
      ),
    );
  }
}

class _OrderCard extends StatelessWidget {
  final Order order;

  const _OrderCard({required this.order});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: AppSpacing.sm),
      child: Semantics(
        button: true,
        label: 'order_card'.tr(
          namedArgs: {
            'product': order.productTitle,
            'status': order.status.labelKey.tr(),
          },
        ),
        child: InkWell(
          onTap: () =>
              context.pushNamed(AppRouteConstants.orderDetail, extra: order),
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.md),
            child: Row(
              children: [
                // Product image placeholder
                 Container(
                  width: 56,
                  height: 56,
                  decoration: BoxDecoration(
                    color: AppColors.warmMist,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: order.productImagePath.isNotEmpty
                      ? ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: AppImage(
                            imageUrl: order.productImagePath,
                            fit: BoxFit.cover,
                          ),
                        )
                      : Icon(
                          Icons.inventory_2,
                          color: AppColors.taupe,
                          size: 28,
                        ),
                ),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        order.productTitle,
                        style: AppTextStyles.headlineSmall,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      Text(
                        'order_placed_on'.tr(
                          args: [_formatDate(order.placedAt)],
                        ),
                        style: AppTextStyles.bodySmall.copyWith(
                          color: AppColors.taupe,
                        ),
                      ),
                    ],
                  ),
                ),
                VisualStatusChip(
                  type: _mapOrderStatus(order.status),
                  label: _mapOrderStatusLabel(order.status),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  VisualStatusType _mapOrderStatus(OrderStatus status) {
    switch (status) {
      case OrderStatus.newOrder:
        return VisualStatusType.pending;
      case OrderStatus.packed:
        return VisualStatusType.warning;
      case OrderStatus.shipped:
        return VisualStatusType.pending;
      case OrderStatus.delivered:
        return VisualStatusType.success;
      case OrderStatus.cancelled:
        return VisualStatusType.error;
    }
  }

  String _mapOrderStatusLabel(OrderStatus status) {
    switch (status) {
      case OrderStatus.newOrder:
        return 'home_order_status_new'.tr();
      case OrderStatus.packed:
        return 'home_order_status_packed'.tr();
      case OrderStatus.shipped:
        return 'home_order_status_shipped'.tr();
      case OrderStatus.delivered:
        return 'home_order_status_delivered'.tr();
      case OrderStatus.cancelled:
        return 'cancelled_label'.tr();
    }
  }

  String _formatDate(DateTime date) {
    final now = DateTime.now();
    final diff = now.difference(date);
    if (diff.inDays == 0) {
      return 'Today';
    } else if (diff.inDays == 1) {
      return 'Yesterday';
    } else if (diff.inDays < 7) {
      return '${diff.inDays} days ago';
    } else {
      return '${date.day}/${date.month}/${date.year}';
    }
  }
}

// ─────────────────────────────────────────────────────────────────────────────
// Earnings Snapshot
// ─────────────────────────────────────────────────────────────────────────────

class _EarningsSnapshot extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'home_earnings_snapshot'.tr(),
                style: AppTextStyles.headlineSmall,
              ),
              TextButton(
                onPressed: () => context.pushNamed(AppRouteConstants.myStats),
                child: Text('home_view_all'.tr()),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          Container(
            padding: const EdgeInsets.all(AppSpacing.lg),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [
                  AppColors.goldLight,
                  AppColors.gold.withValues(alpha: 0.1),
                ],
              ),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: AppColors.gold.withValues(alpha: 0.3)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                 Text(
                   'home_earnings_subtitle'.tr(),
                   style: AppTextStyles.bodyMedium.copyWith(
                     color: AppColors.taupe,
                   ),
                 ),
                const SizedBox(height: AppSpacing.md),
                Row(
                  children: [
                    Expanded(
                      child: _EarningsMetric(
                        label: 'home_total_earnings'.tr(),
                        value: '₹0',
                        icon: Icons.account_balance_wallet,
                      ),
                    ),
                    Expanded(
                      child: _EarningsMetric(
                        label: 'home_pending_orders'.tr(),
                        value: '0',
                        icon: Icons.pending_actions,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _EarningsMetric extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;

  const _EarningsMetric({
    required this.label,
    required this.value,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, size: 20, color: AppColors.gold),
            const SizedBox(width: AppSpacing.xs),
            Text(
              label,
              style: AppTextStyles.bodySmall.copyWith(color: AppColors.taupe),
            ),
          ],
        ),
        const SizedBox(height: AppSpacing.xs),
        Text(
          value,
          style: AppTextStyles.headlineMedium.copyWith(
            color: AppColors.ink,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }
}
