import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/models/commerce_hub_models.dart';
import '../../../core/providers/commerce_hub_provider.dart';
import '../../../core/theme/app_colors.dart';
import '../widgets/commerce_summary_card.dart';
import '../widgets/inventory_overview_card.dart';
import '../widgets/order_channel_summary_card.dart';
import '../../orders/screens/unified_orders_screen.dart';

/// Unified Commerce Hub Dashboard.
///
/// Shows a single view of all commerce operations across channels:
/// - Commerce summary (products, orders, channels)
/// - Product list with channel statuses
/// - Order summary by channel
/// - Inventory overview
class UnifiedCommerceHubScreen extends ConsumerStatefulWidget {
  final String artisanId;

  const UnifiedCommerceHubScreen({super.key, required this.artisanId});

  @override
  ConsumerState<UnifiedCommerceHubScreen> createState() =>
      _UnifiedCommerceHubScreenState();
}

class _UnifiedCommerceHubScreenState
    extends ConsumerState<UnifiedCommerceHubScreen> {
  int _selectedTab = 0;

  @override
  Widget build(BuildContext context) {
    final summaryAsync = ref.watch(commerceSummaryProvider(widget.artisanId));

    return Scaffold(
      appBar: AppBar(
        title: Text('commerce_hub_title'.tr()),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              ref.invalidate(commerceSummaryProvider(widget.artisanId));
              ref.invalidate(unifiedOrdersProvider(widget.artisanId));
            },
          ),
        ],
        bottom: TabBar(
          isScrollable: true,
          onTap: (index) => setState(() => _selectedTab = index),
          tabs: [
            Tab(text: 'commerce_hub_overview'.tr()),
            Tab(text: 'commerce_hub_products'.tr()),
            Tab(text: 'commerce_hub_orders'.tr()),
            Tab(text: 'commerce_hub_inventory'.tr()),
          ],
        ),
      ),
      body: summaryAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.error_outline, size: 48, color: AppColors.coral),
              const SizedBox(height: 16),
              Text('commerce_hub_error'.tr()),
              const SizedBox(height: 8),
              Text(
                error.toString(),
                style: Theme.of(context).textTheme.bodySmall,
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
        data: (summary) => IndexedStack(
          index: _selectedTab,
          children: [
            _buildOverviewTab(summary),
            _buildProductsTab(),
            _buildOrdersTab(),
            _buildInventoryTab(),
          ],
        ),
      ),
    );
  }

  Widget _buildOverviewTab(CommerceSummary summary) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          CommerceSummaryCard(summary: summary),
          const SizedBox(height: 16),
          OrderChannelSummaryCard(artisanId: widget.artisanId),
          const SizedBox(height: 16),
          InventoryOverviewCard(summary: summary),
        ],
      ),
    );
  }

  Widget _buildProductsTab() {
    return const Center(child: Text('Products list with channel statuses'));
  }

  Widget _buildOrdersTab() {
    return UnifiedOrdersScreen(artisanId: widget.artisanId);
  }

  Widget _buildInventoryTab() {
    return const Center(child: Text('Inventory overview'));
  }
}
