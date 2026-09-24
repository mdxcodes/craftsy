import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/router/app_route_constants.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../../../core/widgets/app_image.dart';
import '../../../core/widgets/motifs/empty_craft_state.dart';
import '../../../core/widgets/motifs/craft_category_badge.dart';
import '../../../core/widgets/speaker_affordance.dart';
import '../../../core/services/app_tts_service.dart';
import '../../../core/services/tts_page_guides.dart';
import '../models/order.dart';
import '../providers/orders_provider.dart';
import '../services/label_maker_service.dart';

/// Unified Orders Screen — shows orders from all channels (Craftsy, ONDC, GeM).
///
/// Provides channel filtering and a single inbox for all orders.
class UnifiedOrdersScreen extends ConsumerStatefulWidget {
  final String? artisanId;

  const UnifiedOrdersScreen({super.key, this.artisanId});

  @override
  ConsumerState<UnifiedOrdersScreen> createState() => _UnifiedOrdersScreenState();
}

class _UnifiedOrdersScreenState extends ConsumerState<UnifiedOrdersScreen> {
  String? _selectedChannelFilter;

  @override
  Widget build(BuildContext context) {
    final orders = ref.watch(filteredOrdersProvider);
    final selectedFilter = ref.watch(selectedOrderFilterProvider);

    // If we have an artisanId, also fetch from commerce hub
    // final hubOrdersAsync = widget.artisanId != null
    //     ? ref.watch(unifiedOrdersProvider(widget.artisanId!))
    //     : null;

    return AppScaffold(
      title: 'unified_orders_title'.tr(),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Channel filter pills
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.screenPadding,
              vertical: AppSpacing.sm,
            ),
            child: Row(
              children: [
                _FilterChip(
                  label: 'unified_orders_all'.tr(),
                  selected: _selectedChannelFilter == null,
                  onTap: () => setState(() => _selectedChannelFilter = null),
                ),
                const SizedBox(width: AppSpacing.sm),
                _FilterChip(
                  label: 'unified_orders_craftsy'.tr(),
                  selected: _selectedChannelFilter == 'craftsy',
                  onTap: () => setState(() => _selectedChannelFilter = 'craftsy'),
                ),
                const SizedBox(width: AppSpacing.sm),
                _FilterChip(
                  label: 'unified_orders_ondc'.tr(),
                  selected: _selectedChannelFilter == 'ondc',
                  onTap: () => setState(() => _selectedChannelFilter = 'ondc'),
                ),
                const SizedBox(width: AppSpacing.sm),
                _FilterChip(
                  label: 'unified_orders_gem'.tr(),
                  selected: _selectedChannelFilter == 'gem',
                  onTap: () => setState(() => _selectedChannelFilter = 'gem'),
                ),
              ],
            ),
          ),

          // Orders list
          Expanded(
            child: _buildOrdersList(orders, selectedFilter),
          ),
        ],
      ),
    );
  }

  Widget _buildOrdersList(List<Order> orders, OrderStatus? selectedFilter) {
    // Apply channel filter
    List<Order> filteredOrders = orders;
    if (_selectedChannelFilter != null) {
      filteredOrders = orders
          .where((o) => o.channel == _selectedChannelFilter)
          .toList();
    }

    if (filteredOrders.isEmpty) {
      return _EmptyOrders(
        channel: _selectedChannelFilter,
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.screenPadding,
        vertical: AppSpacing.xs,
      ),
      itemCount: filteredOrders.length,
      itemBuilder: (context, index) {
        final order = filteredOrders[index];
        return _UnifiedOrderCard(
          order: order,
          onTap: () {
            context.pushNamed(
              AppRouteConstants.orderDetail,
              pathParameters: {'orderId': order.id},
              extra: order,
            );
          },
          onStatusAdvance: () {
            final next = order.status.next;
            if (next != null) {
              ref.read(ordersProvider.notifier).updateStatus(order.id, next);
              LabelMakerService.invalidateCache(order.id);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                    'status_updated_to'.tr(namedArgs: {'status': next.labelKey.tr()}),
                  ),
                  backgroundColor: AppColors.indigo,
                  duration: const Duration(seconds: 2),
                ),
              );
            }
          },
        );
      },
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;

  const _FilterChip({
    required this.label,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return ChoiceChip(
      label: Text(
        label,
        style: AppTextStyles.labelSmall.copyWith(
          color: selected ? AppColors.textOnPrimary : AppColors.inkSoft,
          fontWeight: FontWeight.w700,
          fontSize: 12.5,
        ),
      ),
      selected: selected,
      onSelected: (_) => onTap(),
      showCheckmark: false,
      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
      visualDensity: VisualDensity.compact,
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      backgroundColor: AppColors.cardSurface,
      selectedColor: AppColors.indigo,
      side: BorderSide(
        color: selected ? AppColors.indigo : AppColors.line,
        width: 1.5,
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppRadii.chip),
      ),
    );
  }
}

class _UnifiedOrderCard extends StatefulWidget {
  final Order order;
  final VoidCallback onTap;
  final VoidCallback onStatusAdvance;

  const _UnifiedOrderCard({
    required this.order,
    required this.onTap,
    required this.onStatusAdvance,
  });

  @override
  State<_UnifiedOrderCard> createState() => _UnifiedOrderCardState();
}

class _UnifiedOrderCardState extends State<_UnifiedOrderCard> {
  final AppTtsService _tts = AppTtsService();

  @override
  void initState() {
    super.initState();
    _tts.onStateChanged = () {
      if (mounted) setState(() {});
    };
  }

  @override
  void dispose() {
    _tts.dispose();
    super.dispose();
  }

  Future<void> _speakSummary() async {
    if (_tts.isSpeaking) {
      await _tts.stop();
      return;
    }
    final order = widget.order;
    final locale = Localizations.maybeLocaleOf(context)?.languageCode ?? 'en';
    final isHindi = locale == 'hi';
    final lead = TtsPageGuides.orderCardLead.forLanguage(locale);

    final productTitle = (isHindi && order.productTitleHi != null)
        ? order.productTitleHi!
        : order.productTitle;

    final channelLabel = _channelLabel(order.channel, isHindi);

    final summary = isHindi
        ? '$productTitle का ऑर्डर, ${order.buyerCity} से '
            '${order.buyerName} की ओर से। राशि '
            '${order.amount.toStringAsFixed(0)} रुपये। चैनल: $channelLabel। '
            'स्थिति: ${order.status.labelKey.tr()}।'
        : 'Order for ${order.productTitle}, from ${order.buyerName} in '
            '${order.buyerCity}. Amount: ${order.amount.toStringAsFixed(0)} '
            'rupees. Channel: $channelLabel. Status: ${order.status.labelKey.tr()}.';

    final result = await _tts.speak(
      lead + summary,
      languageCode: context.locale.languageCode,
    );

    if (result == TtsResult.voiceUnavailable && mounted) {
      final opened = await _tts.openVoiceDownloadScreen();
      if (!opened && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('voice_download_settings_hint'.tr()),
          ),
        );
      }
    }
  }

  String _channelLabel(String channel, bool isHindi) {
    switch (channel) {
      case 'ondc':
        return 'ONDC';
      case 'gem':
        return isHindi ? 'सरकार' : 'Government';
      case 'craftsy':
      default:
        return 'Craftsy';
    }
  }

  @override
  Widget build(BuildContext context) {
    final order = widget.order;
    final onTap = widget.onTap;
    final onStatusAdvance = widget.onStatusAdvance;
    final canAdvance = order.status.next != null;
    final isHindi = (Localizations.maybeLocaleOf(context)?.languageCode ??
            'en') ==
        'hi';
    final displayProductTitle = (isHindi && order.productTitleHi != null)
        ? order.productTitleHi!
        : order.productTitle;

    return Dismissible(
      key: ValueKey('${order.id}_${order.status}_${order.channel}'),
      direction: canAdvance ? DismissDirection.startToEnd : DismissDirection.none,
      background: Container(
        margin: const EdgeInsets.only(bottom: AppSpacing.itemSpacing),
        decoration: BoxDecoration(
          color: AppColors.indigoLight,
          borderRadius: BorderRadius.circular(AppRadii.card),
        ),
        alignment: Alignment.centerLeft,
        padding: const EdgeInsets.only(left: AppSpacing.lg),
        child: Row(
          children: [
            const Icon(Icons.arrow_forward, color: AppColors.indigoDark),
            const SizedBox(width: AppSpacing.xs),
            Text(
              'mark_as_status'.tr(namedArgs: {
                'status': order.status.next?.labelKey.tr() ?? '',
              }),
              style: AppTextStyles.labelSmall.copyWith(color: AppColors.indigoDark),
            ),
          ],
        ),
      ),
      confirmDismiss: (_) async {
        onStatusAdvance();
        return false;
      },
      child: Container(
        margin: const EdgeInsets.only(bottom: AppSpacing.itemSpacing),
        decoration: BoxDecoration(
          color: AppColors.cardSurface,
          borderRadius: BorderRadius.circular(AppRadii.card),
          border: Border.all(color: AppColors.line, width: 1.0),
          boxShadow: AppElevation.cardShadow,
        ),
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(AppRadii.card),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                // Thumbnail
                Container(
                  width: 64,
                  height: 64,
                  decoration: BoxDecoration(
                    color: AppColors.parchmentDeep,
                    borderRadius: BorderRadius.circular(14),
                  ),
                  clipBehavior: Clip.antiAlias,
                  alignment: Alignment.center,
                  child: order.productImagePath.isNotEmpty
                      ? AppImage(
                          imageUrl: order.productImagePath,
                          width: 64,
                          height: 64,
                          fit: BoxFit.cover,
                        )
                      : _buildCategoryThumb(order.productCategory),
                ),
                const SizedBox(width: 14),

                // Card body
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Row 1: Product name + Channel badge + Status
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Expanded(
                            child: Text(
                              displayProductTitle,
                              style: AppTextStyles.headlineSmall.copyWith(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                                color: AppColors.ink,
                                height: 1.3,
                              ),
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          const SizedBox(width: 6),
                          SpeakerAffordance.compact(
                            isSpeaking: _tts.isSpeaking,
                            onTap: _speakSummary,
                          ),
                          const SizedBox(width: 6),
                          _ChannelBadge(channel: order.channel),
                          const SizedBox(width: 6),
                          _StatusBadge(status: order.status),
                        ],
                      ),
                      const SizedBox(height: 6),

                      // Meta row: User + Location
                      Row(
                        children: [
                          const Icon(Icons.person_outline,
                              size: 14, color: AppColors.inkSoft),
                          const SizedBox(width: 4),
                          Flexible(
                            child: Text(
                              order.buyerName,
                              style: AppTextStyles.bodySmall.copyWith(
                                color: AppColors.inkSoft,
                                fontSize: 13,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          const SizedBox(width: 8),
                          Text('•',
                              style: TextStyle(
                                  color: AppColors.inkFaint, fontSize: 11)),
                          const SizedBox(width: 8),
                          Flexible(
                            child: Text(
                              order.buyerCity,
                              style: AppTextStyles.bodySmall.copyWith(
                                color: AppColors.inkSoft,
                                fontSize: 13,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),

                      // Price row
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          RichText(
                            text: TextSpan(
                              children: [
                                TextSpan(
                                  text: '₹${order.amount.toStringAsFixed(0)}',
                                  style: AppTextStyles.labelMedium.copyWith(
                                    color: AppColors.indigo,
                                    fontWeight: FontWeight.w700,
                                    fontSize: 16,
                                  ),
                                ),
                                if (order.quantity > 1) ...[
                                  const TextSpan(text: ' '),
                                  TextSpan(
                                    text: '× ${order.quantity}',
                                    style: AppTextStyles.bodySmall.copyWith(
                                      color: AppColors.inkSoft,
                                      fontSize: 14,
                                    ),
                                  ),
                                ],
                              ],
                            ),
                          ),
                          Text(
                            _formatDate(order.placedAt),
                            style: AppTextStyles.caption.copyWith(
                              color: AppColors.inkFaint,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildCategoryThumb(String category) {
    final cat = category.toLowerCase();
    if (cat.contains('pot') || cat.contains('clay') || cat.contains('ceramic')) {
      return CustomPaint(
        size: const Size(22, 22),
        painter: CraftCategoryIcons.pottery(color: AppColors.terracottaDark),
      );
    }
    if (cat.contains('silk') || cat.contains('saree') || cat.contains('textile')) {
      return CustomPaint(
        size: const Size(22, 22),
        painter: CraftCategoryIcons.textile(color: AppColors.terracottaDark),
      );
    }
    if (cat.contains('wood') || cat.contains('toy') || cat.contains('carv')) {
      return CustomPaint(
        size: const Size(22, 22),
        painter: CraftCategoryIcons.woodwork(color: AppColors.terracottaDark),
      );
    }
    if (cat.contains('jewel') || cat.contains('metal') || cat.contains('brass')) {
      return CustomPaint(
        size: const Size(22, 22),
        painter: CraftCategoryIcons.jewelry(color: AppColors.terracottaDark),
      );
    }
    return const Icon(Icons.brush, size: 22, color: AppColors.terracottaDark);
  }

  String _formatDate(DateTime dt) {
    final now = DateTime.now();
    final diff = now.difference(dt);
    if (diff.inHours < 24) {
      return 'hours_ago'.tr(namedArgs: {'hours': '${diff.inHours}'});
    }
    if (diff.inDays == 1) return 'yesterday'.tr();
    return '${dt.day}/${dt.month}';
  }
}

class _ChannelBadge extends StatelessWidget {
  final String channel;

  const _ChannelBadge({required this.channel});

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color fg;
    IconData icon;
    String label;

    switch (channel) {
      case 'ondc':
        bg = AppColors.tealLight;
        fg = AppColors.tealDark;
        icon = Icons.public;
        label = 'ONDC';
        break;
      case 'gem':
        bg = AppColors.amberLight;
        fg = AppColors.amberDark;
        icon = Icons.account_balance;
        label = 'Govt';
        break;
      case 'craftsy':
      default:
        bg = AppColors.indigoLight;
        fg = AppColors.indigoDark;
        icon = Icons.shopping_bag_outlined;
        label = 'Craftsy';
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: fg.withValues(alpha: 0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 10, color: fg),
          const SizedBox(width: 3),
          Text(
            label,
            style: AppTextStyles.caption.copyWith(
              color: fg,
              fontSize: 10,
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ),
    );
  }
}

class _StatusBadge extends StatelessWidget {
  final OrderStatus status;

  const _StatusBadge({required this.status});

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color fg;
    IconData icon;

    switch (status) {
      case OrderStatus.newOrder:
        bg = AppColors.amberLight;
        fg = AppColors.amberDark;
        icon = Icons.fiber_new_outlined;
        break;
      case OrderStatus.packed:
        bg = AppColors.indigoLight;
        fg = AppColors.indigoDark;
        icon = Icons.inventory_2_outlined;
        break;
      case OrderStatus.shipped:
        bg = AppColors.tealLight;
        fg = AppColors.tealDark;
        icon = Icons.local_shipping_outlined;
        break;
      case OrderStatus.delivered:
        bg = AppColors.successLight;
        fg = AppColors.teal;
        icon = Icons.check_circle_outline;
        break;
      case OrderStatus.cancelled:
        bg = AppColors.parchmentDeep;
        fg = AppColors.inkSoft;
        icon = Icons.cancel_outlined;
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(AppRadii.chip),
        border: Border.all(color: fg.withValues(alpha: 0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 12, color: fg),
          const SizedBox(width: 4),
          Text(
            status.labelKey.tr(),
            style: AppTextStyles.labelSmall.copyWith(
              color: fg,
              fontSize: 11.5,
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ),
    );
  }
}

class _EmptyOrders extends StatelessWidget {
  final String? channel;

  const _EmptyOrders({this.channel});

  @override
  Widget build(BuildContext context) {
    final String title;
    final String subtitle;

    if (channel == null) {
      title = 'unified_orders_empty'.tr();
      subtitle = 'unified_orders_empty_desc'.tr();
    } else {
      final channelLabel = _channelLabel(channel!);
      title = '$channelLabel ${'unified_orders_empty'.tr()}';
      subtitle = '${'unified_orders_empty_desc'.tr()} $channelLabel';
    }

    return EmptyCraftState(
      title: title,
      subtitle: subtitle,
    );
  }

  String _channelLabel(String channel) {
    switch (channel) {
      case 'ondc':
        return 'ONDC';
      case 'gem':
        return 'Government';
      case 'craftsy':
        return 'Craftsy';
      default:
        return channel;
    }
  }
}
