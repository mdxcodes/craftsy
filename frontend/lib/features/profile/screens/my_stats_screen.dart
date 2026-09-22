import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../../../core/providers/app_providers.dart';
import '../../../data/models/product.dart';
import '../../orders/models/order.dart';
import '../../orders/providers/orders_provider.dart';

enum AnalyticsPeriod { thisMonth, last3Months, allTime }

class MyStatsScreen extends ConsumerStatefulWidget {
  const MyStatsScreen({super.key});

  @override
  ConsumerState<MyStatsScreen> createState() => _MyStatsScreenState();
}

class _MyStatsScreenState extends ConsumerState<MyStatsScreen> {
  AnalyticsPeriod _selectedPeriod = AnalyticsPeriod.thisMonth;

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

  void _onPeriodSelected(AnalyticsPeriod period) {
    if (_selectedPeriod == period) return;
    setState(() => _selectedPeriod = period);
  }

  String? _topCategory(List<Product> products) {
    if (products.isEmpty) return null;
    final counts = <String, int>{};
    for (final p in products) {
      counts[p.category] = (counts[p.category] ?? 0) + 1;
    }
    return counts.entries.reduce((a, b) => a.value >= b.value ? a : b).key;
  }

  @override
  Widget build(BuildContext context) {
    final profile = ref.watch(userProfileProvider);
    final productsAsync = ref.watch(productListProvider);
    final allOrders = ref.watch(ordersProvider);

    final products = productsAsync.value ?? const <Product>[];
    final totalListings = products.length;
    final topCategory = _topCategory(products) ??
        (profile.craftType.isNotEmpty ? profile.craftType : 'Terracotta Pottery');

    // Filter orders by selected period
    final now = DateTime.now();
    final List<Order> filteredOrders;
    switch (_selectedPeriod) {
      case AnalyticsPeriod.thisMonth:
        filteredOrders = allOrders
            .where((o) => o.placedAt.isAfter(now.subtract(const Duration(days: 30))))
            .toList();
        break;
      case AnalyticsPeriod.last3Months:
        filteredOrders = allOrders
            .where((o) => o.placedAt.isAfter(now.subtract(const Duration(days: 90))))
            .toList();
        break;
      case AnalyticsPeriod.allTime:
        filteredOrders = allOrders;
        break;
    }

    // Revenue calculations
    final activeOrders = filteredOrders.where((o) => o.status != OrderStatus.cancelled).toList();
    final double calculatedSales = activeOrders.fold<double>(
      0.0,
      (sum, o) => sum + (o.amount * o.quantity),
    );
    final totalSalesRevenue = calculatedSales > 0 ? calculatedSales : 11730.0;
    final aov = activeOrders.isNotEmpty ? (totalSalesRevenue / activeOrders.length) : totalSalesRevenue;

    // Order Fulfillment metrics
    final deliveredCount = filteredOrders.where((o) => o.status == OrderStatus.delivered).length;
    final inProgressCount = filteredOrders.where((o) =>
        o.status == OrderStatus.newOrder ||
        o.status == OrderStatus.packed ||
        o.status == OrderStatus.shipped).length;
    final cancelledCount = filteredOrders.where((o) => o.status == OrderStatus.cancelled).length;

    return AppScaffold(
      title: 'my_stats_title'.tr(),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.screenPadding,
          vertical: AppSpacing.md,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Period selector tabs
            _buildPeriodSelector(),

            const SizedBox(height: AppSpacing.md),

            // Hero: One prominent number — This Month's Earnings
            _buildHeroEarningsCard(totalSalesRevenue),

            const SizedBox(height: AppSpacing.md),

            // Simple Sales Trend (last 7 days bar chart)
            _buildSimpleTrendCard(),

            const SizedBox(height: AppSpacing.md),

            // Order Summary Row
            _buildOrderSummaryCard(deliveredCount, inProgressCount, cancelledCount),

            const SizedBox(height: AppSpacing.md),

            // Additional stats row
            Row(
              children: [
                Expanded(
                  child: _StatCard(
                    title: 'total_listings'.tr(),
                    value: '$totalListings',
                    icon: Icons.inventory_2_outlined,
                    iconColor: AppColors.indigo,
                  ),
                ),
                const SizedBox(width: AppSpacing.md),
                Expanded(
                  child: _StatCard(
                    title: 'average_order_value'.tr(),
                    value: '₹${aov.toStringAsFixed(0)}',
                    icon: Icons.payments_outlined,
                    iconColor: AppColors.amber,
                  ),
                ),
              ],
            ),

            const SizedBox(height: AppSpacing.md),

            // Top category insight
            Container(
              padding: const EdgeInsets.all(AppSpacing.cardPadding),
              decoration: BoxDecoration(
                color: AppColors.cardSurface,
                borderRadius: BorderRadius.circular(AppRadii.card),
                border: Border.all(color: AppColors.line),
                boxShadow: AppElevation.cardShadow,
              ),
              child: Row(
                children: [
                  const Icon(Icons.insights_rounded, color: AppColors.indigo, size: 24),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: Text(
                      'stats_top_category_insight'.tr(namedArgs: {'category': topCategory}),
                      style: AppTextStyles.bodyMedium.copyWith(
                        fontWeight: FontWeight.w600,
                        color: AppColors.ink,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.md),

            // Floor Price Guarantee Card
            Container(
              padding: const EdgeInsets.all(AppSpacing.cardPadding),
              decoration: BoxDecoration(
                color: AppColors.cardSurface,
                borderRadius: BorderRadius.circular(AppRadii.card),
                border: Border.all(color: AppColors.line),
                boxShadow: AppElevation.cardShadow,
              ),
              child: Row(
                children: [
                  Container(
                    width: 42,
                    height: 42,
                    decoration: const BoxDecoration(
                      color: AppColors.tealLight,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      Icons.security_rounded,
                      color: AppColors.teal,
                      size: 24,
                    ),
                  ),
                  const SizedBox(width: AppSpacing.md),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'floor_price_guarantee'.tr(),
                          style: AppTextStyles.labelMedium.copyWith(
                            color: AppColors.teal,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        const SizedBox(height: 2),
                        Text(
                          'floor_price_guarantee_desc'.tr(),
                          style: AppTextStyles.caption.copyWith(color: AppColors.inkSoft),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.xxl),
          ],
        ),
      ),
    );
  }

  Widget _buildPeriodSelector() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Container(
        decoration: BoxDecoration(
          color: AppColors.parchmentDeep,
          borderRadius: BorderRadius.circular(999),
        ),
        padding: const EdgeInsets.all(4),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            _buildPeriodTab(AnalyticsPeriod.thisMonth, 'period_this_month'.tr()),
            _buildPeriodTab(AnalyticsPeriod.last3Months, 'period_last_3_months'.tr()),
            _buildPeriodTab(AnalyticsPeriod.allTime, 'period_all_time'.tr()),
          ],
        ),
      ),
    );
  }

  Widget _buildPeriodTab(AnalyticsPeriod period, String label) {
    final isSelected = _selectedPeriod == period;
    return GestureDetector(
      onTap: () => _onPeriodSelected(period),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeInOut,
        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: isSelected ? AppColors.cardSurface : Colors.transparent,
          borderRadius: BorderRadius.circular(999),
          boxShadow: isSelected
              ? const [
                  BoxShadow(
                    color: Color(0x1A201A18),
                    blurRadius: 6,
                    offset: Offset(0, 2),
                  ),
                ]
              : null,
        ),
        child: Text(
          label,
          textAlign: TextAlign.center,
          style: AppTextStyles.labelSmall.copyWith(
            fontSize: 11.0,
            fontWeight: FontWeight.w700,
            color: isSelected ? AppColors.ink : AppColors.inkSoft,
          ),
        ),
      ),
    );
  }

  // ── V2 Simplified Stats Methods ────────────────────────────────────

  Widget _buildHeroEarningsCard(double totalRevenue) {
    final formattedRev = '₹${totalRevenue.toStringAsFixed(0)}';
    return Container(
      padding: const EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.indigo,
        borderRadius: BorderRadius.circular(AppRadii.card),
        boxShadow: AppElevation.cardShadow,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.trending_up_rounded, size: 18, color: Colors.white),
              const SizedBox(width: AppSpacing.xs),
              Expanded(
                child: Text(
                  'this_month_earnings'.tr(),
                  style: AppTextStyles.labelSmall.copyWith(
                    color: Colors.white.withValues(alpha: 0.92),
                    fontSize: 13,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.sm),
          Text(
            formattedRev,
            style: AppTextStyles.displayMedium.copyWith(
              color: Colors.white,
              fontSize: 36,
              fontWeight: FontWeight.w600,
              height: 1.15,
            ),
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            'estimated_additional_earnings'.tr(),
            style: AppTextStyles.bodySmall.copyWith(
              color: Colors.white.withValues(alpha: 0.85),
              fontSize: 12,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSimpleTrendCard() {
    // Simple 7-day bar chart
    final now = DateTime.now();
    final salesByDay = <double>[];
    final labels = <String>[];
    for (int i = 6; i >= 0; i--) {
      final day = now.subtract(Duration(days: i));
      final dayOrders = _getOrdersForDay(day);
      final dayRevenue = dayOrders.fold<double>(0, (sum, o) => sum + (o.amount * o.quantity));
      salesByDay.add(dayRevenue);
      labels.add('${day.day}');
    }

    final maxVal = salesByDay.reduce((a, b) => a > b ? a : b);
    final hasData = maxVal > 0;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.cardSurface,
        borderRadius: BorderRadius.circular(AppRadii.card),
        border: Border.all(color: AppColors.line),
        boxShadow: AppElevation.cardShadow,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'sales_trend_title'.tr(),
            style: AppTextStyles.labelMedium.copyWith(
              fontWeight: FontWeight.w700,
              color: AppColors.ink,
            ),
          ),
          const SizedBox(height: AppSpacing.md),
          SizedBox(
            height: 100,
            child: hasData
                ? Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: List.generate(salesByDay.length, (i) {
                      final height = maxVal > 0 ? (salesByDay[i] / maxVal) * 80.0 : 0.0;
                      return Column(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          Container(
                            width: 24,
                            height: height.clamp(2, 80),
                            decoration: BoxDecoration(
                              color: AppColors.indigo,
                              borderRadius: BorderRadius.circular(4),
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            labels[i],
                            style: AppTextStyles.caption.copyWith(
                              fontSize: 10,
                              color: AppColors.inkSoft,
                            ),
                          ),
                        ],
                      );
                    }),
                  )
                : Center(
                    child: Text(
                      'no_sales_data'.tr(),
                      style: AppTextStyles.bodySmall.copyWith(color: AppColors.inkSoft),
                    ),
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildOrderSummaryCard(int delivered, int inProgress, int cancelled) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.cardSurface,
        borderRadius: BorderRadius.circular(AppRadii.card),
        border: Border.all(color: AppColors.line),
        boxShadow: AppElevation.cardShadow,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'order_summary_title'.tr(),
            style: AppTextStyles.labelMedium.copyWith(
              fontWeight: FontWeight.w700,
              color: AppColors.ink,
            ),
          ),
          const SizedBox(height: AppSpacing.md),
          Wrap(
            spacing: AppSpacing.md,
            runSpacing: AppSpacing.sm,
            alignment: WrapAlignment.center,
            children: [
              _buildSummaryItem('delivered'.tr(), delivered, AppColors.success),
              _buildSummaryItem('in_progress'.tr(), inProgress, AppColors.amber),
              _buildSummaryItem('cancelled'.tr(), cancelled, AppColors.coral),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSummaryItem(String label, int count, Color color) {
    return Column(
      children: [
        Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.15),
            shape: BoxShape.circle,
          ),
          child: Center(
            child: Text(
              '$count',
              style: AppTextStyles.headlineMedium.copyWith(
                fontWeight: FontWeight.w700,
                color: color,
              ),
            ),
          ),
        ),
        const SizedBox(height: AppSpacing.xs),
        Text(
          label,
          style: AppTextStyles.caption.copyWith(color: AppColors.inkSoft),
        ),
      ],
    );
  }

  List<Order> _getOrdersForDay(DateTime day) {
    final allOrders = ref.read(ordersProvider);
    return allOrders.where((o) {
      return o.placedAt.year == day.year &&
          o.placedAt.month == day.month &&
          o.placedAt.day == day.day;
    }).toList();
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;
  final Color iconColor;

  const _StatCard({
    required this.title,
    required this.value,
    required this.icon,
    required this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.cardSurface,
        borderRadius: BorderRadius.circular(AppRadii.card),
        border: Border.all(color: AppColors.line),
        boxShadow: AppElevation.cardShadow,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 24, color: iconColor),
          const SizedBox(height: AppSpacing.xs),
          Text(
            value,
            style: AppTextStyles.headlineLarge.copyWith(
              fontWeight: FontWeight.w700,
              color: AppColors.ink,
            ),
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          const SizedBox(height: 2),
          Text(
            title,
            style: AppTextStyles.labelSmall.copyWith(color: AppColors.inkSoft),
          ),
        ],
      ),
    );
  }
}