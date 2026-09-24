import '../../features/orders/models/order.dart';
import '../../data/models/product.dart';
import 'widget_data_bridge.dart';

/// Maps existing Craftsy domain models to widget-safe snapshots.
///
/// This is the ONLY place where domain models are projected
/// into widget snapshot format. Widgets never see domain models directly.
class WidgetDataProjection {

  /// "Needs attention" = order status is newOrder, packed, or shipped.
  /// These are states where the artisan needs to take action.
  static bool _isOrderActionable(Order order) {
    return order.status == OrderStatus.newOrder ||
        order.status == OrderStatus.packed ||
        order.status == OrderStatus.shipped;
  }

  /// Get the required action label for an actionable order.
  static String? _getRequiredAction(Order order) {
    switch (order.status) {
      case OrderStatus.newOrder:
        return 'Confirm order';
      case OrderStatus.packed:
        return 'Ship today';
      case OrderStatus.shipped:
        return 'Track delivery';
      case OrderStatus.delivered:
        return null;
      case OrderStatus.cancelled:
        return null;
    }
  }

  /// Project a domain Order to a widget-safe summary.
  static WidgetOrderSummary projectOrder(Order order) {
    return WidgetOrderSummary(
      orderId: order.id,
      status: order.status.name,
      statusLabel: order.status.labelKey,
      productTitle: order.productTitle,
      requiredAction: _getRequiredAction(order),
      deepLink: '/orders/${order.id}',
    );
  }

  /// Project a domain Product to a widget-safe stock item.
  ///
  /// IMPORTANT: No low-stock threshold is defined yet in Craftsy.
  /// We expose stockQuantity and stockState, but the threshold
  /// rule must come from the backend. For now:
  /// - stock == 0 → OUT_OF_STOCK
  /// - stock > 0 → IN_STOCK
  ///
  /// Low-stock (LOW) state is reserved for when the backend defines
  /// an authoritative threshold.
  static WidgetStockItem projectStockItem(Product product) {
    final stockState = product.stock == 0
        ? 'OUT_OF_STOCK'
        : 'IN_STOCK';

    return WidgetStockItem(
      productId: product.id,
      productName: product.title,
      stockQuantity: product.stock,
      stockState: stockState,
      deepLink: '/product/${product.id}',
    );
  }

  /// Build the Today snapshot from domain data.
  static TodaySnapshot projectToday({
    required List<Order> orders,
    required List<Product> products,
    required bool channelsNeedAttention,
  }) {
    final actionableOrders = orders.where(_isOrderActionable).toList();
    final outOfStock = products.where((p) => p.stock == 0).toList();

    final items = <ActionableItem>[];

    // Add actionable orders
    for (final order in actionableOrders) {
      items.add(ActionableItem(
        type: 'ORDER',
        id: order.id,
        title: order.productTitle,
        subtitle: _getRequiredAction(order),
        deepLink: '/orders/${order.id}',
      ));
    }

    // Add stock alerts
    for (final product in outOfStock) {
      items.add(ActionableItem(
        type: 'STOCK',
        id: product.id,
        title: product.title,
        subtitle: 'Out of stock',
        deepLink: '/product/${product.id}',
      ));
    }

    // Add channel attention if needed
    if (channelsNeedAttention) {
      items.add(ActionableItem(
        type: 'CHANNEL',
        id: 'channels',
        title: 'Selling channels',
        subtitle: 'Needs attention',
        deepLink: '/commerce-hub',
      ));
    }

    return TodaySnapshot(
      attentionCount: items.length,
      orderAttentionCount: actionableOrders.length,
      stockAttentionCount: outOfStock.length,
      channelAttentionCount: channelsNeedAttention ? 1 : 0,
      actionableItems: items,
    );
  }

  /// Build the Orders snapshot from domain data.
  static OrdersSnapshot projectOrders(List<Order> orders) {
    final actionable = orders.where(_isOrderActionable).toList();
    return OrdersSnapshot(
      actionableCount: actionable.length,
      items: actionable.map(projectOrder).toList(),
    );
  }

  /// Build the Stock snapshot from domain data.
  static StockSnapshot projectStockSnapshot(List<Product> products) {
    final stockItems = products
        .map(projectStockItem)
        .toList();

    final outOfStockCount = stockItems
        .where((i) => i.stockState == 'OUT_OF_STOCK')
        .length;

    return StockSnapshot(
      outOfStockCount: outOfStockCount,
      lowStockCount: 0, // No threshold defined yet
      items: stockItems,
    );
  }

  /// Build the Channels snapshot from existing commerce state.
  ///
  /// IMPORTANT: ONDC and GeM are NOT connected. They show
  /// NOT_CONFIGURED. Only Craftsy channel can be ACTIVE.
  static ChannelsSnapshot projectChannels({
    bool ondcConnected = false,
    bool governmentConnected = false,
  }) {
    return ChannelsSnapshot(
      craftsy: const ChannelStatus(
        channelName: 'Craftsy',
        state: 'ACTIVE',
        stateLabel: 'Active',
        detail: 'Your marketplace is live',
        deepLink: '/catalogue',
      ),
      ondc: ChannelStatus(
        channelName: 'ONDC',
        state: ondcConnected ? 'READY' : 'NOT_CONFIGURED',
        stateLabel: ondcConnected ? 'Ready' : 'Not configured',
        detail: ondcConnected ? null : 'Setup required to sell on ONDC',
        deepLink: '/commerce-hub',
      ),
      government: ChannelStatus(
        channelName: 'Government',
        state: governmentConnected ? 'PREPARATION_NEEDED' : 'NOT_CONFIGURED',
        stateLabel: governmentConnected
            ? 'Preparation needed'
            : 'Not configured',
        detail: governmentConnected
            ? 'Guided workflow available'
            : 'Setup required to sell to government',
        deepLink: '/commerce-hub',
      ),
    );
  }

  /// Build the CraftMitra snapshot.
  /// CraftMitra is always available — the widget is just a launcher.
  static CraftMitraSnapshot projectCraftMitra() {
    return const CraftMitraSnapshot(
      available: true,
      voiceModeAvailable: true,
      textModeAvailable: true,
      voiceDeepLink: '/assistant?mode=voice',
      textDeepLink: '/assistant?mode=text',
    );
  }
}
