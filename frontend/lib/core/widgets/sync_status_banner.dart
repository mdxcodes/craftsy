import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import '../providers/app_providers.dart';
import '../services/app_tts_service.dart';
import '../theme/app_colors.dart';
import '../theme/app_spacing.dart';
import '../theme/app_text_styles.dart';
import '../widgets/app_button.dart';
import '../offline_sync/models/queue_item.dart';
import '../offline_sync/offline_sync_service.dart';

/// Aggregated sync queue banner shown on Home.
///
/// Displays a single summarized line when there are pending/processing items:
///   "☁️ 3 items pending — Craftsy will send them when internet returns"
///
/// Expands to show item details on tap.
class SyncStatusBanner extends ConsumerStatefulWidget {
  const SyncStatusBanner({super.key});

  @override
  ConsumerState<SyncStatusBanner> createState() => _SyncStatusBannerState();
}

class _SyncStatusBannerState extends ConsumerState<SyncStatusBanner> {
  bool _expanded = false;
  final _ttsService = AppTtsService();

  @override
  void dispose() {
    _ttsService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isOnline = ref.watch(connectivityProvider).value ?? true;
    final queueAsync = ref.watch(syncQueueProvider);

    return queueAsync.when(
      loading: () => const SizedBox.shrink(),
      error: (_, __) => const SizedBox.shrink(),
      data: (items) {
        if (items.isEmpty) return const SizedBox.shrink();

        final pendingCount = items.where((i) => i.status == QueueStatus.pending).length;
        final processingCount = items.where((i) => i.status == QueueStatus.uploading || i.status == QueueStatus.processing).length;
        final failedCount = items.where((i) => i.status == QueueStatus.failed).length;
        final completedCount = items.where((i) => i.status == QueueStatus.completed).length;

        // Only show pending/processing/failed — not completed
        final activeCount = pendingCount + processingCount + failedCount;
        if (activeCount == 0) return const SizedBox.shrink();

        String statusLabel;
        IconData statusIcon;
        Color statusColor;

        if (failedCount > 0) {
          statusLabel = 'sync_failed_status'.tr(namedArgs: {'count': '$failedCount'});
          statusIcon = Icons.error_outline_rounded;
          statusColor = AppColors.coral;
        } else if (processingCount > 0) {
          statusLabel = 'syncing_status'.tr(namedArgs: {'count': '$processingCount'});
          statusIcon = Icons.sync_rounded;
          statusColor = AppColors.amber;
        } else {
          statusLabel = 'sync_pending_status'.tr(namedArgs: {'count': '$pendingCount'});
          statusIcon = Icons.cloud_queue_rounded;
          statusColor = AppColors.indigo;
        }

        return Semantics(
          liveRegion: true,
          label: statusLabel,
          child: Container(
            margin: const EdgeInsets.only(bottom: AppSpacing.md),
            decoration: BoxDecoration(
              color: statusColor.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(AppRadii.card),
              border: Border.all(color: statusColor.withValues(alpha: 0.3)),
            ),
            child: Column(
              children: [
                InkWell(
                  onTap: () {
                    setState(() => _expanded = !_expanded);
                    _ttsService.speak(statusLabel, languageCode: context.locale.languageCode);
                  },
                  borderRadius: BorderRadius.circular(AppRadii.card),
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.md,
                      vertical: AppSpacing.sm + 2,
                    ),
                    child: Row(
                      children: [
                        Icon(statusIcon, size: 20, color: statusColor),
                        const SizedBox(width: AppSpacing.sm),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                statusLabel,
                                style: AppTextStyles.bodySmall.copyWith(
                                  color: statusColor,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                              if (!_expanded)
                                Text(
                                  'sync_tap_to_expand'.tr(),
                                  style: AppTextStyles.caption.copyWith(
                                    color: AppColors.inkFaint,
                                  ),
                                ),
                            ],
                          ),
                        ),
                        Icon(
                          _expanded ? Icons.expand_less : Icons.expand_more,
                          color: statusColor,
                          size: 20,
                        ),
                      ],
                    ),
                  ),
                ),
                if (_expanded) ...[
                  const Divider(height: 1, color: AppColors.divider),
                  Padding(
                    padding: const EdgeInsets.all(AppSpacing.md),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        if (pendingCount > 0)
                          _QueueItemRow(
                            icon: Icons.cloud_queue_rounded,
                            label: 'queue_pending'.tr(),
                            count: pendingCount,
                            color: AppColors.indigo,
                          ),
                        if (processingCount > 0)
                          _QueueItemRow(
                            icon: Icons.sync_rounded,
                            label: 'queue_processing'.tr(),
                            count: processingCount,
                            color: AppColors.amber,
                          ),
                        if (failedCount > 0)
                          _QueueItemRow(
                            icon: Icons.error_outline_rounded,
                            label: 'queue_failed'.tr(),
                            count: failedCount,
                            color: AppColors.coral,
                          ),
                        if (completedCount > 0)
                          _QueueItemRow(
                            icon: Icons.check_circle_outline_rounded,
                            label: 'queue_completed'.tr(),
                            count: completedCount,
                            color: AppColors.teal,
                          ),
                        const SizedBox(height: AppSpacing.sm),
                        if (failedCount > 0 && isOnline)
                          AppButton(
                            label: 'retry_all'.tr(),
                            icon: Icons.refresh_rounded,
                            type: AppButtonType.secondary,
                            onPressed: () {
                              OfflineSyncService.instance.retryAll();
                            },
                          ),
                        if (failedCount > 0 && !isOnline)
                          Text(
                            'sync_retry_when_online'.tr(),
                            style: AppTextStyles.caption.copyWith(
                              color: AppColors.inkFaint,
                            ),
                            textAlign: TextAlign.center,
                          ),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }
}

class _QueueItemRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final int count;
  final Color color;

  const _QueueItemRow({
    required this.icon,
    required this.label,
    required this.count,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.xs),
      child: Row(
        children: [
          Icon(icon, size: 16, color: color),
          const SizedBox(width: AppSpacing.xs),
          Expanded(
            child: Text(
              label.tr(),
              style: AppTextStyles.bodySmall,
            ),
          ),
          Text(
            '$count',
            style: AppTextStyles.labelMedium.copyWith(color: color),
          ),
        ],
      ),
    );
  }
}
