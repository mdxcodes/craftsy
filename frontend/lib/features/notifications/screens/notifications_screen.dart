import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/services/app_tts_service.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../../../core/widgets/speaker_affordance.dart';
import '../../../core/providers/app_providers.dart';

class NotificationsScreen extends ConsumerStatefulWidget {
  const NotificationsScreen({super.key});

  @override
  ConsumerState<NotificationsScreen> createState() =>
      _NotificationsScreenState();
}

class _NotificationsScreenState extends ConsumerState<NotificationsScreen> {
  // One shared engine for the whole list rather than one per card — a
  // notification list can be long, and only one item speaks at a time.
  final AppTtsService _tts = AppTtsService();
  String? _speakingId;

  @override
  void initState() {
    super.initState();
    // Mark all as read when this screen opens.
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(notificationsProvider.notifier).markAllRead();
    });
    _tts.onStateChanged = () {
      if (!_tts.isSpeaking && mounted) setState(() => _speakingId = null);
    };
  }

  @override
  void dispose() {
    _tts.dispose();
    super.dispose();
  }

  Future<void> _speakNotification(
    String id,
    String message,
    DateTime at,
  ) async {
    if (_speakingId == id) {
      await _tts.stop();
      setState(() => _speakingId = null);
      return;
    }

    // The card shows the message *and* how long ago it arrived, and the age
    // is often the part that decides whether it still needs acting on. Read
    // it out too, or someone listening gets only half the card.
    final isHindi = context.locale.languageCode == 'hi';
    final result = await _tts.speak(
      '$message ${_spokenTime(at, isHindi)}',
      languageCode: context.locale.languageCode,
    );

    if (result == TtsResult.spoke) {
      setState(() => _speakingId = id);
    } else if (result == TtsResult.voiceUnavailable && mounted) {
      final opened = await _tts.openVoiceDownloadScreen();
      if (!opened && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('voice_download_settings_hint'.tr())),
        );
      }
    }
  }

  (IconData, Color) _iconAndColorFor(NotificationType type) {
    switch (type) {
      case NotificationType.listingLive:
        return (Icons.check_circle, AppColors.sage);
      case NotificationType.pendingSync:
        return (Icons.cloud_queue, AppColors.burgundy);
      case NotificationType.buyerView:
        return (Icons.visibility, AppColors.burgundy);
      case NotificationType.priceSuggestion:
        return (Icons.trending_up, AppColors.gold);
      case NotificationType.newOrder:
        return (Icons.receipt_long, AppColors.burgundyDark);
    }
  }

  String _actionLabelFor(NotificationType type) {
    switch (type) {
      case NotificationType.listingLive:
        return 'notif_action_view_listing'.tr();
      case NotificationType.pendingSync:
        return 'notif_action_view_drafts'.tr();
      case NotificationType.buyerView:
        return 'notif_action_view_product'.tr();
      case NotificationType.priceSuggestion:
        return 'notif_action_view_suggestion'.tr();
      case NotificationType.newOrder:
        return 'notif_action_view_order'.tr();
    }
  }

  String _actionRouteFor(NotificationType type) {
    switch (type) {
      case NotificationType.listingLive:
        return '/catalogue';
      case NotificationType.pendingSync:
        return '/catalogue';
      case NotificationType.buyerView:
        return '/catalogue';
      case NotificationType.priceSuggestion:
        return '/catalogue';
      case NotificationType.newOrder:
        return '/orders';
    }
  }

  String _relativeTime(DateTime t) {
    final diff = DateTime.now().difference(t);
    if (diff.inMinutes < 60) return '${diff.inMinutes}m ago';
    if (diff.inHours < 24) return '${diff.inHours}h ago';
    return '${diff.inDays}d ago';
  }

  /// Same age as [_relativeTime], written out in full words. The abbreviated
  /// on-screen form is unusable as speech — TTS reads "2h ago" as "two aitch
  /// ago".
  String _spokenTime(DateTime t, bool isHindi) {
    final diff = DateTime.now().difference(t);
    if (diff.inMinutes < 1) return isHindi ? 'अभी अभी।' : 'Just now.';
    if (diff.inMinutes < 60) {
      final n = diff.inMinutes;
      return isHindi ? '$n मिनट पहले।' : '$n minute${n == 1 ? '' : 's'} ago.';
    }
    if (diff.inHours < 24) {
      final n = diff.inHours;
      return isHindi ? '$n घंटे पहले।' : '$n hour${n == 1 ? '' : 's'} ago.';
    }
    final n = diff.inDays;
    return isHindi ? '$n दिन पहले।' : '$n day${n == 1 ? '' : 's'} ago.';
  }

  @override
  Widget build(BuildContext context) {
    final notifications = ref.watch(notificationsProvider);

    return AppScaffold(
      title: 'notifications_title'.tr(),
      showNotificationBell:
          false, // Already on this screen — don't show bell again
      body: notifications.isEmpty
          ? Center(
              child: Padding(
                padding: const EdgeInsets.all(AppSpacing.screenPadding),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.notifications_none,
                      size: 56,
                      color: AppColors.taupe,
                    ),
                    const SizedBox(height: AppSpacing.md),
                    Text(
                      'no_notifications_title'.tr(),
                      style: AppTextStyles.headlineMedium,
                    ),
                    const SizedBox(height: AppSpacing.sm),
                    Text(
                      'notif_local_only'.tr(),
                      style: AppTextStyles.bodySmall.copyWith(
                        color: AppColors.taupe,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            )
          : Column(
              children: [
                // Honest local-only notice
                Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.screenPadding,
                    vertical: AppSpacing.xs,
                  ),
                  child: Semantics(
                    label: 'notif_local_only'.tr(),
                    child: Text(
                      'notif_local_only'.tr(),
                      style: AppTextStyles.caption.copyWith(
                        color: AppColors.taupe,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
                Expanded(
                  child: ListView.separated(
                    padding: const EdgeInsets.all(AppSpacing.screenPadding),
                    itemCount: notifications.length,
                    separatorBuilder: (_, _) =>
                        const SizedBox(height: AppSpacing.sm),
                    itemBuilder: (context, index) {
                      final item = notifications[index];
                      final (icon, color) = _iconAndColorFor(item.type);
                      final actionLabel = _actionLabelFor(item.type);
                      final actionRoute = _actionRouteFor(item.type);
                      return Semantics(
                        label:
                            '${item.messageKey.tr()}, ${_relativeTime(item.timestamp)}',
                        child: Container(
                          padding: const EdgeInsets.all(AppSpacing.md),
                          decoration: BoxDecoration(
                            color: AppColors.cardSurface,
                            borderRadius: BorderRadius.circular(AppRadii.card),
                            border: Border.all(
                              color: AppColors.warmStone,
                              width: 0.6,
                            ),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Container(
                                    padding: const EdgeInsets.all(
                                      AppSpacing.sm,
                                    ),
                                    decoration: BoxDecoration(
                                      color: color.withValues(alpha: 0.14),
                                      shape: BoxShape.circle,
                                    ),
                                    child: Icon(
                                      icon,
                                      color: color,
                                      size: AppSpacing.iconSize,
                                    ),
                                  ),
                                  const SizedBox(width: AppSpacing.md),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment:
                                          CrossAxisAlignment.start,
                                      children: [
                                        Text(
                                          item.messageKey.tr(),
                                          style: AppTextStyles.bodyMedium,
                                        ),
                                        const SizedBox(height: 4),
                                        Text(
                                          _relativeTime(item.timestamp),
                                          style: AppTextStyles.caption,
                                        ),
                                      ],
                                    ),
                                  ),
                                  SpeakerAffordance.compact(
                                    isSpeaking: _speakingId == item.id,
                                    onTap: () => _speakNotification(
                                      item.id,
                                      item.messageKey.tr(),
                                      item.timestamp,
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: AppSpacing.sm),
                              Row(
                                mainAxisAlignment: MainAxisAlignment.end,
                                children: [
                                  Semantics(
                                    button: true,
                                    label: actionLabel,
                                    child: TextButton(
                                      onPressed: () =>
                                          context.push(actionRoute),
                                      style: TextButton.styleFrom(
                                        minimumSize: const Size(88, 48),
                                      ),
                                      child: Text(actionLabel),
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
    );
  }
}
