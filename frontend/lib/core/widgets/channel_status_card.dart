import 'package:flutter/material.dart';
import '../../../core/models/commerce_models.dart';
import '../../../core/theme/app_colors.dart';

/// A card displaying the status of a commerce channel for a product.
///
/// Shows:
/// - Channel icon and name
/// - Current status (Live, Needs Information, etc.)
/// - Missing requirements (if any)
/// - Publish action (if available)
class ChannelStatusCard extends StatelessWidget {
  final ChannelStatus status;
  final VoidCallback? onTap;
  final VoidCallback? onPublish;
  final bool showPublishButton;

  const ChannelStatusCard({
    super.key,
    required this.status,
    this.onTap,
    this.onPublish,
    this.showPublishButton = true,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: '${status.label}: ${status.displayStatus}',
      button: onTap != null,
      child: Card(
        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
          side: BorderSide(
            color: _statusColor.withValues(alpha: 0.3),
            width: 1,
          ),
        ),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                // Channel icon
                Container(
                  width: 44,
                  height: 44,
                  decoration: BoxDecoration(
                    color: _statusColor.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Icon(_channelIcon, color: _statusColor, size: 24),
                ),
                const SizedBox(width: 12),

                // Channel info
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        status.label,
                        style: const TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 2),
                      _buildStatusChip(),
                      if (status.missingRequirements.isNotEmpty) ...[
                        const SizedBox(height: 6),
                        Text(
                          'Missing: ${status.missingRequirements.join(', ')}',
                          style: const TextStyle(
                            fontSize: 12,
                            color: AppColors.textSecondary,
                          ),
                        ),
                      ],
                    ],
                  ),
                ),

                // Publish button
                if (showPublishButton && status.canPublish && onPublish != null)
                  FilledButton(
                    onPressed: onPublish,
                    style: FilledButton.styleFrom(
                      backgroundColor: AppColors.indigo,
                      foregroundColor: AppColors.textOnPrimary,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                    ),
                    child: const Text('Publish'),
                  )
                else if (status.needsInfo)
                  TextButton(onPressed: onTap, child: const Text('Set up')),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildStatusChip() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: _statusColor.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        status.displayStatus,
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w500,
          color: _statusColor,
        ),
      ),
    );
  }

  Color get _statusColor {
    if (status.isLive) return AppColors.success;
    if (status.hasFailed) return AppColors.error;
    if (status.needsInfo) return AppColors.amber;
    if (status.isPending) return AppColors.indigo;
    if (status.isNotConnected) return AppColors.inkFaint;
    return AppColors.inkSoft;
  }

  IconData get _channelIcon {
    switch (status.channel) {
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
}
