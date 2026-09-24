import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/services.dart';
import '../../features/orders/models/order.dart';
import '../../features/orders/providers/orders_provider.dart';
import '../../features/auth/providers/auth_provider.dart';
import '../../core/providers/app_providers.dart';
import '../../data/models/product.dart';
import 'widget_data_bridge.dart';
import 'widget_data_projection.dart';

/// Method channel for widget data communication.
const widgetDataChannel = MethodChannel('com.craftsy.app/widget_data');

/// Provider that builds and sends widget snapshots to Android.
///
/// Watches existing Riverpod state (orders, products, auth) and
/// projects them into widget-safe snapshots via [WidgetDataProjection].
/// Sends snapshots to Android via [WidgetDataBridge].
///
/// This provider does NOT create any new business logic — it only
/// projects existing authoritative state into a widget-safe format.
final widgetSnapshotProvider = Provider<WidgetSnapshot>((ref) {
  // Watch existing state
  final orders = ref.watch(ordersProvider);
  final products = ref.watch(productListProvider);
  final authState = ref.watch(authStateProvider);
  final userProfile = ref.watch(userProfileProvider);

  // Project domain models to widget snapshot
  final productList = products.value ?? const <Product>[];

  final todaySnapshot = WidgetDataProjection.projectToday(
    orders: orders,
    products: productList,
    channelsNeedAttention: false, // TODO: Connect to real channel state
  );

  final ordersSnapshot = WidgetDataProjection.projectOrders(orders);
  final stockSnapshot = WidgetDataProjection.projectStockSnapshot(productList);
  final channelsSnapshot = WidgetDataProjection.projectChannels();
  final craftMitraSnapshot = WidgetDataProjection.projectCraftMitra();

  // Determine data freshness
  final freshness = orders.isNotEmpty || productList.isNotEmpty
      ? 'FRESH'
      : 'UNKNOWN';

  final snapshot = WidgetSnapshot(
    authenticated: authState.isAuthenticated,
    accountId: authState.userId ?? authState.phoneNumber,
    lastUpdated: DateTime.now().millisecondsSinceEpoch,
    dataFreshness: freshness,
    today: todaySnapshot,
    orders: ordersSnapshot,
    stock: stockSnapshot,
    channels: channelsSnapshot,
    craftMitra: craftMitraSnapshot,
  );

  // Send to Android (fire-and-forget, no await)
  // Schedule after frame to avoid sending during build
  Future.microtask(() {
    WidgetDataBridge.sendSnapshot(snapshot);
  });

  return snapshot;
});

/// Provider that listens for widget refresh requests from Android.
///
/// When Android requests a refresh (e.g., widget tapped "refresh"),
/// this provider rebuilds the snapshot and sends it to Android.
final widgetRefreshListenerProvider = Provider<void>((ref) {
  // Listen for method calls from Android
  widgetDataChannel.setMethodCallHandler((call) async {
    switch (call.method) {
      case 'refreshWidgets':
        // Rebuild and resend snapshot
        final snapshot = ref.read(widgetSnapshotProvider);
        await WidgetDataBridge.sendSnapshot(snapshot);
        break;
      case 'clearWidgetData':
        // Clear widget data (on logout)
        ref.read(authStateProvider.notifier).signOut();
        break;
    }
  });
});

/// Provider for auth state changes → clear widget data on logout.
///
/// When the user logs out, this provider clears all widget data
/// to prevent another user's data from appearing.
final widgetAuthStateProvider = Provider<void>((ref) {
  ref.listen<AuthState>(authStateProvider, (previous, next) {
    if (previous?.isAuthenticated == true && !next.isAuthenticated) {
      // User logged out — clear widget data
      WidgetDataBridge.clearWidgetData();
    }
  });
});

/// Provider for order state changes → trigger widget refresh.
///
/// When orders change (new order, status update, etc.),
/// this provider triggers a widget refresh.
final widgetOrderRefreshProvider = Provider<void>((ref) {
  ref.listen<List<Order>>(ordersProvider, (previous, next) {
    if (previous != null && previous.length != next.length) {
      // Order count changed — refresh widgets
      WidgetDataBridge.requestWidgetRefresh();
    }
  });
});

/// Provider for product/stock changes → trigger widget refresh.
final widgetProductRefreshProvider = Provider<void>((ref) {
  ref.watch(productListProvider);
  // Refresh widgets whenever products change
  // (stock quantities, new products, etc.)
  Future.microtask(() {
    WidgetDataBridge.requestWidgetRefresh();
  });
});
