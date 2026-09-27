import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers/app_providers.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/app_button.dart';
import '../../../data/models/product.dart';

class UpdatePriceScreen extends ConsumerStatefulWidget {
  final Product product;

  const UpdatePriceScreen({
    super.key,
    required this.product,
  });

  @override
  ConsumerState<UpdatePriceScreen> createState() => _UpdatePriceScreenState();
}

class _UpdatePriceScreenState extends ConsumerState<UpdatePriceScreen> {
  late final TextEditingController priceController;

  @override
  void initState() {
    super.initState();
    priceController = TextEditingController(
      text: widget.product.price.toStringAsFixed(0),
    );
  }

  @override
  void dispose() {
    priceController.dispose();
    super.dispose();
  }

  Future<void> _savePrice() async {
    final newPrice = double.tryParse(priceController.text.trim());

    if (newPrice == null || newPrice <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please enter a valid price'),
        ),
      );
      return;
    }

    final updated = widget.product.copyWith(
      price: newPrice,
    );

    await ref
        .read(productListProvider.notifier)
        .updateProduct(updated);

    if (!mounted) return;

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Price updated successfully'),
      ),
    );

    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Update Price'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(AppSpacing.screenPadding),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Product',
              style: TextStyle(
                fontSize: 14,
                color: AppColors.inkSoft,
              ),
            ),
            const SizedBox(height: 6),

            Text(
              widget.product.title,
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.w600,
                color: AppColors.ink,
              ),
            ),

            const SizedBox(height: 28),

            const Text(
              'Current Price',
              style: TextStyle(
                fontSize: 14,
                color: AppColors.inkSoft,
              ),
            ),
            const SizedBox(height: 6),

            Text(
              '₹${widget.product.price.toStringAsFixed(0)}',
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w600,
                color: AppColors.ink,
              ),
            ),

            const SizedBox(height: 24),

            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.parchmentDeep,
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'AI Suggested Price',
                    style: TextStyle(
                      fontSize: 14,
                      color: AppColors.inkSoft,
                    ),
                  ),
                  SizedBox(height: 6),
                  Text(
                    '₹600–₹800',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w600,
                      color: AppColors.ink,
                    ),
                  ),
                  SizedBox(height: 6),
                  Text(
                    'Similar products are selling at higher prices.',
                    style: TextStyle(
                      fontSize: 13,
                      color: AppColors.inkSoft,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 28),

            const Text(
              'New Price',
              style: TextStyle(
                fontSize: 14,
                color: AppColors.inkSoft,
              ),
            ),
            const SizedBox(height: 8),

            TextField(
              controller: priceController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                prefixText: '₹ ',
                hintText: 'Enter new price',
                filled: true,
                fillColor: AppColors.surface,
              ),
            ),

            const SizedBox(height: 28),

            SizedBox(
              width: double.infinity,
              height: 50,
              child: AppButton(
                label: 'Save Price',
                onPressed: _savePrice,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
