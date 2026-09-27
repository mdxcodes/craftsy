import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

/// Widget-safe snapshot model — matches the Kotlin WidgetSnapshot.
/// This is the ONLY data exposed to Android widgets.
class WidgetSnapshot {
  final int schemaVersion;
  final bool authenticated;
  final String? accountId;
  final int lastUpdated;
  final String dataFreshness;
  final TodaySnapshot? today;
  final OrdersSnapshot? orders;
  final StockSnapshot? stock;
  final ChannelsSnapshot? channels;
  final CraftMitraSnapshot? craftMitra;

  const WidgetSnapshot({
    this.schemaVersion = 1,
    this.authenticated = false,
    this.accountId,
    this.lastUpdated = 0,
    this.dataFreshness = 'UNKNOWN',
    this.today,
    this.orders,
    this.stock,
    this.channels,
    this.craftMitra,
  });

  Map<String, dynamic> toJson() {
    return {
      'schemaVersion': schemaVersion,
      'authenticated': authenticated,
      'accountId': accountId,
      'lastUpdated': lastUpdated,
      'dataFreshness': dataFreshness,
      'today': today?.toJson(),
      'orders': orders?.toJson(),
      'stock': stock?.toJson(),
      'channels': channels?.toJson(),
      'craftMitra': craftMitra?.toJson(),
    };
  }
}

class TodaySnapshot {
  final int attentionCount;
  final int orderAttentionCount;
  final int stockAttentionCount;
  final int channelAttentionCount;
  final List<ActionableItem> actionableItems;

  const TodaySnapshot({
    this.attentionCount = 0,
    this.orderAttentionCount = 0,
    this.stockAttentionCount = 0,
    this.channelAttentionCount = 0,
    this.actionableItems = const [],
  });

  Map<String, dynamic> toJson() {
    return {
      'attentionCount': attentionCount,
      'orderAttentionCount': orderAttentionCount,
      'stockAttentionCount': stockAttentionCount,
      'channelAttentionCount': channelAttentionCount,
      'actionableItems': actionableItems.map((e) => e.toJson()).toList(),
    };
  }
}

class ActionableItem {
  final String type;
  final String id;
  final String title;
  final String? subtitle;
  final String? deepLink;

  const ActionableItem({
    required this.type,
    required this.id,
    required this.title,
    this.subtitle,
    this.deepLink,
  });

  Map<String, dynamic> toJson() {
    return {
      'type': type,
      'id': id,
      'title': title,
      'subtitle': subtitle,
      'deepLink': deepLink,
    };
  }
}

class OrdersSnapshot {
  final int actionableCount;
  final List<WidgetOrderSummary> items;

  const OrdersSnapshot({
    this.actionableCount = 0,
    this.items = const [],
  });

  Map<String, dynamic> toJson() {
    return {
      'actionableCount': actionableCount,
      'items': items.map((e) => e.toJson()).toList(),
    };
  }
}

class WidgetOrderSummary {
  final String orderId;
  final String status;
  final String statusLabel;
  final String productTitle;
  final String? requiredAction;
  final String? deepLink;

  const WidgetOrderSummary({
    required this.orderId,
    required this.status,
    required this.statusLabel,
    required this.productTitle,
    this.requiredAction,
    this.deepLink,
  });

  Map<String, dynamic> toJson() {
    return {
      'orderId': orderId,
      'status': status,
      'statusLabel': statusLabel,
      'productTitle': productTitle,
      'requiredAction': requiredAction,
      'deepLink': deepLink,
    };
  }
}

class StockSnapshot {
  final int outOfStockCount;
  final int lowStockCount;
  final List<WidgetStockItem> items;

  const StockSnapshot({
    this.outOfStockCount = 0,
    this.lowStockCount = 0,
    this.items = const [],
  });

  Map<String, dynamic> toJson() {
    return {
      'outOfStockCount': outOfStockCount,
      'lowStockCount': lowStockCount,
      'items': items.map((e) => e.toJson()).toList(),
    };
  }
}

class WidgetStockItem {
  final String productId;
  final String productName;
  final int stockQuantity;
  final String stockState;
  final String? deepLink;

  const WidgetStockItem({
    required this.productId,
    required this.productName,
    required this.stockQuantity,
    required this.stockState,
    this.deepLink,
  });

  Map<String, dynamic> toJson() {
    return {
      'productId': productId,
      'productName': productName,
      'stockQuantity': stockQuantity,
      'stockState': stockState,
      'deepLink': deepLink,
    };
  }
}

class ChannelsSnapshot {
  final ChannelStatus? craftsy;
  final ChannelStatus? ondc;
  final ChannelStatus? government;

  const ChannelsSnapshot({
    this.craftsy,
    this.ondc,
    this.government,
  });

  Map<String, dynamic> toJson() {
    return {
      'craftsy': craftsy?.toJson(),
      'ondc': ondc?.toJson(),
      'government': government?.toJson(),
    };
  }
}

class ChannelStatus {
  final String channelName;
  final String state;
  final String stateLabel;
  final String? detail;
  final String? deepLink;

  const ChannelStatus({
    required this.channelName,
    required this.state,
    required this.stateLabel,
    this.detail,
    this.deepLink,
  });

  Map<String, dynamic> toJson() {
    return {
      'channelName': channelName,
      'state': state,
      'stateLabel': stateLabel,
      'detail': detail,
      'deepLink': deepLink,
    };
  }
}

class CraftMitraSnapshot {
  final bool available;
  final bool voiceModeAvailable;
  final bool textModeAvailable;
  final String? voiceDeepLink;
  final String? textDeepLink;

  const CraftMitraSnapshot({
    this.available = true,
    this.voiceModeAvailable = true,
    this.textModeAvailable = true,
    this.voiceDeepLink = '/assistant?mode=voice',
    this.textDeepLink = '/assistant?mode=text',
  });

  Map<String, dynamic> toJson() {
    return {
      'available': available,
      'voiceModeAvailable': voiceModeAvailable,
      'textModeAvailable': textModeAvailable,
      'voiceDeepLink': voiceDeepLink,
      'textDeepLink': textDeepLink,
    };
  }
}

/// Widget data bridge — sends snapshots to Android via MethodChannel.
class WidgetDataBridge {
  static const MethodChannel _channel = MethodChannel('com.craftsy.app/widget_data');

  /// Send snapshot to Android for widget rendering.
  static Future<void> sendSnapshot(WidgetSnapshot snapshot) async {
    try {
      await _channel.invokeMethod('updateWidgetData', snapshot.toJson());
    } on PlatformException catch (e) {
      // Widget data update failed — log but don't crash the app
      // Widgets will show stale data until next successful update
      debugPrint('WidgetDataBridge: Failed to send snapshot: ${e.message}');
    } on MissingPluginException {
      // Android side not ready or method not implemented — ignore
    }
  }

  /// Clear all widget data (on logout/account switch).
  static Future<void> clearWidgetData() async {
    try {
      await _channel.invokeMethod('clearWidgetData');
    } on PlatformException catch (e) {
      debugPrint('WidgetDataBridge: Failed to clear widget data: ${e.message}');
    } on MissingPluginException {
      // Android side not ready — ignore
    }
  }

  /// Request widget refresh from Android.
  static Future<void> requestWidgetRefresh() async {
    try {
      await _channel.invokeMethod('refreshWidgets');
    } on PlatformException catch (e) {
      debugPrint('WidgetDataBridge: Failed to refresh widgets: ${e.message}');
    } on MissingPluginException {
      // Android side not ready — ignore
    }
  }
}
