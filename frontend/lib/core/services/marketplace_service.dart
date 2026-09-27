import 'package:dio/dio.dart';
import '../../core/config/api_config.dart';

class MarketplaceProduct {
  final String id;
  final String title;
  final String titleHi;
  final String description;
  final String descriptionHi;
  final double price;
  final String imageUrl;
  final String category;
  final List<String> tags;
  final int stock;
  final String? artisanId;

  MarketplaceProduct({
    required this.id,
    required this.title,
    this.titleHi = '',
    this.description = '',
    this.descriptionHi = '',
    required this.price,
    this.imageUrl = '',
    this.category = '',
    this.tags = const [],
    this.stock = 0,
    this.artisanId,
  });

  factory MarketplaceProduct.fromJson(Map<String, dynamic> json) {
    return MarketplaceProduct(
      id: json['id'] ?? '',
      title: json['title'] ?? '',
      titleHi: json['title_hi'] ?? '',
      description: json['description'] ?? '',
      descriptionHi: json['description_hi'] ?? '',
      price: (json['price'] ?? 0).toDouble(),
      imageUrl: json['image_url'] ?? '',
      category: json['category'] ?? '',
      tags: List<String>.from(json['tags'] ?? []),
      stock: json['stock'] ?? 0,
      artisanId: json['artisan_id'],
    );
  }
}

class MarketplaceService {
  final Dio _dio = Dio();

  Future<List<MarketplaceProduct>> getProducts({
    String? category,
    String? search,
    int limit = 50,
    int offset = 0,
  }) async {
    final response = await _dio.get(
      '${ApiConfig.baseUrl}/api/v1/marketplace/products',
      queryParameters: {
        if (category != null && category.isNotEmpty) 'category': category,
        if (search != null && search.isNotEmpty) 'search': search,
        'limit': limit,
        'offset': offset,
      },
    );

    final List<dynamic> data = response.data;
    return data.map((json) => MarketplaceProduct.fromJson(json)).toList();
  }

  Future<MarketplaceProduct?> getProduct(String productId) async {
    final response = await _dio.get(
      '${ApiConfig.baseUrl}/api/v1/marketplace/products/$productId',
    );

    if (response.data == null) return null;
    return MarketplaceProduct.fromJson(response.data);
  }

  Future<List<String>> getCategories() async {
    final response = await _dio.get(
      '${ApiConfig.baseUrl}/api/v1/marketplace/categories',
    );

    return List<String>.from(response.data);
  }
}

final marketplaceService = MarketplaceService();
