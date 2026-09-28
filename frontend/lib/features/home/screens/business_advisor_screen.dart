import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers/app_providers.dart';
import '../../../data/models/product.dart';
import '../../../data/services/advisor_service.dart';
import 'update_price_screen.dart';
import 'update_stock_screen.dart';

class BusinessAdvisorScreen extends ConsumerWidget {
  const BusinessAdvisorScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productsAsync = ref.watch(productListProvider);
    final products = productsAsync.valueOrNull ?? [];

    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Business Advisor'),
      ),
      body: products.isEmpty
          ? Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.storefront_outlined,
                      size: 64,
                      color: Theme.of(context).colorScheme.outlineVariant,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Add products to get personalized business advice.',
                      style: Theme.of(context).textTheme.titleMedium,
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              ),
            )
          : FutureBuilder<AdvisorAnalysisResponse>(
              future: _loadAdvice(ref, products),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(
                    child: CircularProgressIndicator(),
                  );
                }
                if (snapshot.hasError) {
                  return Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        children: [
                          const Icon(Icons.wifi_off_rounded, size: 48),
                          const SizedBox(height: 16),
                          Text(
                            'Unable to load advisor right now.',
                            style: Theme.of(context).textTheme.titleMedium,
                          ),
                          const SizedBox(height: 8),
                          TextButton.icon(
                            onPressed: () {
                              if (products.isNotEmpty) {
                                _loadAdvice(ref, products, forceRefresh: true);
                              }
                            },
                            icon: const Icon(Icons.refresh),
                            label: const Text('Retry'),
                          ),
                        ],
                      ),
                    ),
                  );
                }

                final response = snapshot.data;
                if (response == null || response.advice.isEmpty) {
                  return Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Column(
                        children: [
                          Icon(
                            Icons.check_circle_outline,
                            size: 64,
                            color: Theme.of(context).colorScheme.primary,
                          ),
                          const SizedBox(height: 16),
                          Text(
                            'Your catalog looks healthy right now.',
                            style: Theme.of(context).textTheme.titleMedium,
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                  );
                }

                return ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: response.advice.length,
                  itemBuilder: (context, index) {
                    final item = response.advice[index];
                    return _AdviceCard(
                      advice: item,
                      products: products,
                    );
                  },
                );
              },
            ),
    );
  }

  Future<AdvisorAnalysisResponse> _loadAdvice(
    WidgetRef ref,
    List<Product> products, {
    bool forceRefresh = false,
  }) async {
    final service = ref.read(advisorServiceProvider);
    final summaries = products.map(AdvisorProductSummary.fromProduct).toList();
    return service.analyzeCatalog(summaries);
  }
}

class _AdviceCard extends StatelessWidget {
  final AdvisorSuggestion advice;
  final List<Product> products;

  const _AdviceCard({
    required this.advice,
    required this.products,
  });

  Product? _findProduct() {
    try {
      return products.firstWhere((p) => p.id == advice.productId);
    } on StateError {
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    final product = _findProduct();
    final colorScheme = Theme.of(context).colorScheme;
    final icon = switch (advice.adviceType) {
      'price_review' => Icons.currency_rupee,
      'low_stock' => Icons.inventory_2_outlined,
      'slow_moving' => Icons.hourglass_empty_outlined,
      'festival_opportunity' => Icons.celebration_outlined,
      _ => Icons.lightbulb_outlined,
    };

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: colorScheme.outlineVariant),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: colorScheme.primary, size: 24),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    advice.title,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: _priorityColor(advice.priority).withValues(alpha: 0.12),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    advice.priority.toUpperCase(),
                    style: TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w600,
                      color: _priorityColor(advice.priority),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            Text(
              advice.description,
              style: TextStyle(
                fontSize: 14,
                color: colorScheme.onSurfaceVariant,
                height: 1.4,
              ),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                if (advice.suggestedAction == 'update_price' && product != null)
                  FilledButton.icon(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => UpdatePriceScreen(product: product),
                        ),
                      );
                    },
                    icon: const Icon(Icons.edit, size: 18),
                    label: Text('Update Price'),
                  ),
                if (advice.suggestedAction == 'update_stock' && product != null)
                  FilledButton.icon(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                           builder: (_) => UpdateStockScreen(
                             productName: product.title,
                             product: product,
                           ),
                        ),
                      );
                    },
                    icon: const Icon(Icons.inventory, size: 18),
                    label: Text('Update Stock'),
                  ),
                if (advice.suggestedAction == 'refresh_listing' && product != null)
                  FilledButton.icon(
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Open ${product.title} to refresh photos/price.'),
                        ),
                      );
                    },
                    icon: const Icon(Icons.refresh, size: 18),
                    label: const Text('Refresh Listing'),
                  ),
                if (advice.suggestedAction == 'boost_listing' && product != null)
                  FilledButton.icon(
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text('Consider featuring ${product.title} in promotions.'),
                        ),
                      );
                    },
                     icon: const Icon(Icons.auto_awesome, size: 18),
                     label: const Text('Boost Listing'),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Color _priorityColor(String priority) {
    switch (priority) {
      case 'high':
        return Colors.red;
      case 'medium':
        return Colors.orange;
      case 'low':
      default:
        return Colors.green;
    }
  }
}
