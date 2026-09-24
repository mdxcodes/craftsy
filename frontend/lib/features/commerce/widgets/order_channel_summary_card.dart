import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/models/commerce_hub_models.dart';
import '../../../core/providers/commerce_hub_provider.dart';

/// Order summary grouped by channel.
class OrderChannelSummaryCard extends ConsumerWidget {
  final String artisanId;

  const OrderChannelSummaryCard({super.key, required this.artisanId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final summaryAsync = ref.watch(orderChannelSummaryProvider(artisanId));

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Orders by Channel'.tr(),
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            summaryAsync.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (error, stack) => Text('Error: $error'),
              data: (summaries) {
                if (summaries.isEmpty) {
                  return Text('No orders yet'.tr());
                }
                return Column(
                  children: summaries
                      .map((s) => _buildChannelRow(context, s))
                      .toList(),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChannelRow(BuildContext context, OrderChannelSummary summary) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(_channelLabel(summary.channel)),
          Text('${summary.total}'),
        ],
      ),
    );
  }

  String _channelLabel(String channel) {
    switch (channel) {
      case 'craftsy':
        return 'Craftsy Marketplace';
      case 'ondc':
        return 'ONDC';
      case 'gem':
        return 'GeM';
      default:
        return channel;
    }
  }
}
