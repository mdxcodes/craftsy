import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/models/commerce_hub_models.dart';
import '../../../core/providers/commerce_hub_provider.dart';
import '../../../core/theme/app_colors.dart';

/// "Where I Sell" section for product detail screen.
///
/// Shows channel statuses and actions for a product across
/// Craftsy, ONDC, and GeM channels.
class WhereISellSection extends ConsumerWidget {
  final String productId;
  final VoidCallback? onRefresh;

  const WhereISellSection({super.key, required this.productId, this.onRefresh});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final channelsAsync = ref.watch(productChannelsProvider(productId));

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'where_i_sell'.tr(),
              style: Theme.of(
                context,
              ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
            ),
            if (onRefresh != null)
              IconButton(
                icon: const Icon(Icons.refresh, size: 20),
                onPressed: onRefresh,
                tooltip: 'Refresh',
              ),
          ],
        ),
        const SizedBox(height: 8),
        channelsAsync.when(
          loading: () => const Center(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: CircularProgressIndicator(),
            ),
          ),
          error: (error, stack) => Text(
            'Error: $error',
            style: const TextStyle(color: AppColors.sienna),
          ),
          data: (channels) => Column(
            children: channels.map((ch) {
              return _buildChannelItem(context, ref, ch);
            }).toList(),
          ),
        ),
      ],
    );
  }

  Widget _buildChannelItem(
    BuildContext context,
    WidgetRef ref,
    ChannelStatusInfo channel,
  ) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: _channelColor(channel).withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Icon(
                _channelIcon(channel.channel),
                color: _channelColor(channel),
                size: 20,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    _channelLabel(channel.channel),
                    style: const TextStyle(
                      fontWeight: FontWeight.w600,
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    _statusLabel(channel.displayStatus),
                    style: TextStyle(
                      fontSize: 12,
                      color: _channelColor(channel),
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ],
              ),
            ),
            _buildActionButton(context, ref, channel),
          ],
        ),
      ),
    );
  }

  Widget _buildActionButton(
    BuildContext context,
    WidgetRef ref,
    ChannelStatusInfo channel,
  ) {
    final api = ref.read(commerceHubApiProvider);

    if (channel.channel == 'craftsy') {
      // Craftsy is always active — show "Manage" button
      return OutlinedButton(
        onPressed: () {
          // Navigate to product detail (already there)
        },
        style: OutlinedButton.styleFrom(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        ),
        child: Text('channel_manage'.tr()),
      );
    }

    if (channel.isConnected) {
      // Connected — show "View Status" or "Disable"
      return TextButton(
        onPressed: () async {
          await api.disableChannel(productId, channel.channel);
          if (context.mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(
                  '${_channelLabel(channel.channel)} ${'channel_disabled'.tr()}',
                ),
              ),
            );
          }
        },
        child: Text('channel_disable'.tr()),
      );
    }

    // Not connected — show "Enable" or "Complete Setup"
    if (channel.missingRequirements.isNotEmpty) {
      return TextButton(
        onPressed: () {
          // Navigate to complete setup
        },
        child: Text('channel_complete_setup'.tr()),
      );
    }

    return FilledButton(
      onPressed: () async {
        await api.enableChannel(productId, channel.channel);
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(
                '${_channelLabel(channel.channel)} ${'channel_enabled'.tr()}',
              ),
            ),
          );
        }
      },
      style: FilledButton.styleFrom(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      ),
      child: Text('channel_enable'.tr()),
    );
  }

  IconData _channelIcon(String channel) {
    switch (channel) {
      case 'craftsy':
        return Icons.shopping_bag_outlined;
      case 'ondc':
        return Icons.public;
      case 'gem':
        return Icons.account_balance;
      default:
        return Icons.store;
    }
  }

  String _channelLabel(String channel) {
    switch (channel) {
      case 'craftsy':
        return 'Craftsy Marketplace';
      case 'ondc':
        return 'ONDC';
      case 'gem':
        return 'Government Selling';
      default:
        return channel;
    }
  }

  String _statusLabel(String status) {
    // Map display status to localized string
    switch (status.toLowerCase()) {
      case 'active':
      case 'live':
        return 'channel_active'.tr();
      case 'inactive':
        return 'channel_inactive'.tr();
      case 'draft':
        return 'channel_draft'.tr();
      case 'not started':
      case 'not_started':
        return 'channel_not_started'.tr();
      case 'needs information':
      case 'needs_information':
        return 'channel_needs_info'.tr();
      case 'ready':
        return 'channel_ready'.tr();
      case 'problem':
      case 'error':
        return 'channel_problem'.tr();
      default:
        return status;
    }
  }

  Color _channelColor(ChannelStatusInfo channel) {
    if (channel.displayStatus.toLowerCase() == 'active' ||
        channel.displayStatus.toLowerCase() == 'live') {
      return AppColors.success;
    }
    if (channel.displayStatus.toLowerCase() == 'problem' ||
        channel.displayStatus.toLowerCase() == 'error') {
      return AppColors.sienna;
    }
    if (channel.displayStatus.toLowerCase() == 'needs information' ||
        channel.displayStatus.toLowerCase() == 'needs_information') {
      return AppColors.gold;
    }
    if (channel.displayStatus.toLowerCase() == 'not started' ||
        channel.displayStatus.toLowerCase() == 'not_started') {
      return AppColors.inkFaint;
    }
    return AppColors.burgundy;
  }
}
