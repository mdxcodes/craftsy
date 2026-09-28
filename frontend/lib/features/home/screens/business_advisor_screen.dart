import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../chatbot/screens/chatbot_sheet.dart';
import '../../../core/providers/app_providers.dart';
import '../../../data/models/product.dart';
import 'update_price_screen.dart';
import 'update_stock_screen.dart';

class BusinessAdvisorScreen extends ConsumerWidget {
  const BusinessAdvisorScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productsAsync = ref.watch(productListProvider);
    final products = productsAsync.valueOrNull ?? [];

    final liveProducts = products.where((p) => p.status == ProductStatus.live).toList();

    final lowStockProducts = <Product>[];
    final priceReviewProducts = <Product>[];
    final slowMovingProducts = <Product>[];
    final festivalOpportunities = <String>[];

    final now = DateTime.now();

    for (final product in products) {
      if (product.stock > 0 && product.stock < 5) {
        lowStockProducts.add(product);
      }

      final ageDays = now.difference(product.createdAt).inDays;
      if (product.status == ProductStatus.draft && ageDays > 14) {
        slowMovingProducts.add(product);
      }
      if (product.status == ProductStatus.listingRemoved && ageDays > 30) {
        slowMovingProducts.add(product);
      }
    }

    if (liveProducts.length >= 2) {
      final categoryPrices = <String, List<double>>{};
      for (final product in liveProducts) {
        categoryPrices.putIfAbsent(product.category, () => []).add(product.price);
      }
      for (final product in liveProducts) {
        final prices = categoryPrices[product.category] ?? [];
        if (prices.length < 2) continue;
        final avgPrice = prices.reduce((a, b) => a + b) / prices.length;
        if (product.price < avgPrice * 0.7) {
          priceReviewProducts.add(product);
        }
      }
    }

    final currentMonth = now.month;
    if (currentMonth >= 9 && currentMonth <= 11) {
      festivalOpportunities.addAll([
        'Diwali: Hand-painted items, diyas, and home decor see high demand.',
        'Dussehra: Traditional textiles and handicrafts are popular gifts.',
        'Wedding season: Jewelry and decorative items gain traction.',
      ]);
    } else if (currentMonth >= 12 || currentMonth <= 2) {
      festivalOpportunities.addAll([
        'New Year: Festive home decor and gift items are in demand.',
        'Makar Sankranti: Kite-making materials and traditional sweets crafts sell well.',
        'Republic Day: Patriotic-themed crafts and textiles see interest.',
      ]);
    } else if (currentMonth >= 3 && currentMonth <= 5) {
      festivalOpportunities.addAll([
        'Holi: Brightly colored textiles and eco-friendly celebration items.',
        'Summer: Terracotta coolers, hand fans, and cotton crafts.',
        'Wedding season continues: Jewelry and home decor.',
      ]);
    } else {
      festivalOpportunities.addAll([
        'Monsoon: Bamboo crafts and waterproof home items.',
        'Upcoming festivals: Stock up on traditional crafts early.',
        'Seasonal shift: Consider refreshing product photos and descriptions.',
      ]);
    }

    final priceReview = priceReviewProducts.isNotEmpty ? priceReviewProducts.first : null;
    final lowStock = lowStockProducts.isNotEmpty ? lowStockProducts.first : null;
    final slowMoving = slowMovingProducts.isNotEmpty ? slowMovingProducts.first : null;

    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Business Advisor'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Here are some suggestions for your business',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600,
                color: Theme.of(context).colorScheme.onSurface,
              ),
            ),

            const SizedBox(height: 20),

            _SuggestionCard(
              icon: Icons.currency_rupee,
              title: 'Price Review Needed',
              description: priceReview != null
                  ? '${priceReview.title}\n'
                      'Current Price: ₹${priceReview.price.toStringAsFixed(0)}\n'
                      'Suggested Price: ₹${(priceReview.price * 1.2).toStringAsFixed(0)}\n'
                      'Reason: Similar products in ${priceReview.category} are priced higher.'
                  : products.isEmpty
                      ? 'Add products to get price recommendations.'
                      : 'Your current pricing looks competitive for your catalog.',
              buttonText: priceReview != null ? 'Update Price' : 'Review Catalog',
              primary: Theme.of(context).primaryColor,
              onPressed: priceReview != null
                  ? () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => UpdatePriceScreen(
                            product: priceReview,
                          ),
                        ),
                      );
                    }
                  : () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text(
                            'Keep monitoring your prices against market trends.',
                          ),
                        ),
                      );
                    },
            ),
            const SizedBox(height: 14),

            _SuggestionCard(
              icon: Icons.inventory_2_outlined,
              title: 'Low Stock Alert',
              description: lowStock != null
                  ? '${lowStock.title}\n'
                      'Current Stock: ${lowStock.stock}\n'
                      'Demand is expected to increase during the upcoming season.\n'
                      'Suggested Stock: ${(lowStock.stock * 3).clamp(10, 50)}'
                  : 'No low-stock products detected. Keep monitoring inventory levels.',
              buttonText: lowStock != null ? 'Update Stock' : 'View Inventory',
              primary: Theme.of(context).primaryColor,
              onPressed: lowStock != null
                  ? () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => UpdateStockScreen(
                            productName: lowStock.title,
                          ),
                        ),
                      );
                    }
                  : () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text(
                            'Check your inventory regularly to avoid stockouts.',
                          ),
                        ),
                      );
                    },
            ),
            const SizedBox(height: 14),

            _SuggestionCard(
              icon: Icons.hourglass_empty_outlined,
              title: 'Slow Moving Products',
              description: slowMoving != null
                  ? '${slowMoving.title}\n'
                      'This product has been in your catalog for ${now.difference(slowMoving.createdAt).inDays} days.\n'
                      'AI suggests refreshing the photos or adjusting the price.'
                  : slowMovingProducts.isEmpty
                      ? 'No slow-moving products detected. Great job!'
                      : '${slowMovingProducts.length} products may need attention.',
              buttonText: slowMoving != null ? 'Refresh Listing' : 'View All Products',
              primary: Theme.of(context).primaryColor,
              onPressed: () {
                if (slowMoving != null) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        'Consider updating photos or price for ${slowMoving.title}.',
                      ),
                    ),
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text(
                        'Browse your catalog to identify products that need a refresh.',
                      ),
                    ),
                  );
                }
              },
            ),

            const SizedBox(height: 14),

            _SuggestionCard(
              icon: Icons.celebration_outlined,
              title: 'Festival Demand Opportunity',
              description: festivalOpportunities.isNotEmpty
                  ? festivalOpportunities.join('\n\n')
                  : 'Check back during festival season for personalized suggestions.',
              buttonText: 'View Suggestions',
              primary: Theme.of(context).primaryColor,
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    title: const Text('Festival Demand Suggestions'),
                    content: Text(
                      festivalOpportunities.isNotEmpty
                          ? festivalOpportunities.join('\n\n')
                          : 'No specific festival suggestions at this time.',
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(ctx),
                        child: const Text('Close'),
                      ),
                    ],
                  ),
                );
              },
            ),

            const SizedBox(height: 24),

            SizedBox(
              width: double.infinity,
              height: 50,
              child: OutlinedButton.icon(
                onPressed: () {
                  ChatbotSheet.show(context);
                },
                icon: const Icon(Icons.smart_toy_outlined),
                label: const Text(
                  'Ask AI Advisor',
                  style: TextStyle(
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SuggestionCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;
  final String buttonText;
  final Color primary;
  final VoidCallback onPressed;

  const _SuggestionCard({
    required this.icon,
    required this.title,
    required this.description,
    required this.buttonText,
    required this.primary,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: Theme.of(context).colorScheme.outlineVariant,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                icon,
                color: primary,
                size: 24,
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: 10),

          Text(
            description,
            style: TextStyle(
              fontSize: 14,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
              height: 1.4,
            ),
          ),

          const SizedBox(height: 12),

          Align(
            alignment: Alignment.centerRight,
            child: TextButton(
              onPressed: onPressed,
              child: Text(buttonText),
            ),
          ),
        ],
      ),
    );
  }
}
