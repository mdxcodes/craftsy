/// Unified Commerce Hub models.
///
/// These models represent the unified commerce experience across
/// all channels: Craftsy Marketplace, ONDC, and GeM.

/// Channel status information for a product.
class ChannelStatusInfo {
  final String channel;
  final String status;
  final String label;
  final String icon;
  final String color;
  final bool isConnected;
  final bool canPublish;
  final List<String> missingRequirements;
  final String displayStatus;

  const ChannelStatusInfo({
    required this.channel,
    required this.status,
    required this.label,
    required this.icon,
    required this.color,
    required this.isConnected,
    required this.canPublish,
    required this.missingRequirements,
    required this.displayStatus,
  });

  factory ChannelStatusInfo.fromJson(Map<String, dynamic> json) {
    return ChannelStatusInfo(
      channel: json['channel'] as String? ?? '',
      status: json['status'] as String? ?? '',
      label: json['label'] as String? ?? '',
      icon: json['icon'] as String? ?? '',
      color: json['color'] as String? ?? '',
      isConnected: json['is_connected'] as bool? ?? false,
      canPublish: json['can_publish'] as bool? ?? false,
      missingRequirements: (json['missing_requirements'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      displayStatus: json['display_status'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'channel': channel,
      'status': status,
      'label': label,
      'icon': icon,
      'color': color,
      'is_connected': isConnected,
      'can_publish': canPublish,
      'missing_requirements': missingRequirements,
      'display_status': displayStatus,
    };
  }
}

/// Commerce summary for the artisan dashboard.
class CommerceSummary {
  final int totalProducts;
  final int liveProducts;
  final Map<String, int> channelCounts;
  final int totalOrders;
  final int productsNeedingAttention;
  final int lowStock;

  const CommerceSummary({
    required this.totalProducts,
    required this.liveProducts,
    required this.channelCounts,
    required this.totalOrders,
    required this.productsNeedingAttention,
    required this.lowStock,
  });

  factory CommerceSummary.fromJson(Map<String, dynamic> json) {
    return CommerceSummary(
      totalProducts: json['total_products'] as int? ?? 0,
      liveProducts: json['live_products'] as int? ?? 0,
      channelCounts: (json['channel_counts'] as Map<String, dynamic>?)
              ?.map((k, v) => MapEntry(k, v as int? ?? 0)) ??
          {},
      totalOrders: json['total_orders'] as int? ?? 0,
      productsNeedingAttention: json['products_needing_attention'] as int? ?? 0,
      lowStock: json['low_stock'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'total_products': totalProducts,
      'live_products': liveProducts,
      'channel_counts': channelCounts,
      'total_orders': totalOrders,
      'products_needing_attention': productsNeedingAttention,
      'low_stock': lowStock,
    };
  }
}

/// Product detail with channel information.
class ProductDetailWithChannels {
  final String id;
  final String title;
  final String titleHi;
  final String description;
  final String descriptionHi;
  final double price;
  final String imageUrl;
  final String category;
  final String status;
  final int stock;
  final List<String> tags;
  final List<ChannelStatusInfo> channels;

  const ProductDetailWithChannels({
    required this.id,
    required this.title,
    required this.titleHi,
    required this.description,
    required this.descriptionHi,
    required this.price,
    required this.imageUrl,
    required this.category,
    required this.status,
    required this.stock,
    required this.tags,
    required this.channels,
  });

  factory ProductDetailWithChannels.fromJson(Map<String, dynamic> json) {
    return ProductDetailWithChannels(
      id: json['id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      titleHi: json['title_hi'] as String? ?? '',
      description: json['description'] as String? ?? '',
      descriptionHi: json['description_hi'] as String? ?? '',
      price: (json['price'] as num?)?.toDouble() ?? 0.0,
      imageUrl: json['image_url'] as String? ?? '',
      category: json['category'] as String? ?? '',
      status: json['status'] as String? ?? '',
      stock: json['stock'] as int? ?? 0,
      tags: (json['tags'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      channels: (json['channels'] as List<dynamic>?)
              ?.map((e) => ChannelStatusInfo.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'title_hi': titleHi,
      'description': description,
      'description_hi': descriptionHi,
      'price': price,
      'image_url': imageUrl,
      'category': category,
      'status': status,
      'stock': stock,
      'tags': tags,
      'channels': channels.map((e) => e.toJson()).toList(),
    };
  }
}

/// Unified inventory for a product.
class ProductInventory {
  final String productId;
  final int available;
  final int reserved;
  final int committed;
  final int fulfilled;

  const ProductInventory({
    required this.productId,
    required this.available,
    required this.reserved,
    required this.committed,
    required this.fulfilled,
  });

  factory ProductInventory.fromJson(Map<String, dynamic> json) {
    return ProductInventory(
      productId: json['product_id'] as String? ?? '',
      available: json['available'] as int? ?? 0,
      reserved: json['reserved'] as int? ?? 0,
      committed: json['committed'] as int? ?? 0,
      fulfilled: json['fulfilled'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'product_id': productId,
      'available': available,
      'reserved': reserved,
      'committed': committed,
      'fulfilled': fulfilled,
    };
  }
}

/// Cross-channel sync status for a product.
class ProductSyncStatus {
  final String productId;
  final String productUpdated;
  final Map<String, ChannelSyncStatus> channels;

  const ProductSyncStatus({
    required this.productId,
    required this.productUpdated,
    required this.channels,
  });

  factory ProductSyncStatus.fromJson(Map<String, dynamic> json) {
    return ProductSyncStatus(
      productId: json['product_id'] as String? ?? '',
      productUpdated: json['product_updated'] as String? ?? '',
      channels: (json['channels'] as Map<String, dynamic>?)
              ?.map((k, v) => MapEntry(
                  k, ChannelSyncStatus.fromJson(v as Map<String, dynamic>))) ??
          {},
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'product_id': productId,
      'product_updated': productUpdated,
      'channels': channels.map((k, v) => MapEntry(k, v.toJson())),
    };
  }
}

/// Sync status for a single channel.
class ChannelSyncStatus {
  final String status;
  final String? lastSynced;
  final String? externalId;
  final String syncState;

  const ChannelSyncStatus({
    required this.status,
    required this.lastSynced,
    required this.externalId,
    required this.syncState,
  });

  factory ChannelSyncStatus.fromJson(Map<String, dynamic> json) {
    return ChannelSyncStatus(
      status: json['status'] as String? ?? '',
      lastSynced: json['last_synced'] as String?,
      externalId: json['external_id'] as String?,
      syncState: json['sync_state'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'status': status,
      'last_synced': lastSynced,
      'external_id': externalId,
      'sync_state': syncState,
    };
  }
}

/// Order channel summary.
class OrderChannelSummary {
  final String channel;
  final int total;
  final int pending;
  final int confirmed;
  final int shipped;
  final int delivered;
  final int cancelled;

  const OrderChannelSummary({
    required this.channel,
    required this.total,
    required this.pending,
    required this.confirmed,
    required this.shipped,
    required this.delivered,
    required this.cancelled,
  });

  factory OrderChannelSummary.fromJson(Map<String, dynamic> json) {
    return OrderChannelSummary(
      channel: json['channel'] as String? ?? '',
      total: json['total'] as int? ?? 0,
      pending: json['pending'] as int? ?? 0,
      confirmed: json['confirmed'] as int? ?? 0,
      shipped: json['shipped'] as int? ?? 0,
      delivered: json['delivered'] as int? ?? 0,
      cancelled: json['cancelled'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'channel': channel,
      'total': total,
      'pending': pending,
      'confirmed': confirmed,
      'shipped': shipped,
      'delivered': delivered,
      'cancelled': cancelled,
    };
  }
}
