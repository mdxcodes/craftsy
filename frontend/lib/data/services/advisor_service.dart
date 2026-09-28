import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/config/api_config.dart';
import '../../data/models/product.dart';

class AdvisorProductSummary {
  final String id;
  final String title;
  final String description;
  final String category;
  final double price;
  final int stock;
  final String status;
  final String createdAt;
  final String titleEn;
  final String descriptionEn;

  AdvisorProductSummary({
    required this.id,
    required this.title,
    this.description = '',
    this.category = 'Handicrafts',
    required this.price,
    this.stock = 0,
    this.status = 'draft',
    this.createdAt = '',
    this.titleEn = '',
    this.descriptionEn = '',
  });

  factory AdvisorProductSummary.fromProduct(Product product) {
    return AdvisorProductSummary(
      id: product.id,
      title: product.title,
      description: product.description,
      category: product.category,
      price: product.price,
      stock: product.stock,
      status: product.status.name,
      createdAt: product.createdAt.toIso8601String(),
      titleEn: product.title,
      descriptionEn: product.description,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'category': category,
      'price': price,
      'stock': stock,
      'status': status,
      'createdAt': createdAt,
      'title_en': titleEn,
      'description_en': descriptionEn,
    };
  }
}

class AdvisorSuggestion {
  final String productId;
  final String productTitle;
  final String adviceType;
  final String priority;
  final String title;
  final String description;
  final String suggestedAction;
  final double? suggestedPrice;
  final int? suggestedStock;
  final double? currentPrice;
  final int? currentStock;
  final String? category;

  AdvisorSuggestion({
    required this.productId,
    required this.productTitle,
    required this.adviceType,
    required this.priority,
    required this.title,
    required this.description,
    required this.suggestedAction,
    this.suggestedPrice,
    this.suggestedStock,
    this.currentPrice,
    this.currentStock,
    this.category,
  });

  factory AdvisorSuggestion.fromJson(Map<String, dynamic> json) {
    return AdvisorSuggestion(
      productId: json['product_id'] as String? ?? '',
      productTitle: json['product_title'] as String? ?? '',
      adviceType: json['advice_type'] as String? ?? '',
      priority: json['priority'] as String? ?? 'low',
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      suggestedAction: json['suggested_action'] as String? ?? '',
      suggestedPrice: (json['suggested_price'] as num?)?.toDouble(),
      suggestedStock: json['suggested_stock'] as int?,
      currentPrice: (json['current_price'] as num?)?.toDouble(),
      currentStock: json['current_stock'] as int?,
      category: json['category'] as String?,
    );
  }
}

class AdvisorAnalysisResponse {
  final List<AdvisorSuggestion> advice;
  final int totalProducts;
  final int productsNeedingAttention;

  AdvisorAnalysisResponse({
    required this.advice,
    required this.totalProducts,
    required this.productsNeedingAttention,
  });

  factory AdvisorAnalysisResponse.fromJson(Map<String, dynamic> json) {
    return AdvisorAnalysisResponse(
      advice: (json['advice'] as List<dynamic>?)
              ?.map((e) => AdvisorSuggestion.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      totalProducts: json['total_products'] as int? ?? 0,
      productsNeedingAttention: json['products_needing_attention'] as int? ?? 0,
    );
  }
}

class AdvisorService {
  final Dio _dio;

  AdvisorService({String? baseUrl, Dio? dio})
      : _dio =
            dio ??
            Dio(
              BaseOptions(
                baseUrl: baseUrl ?? ApiConfig.baseUrl,
                connectTimeout: const Duration(seconds: 15),
                receiveTimeout: const Duration(seconds: 30),
                headers: {'Accept': 'application/json'},
              ),
            );

  Future<AdvisorAnalysisResponse> analyzeCatalog(List<AdvisorProductSummary> products) async {
    final activeUrl = ApiConfig.baseUrl;
    _dio.options.baseUrl = activeUrl;

    final response = await _dio.post(
      '/api/v1/advisor/analyze',
      data: {
        'products': products.map((p) => p.toJson()).toList(),
      },
    );

    if (response.statusCode == 200 && response.data != null) {
      return AdvisorAnalysisResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw DioException(
      requestOptions: response.requestOptions,
      response: response,
      error: 'Invalid response from advisor service',
    );
  }
}

final advisorServiceProvider = Provider<AdvisorService>((ref) {
  return AdvisorService();
});
