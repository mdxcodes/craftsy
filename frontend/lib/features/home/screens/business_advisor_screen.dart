import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../chatbot/screens/chatbot_sheet.dart';
import '../../../core/providers/app_providers.dart';
import 'update_price_screen.dart';
import 'update_stock_screen.dart';


class BusinessAdvisorScreen extends ConsumerWidget {
  const BusinessAdvisorScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final primary = Theme.of(context).primaryColor;
    final productsAsync = ref.watch(productListProvider);
    final products = productsAsync.valueOrNull ?? [];
    final advisorProduct = products.isNotEmpty ? products.last : null;

    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Business Advisor'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Here are some suggestions for your business',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600,
              ),
            ),

            const SizedBox(height: 20),

            _SuggestionCard(
              icon: Icons.currency_rupee,
              title: 'Price Review Needed',
              description: advisorProduct != null
                  ? '${advisorProduct.title}\n'
                      'Current Price: ₹${advisorProduct.price.toStringAsFixed(0)}\n'
                      'Suggested Price: ₹600–₹800\n'
                      'Reason: Similar products are selling at higher prices.'
                  : 'Add a product to get a price recommendation.',
              buttonText: 'Update Price',
              primary: primary,
              onPressed: () {
                if (advisorProduct == null) return;

                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => UpdatePriceScreen(
                      product: advisorProduct,
                    ),
                  ),
                );
              },
            ),
            const SizedBox(height: 14),

            _SuggestionCard(
              icon: Icons.inventory_2_outlined,
              title: 'Low Stock Alert',
              description:
                  'Terracotta Clay Hand-Painted Folk Art Water Pot with Tap\n'
                  'Current Stock: 4\n'
                  'Demand is expected to increase during summer season. Keeping more units ready may help avoid missed sales opportunities\n'
                  'Suggested Stock: 15',
              buttonText: 'Update Stock',
              primary: primary,
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const UpdateStockScreen(
                      productName:
                          'Terracotta Clay Hand-Painted Folk Art Water Pot with Tap',
                    ),
                  ),
                );
              },
            ),
              const SizedBox(height: 14),

              _SuggestionCard(
                icon: Icons.hourglass_empty_outlined,
                title: 'Slow Moving Products',
                description:
                    'Handcrafted Bamboo Basket\n'
                    'This product has not been sold for 120 days\n'
                    'AI suggests creating a 10% offer to improve sales.',
                buttonText: 'View Offer',
                primary: primary,
                onPressed: () {},
              ),

              const SizedBox(height: 14),

              _SuggestionCard(
                icon: Icons.celebration_outlined,
                title: 'Festival Demand Opportunity',
                description: 'Some products may have higher demand during festivals.',
                buttonText: 'View Suggestions',
                primary: primary,
                onPressed: () {},
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
          color: Colors.grey.shade300,
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
              color: Colors.grey.shade700,
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
