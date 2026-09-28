import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers/app_providers.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/app_button.dart';
import '../../../data/models/product.dart';

class UpdateStockScreen extends ConsumerStatefulWidget {
  final String productName;
  final Product product;

  const UpdateStockScreen({
    super.key,
    required this.productName,
    required this.product,
  });

  @override
  ConsumerState<UpdateStockScreen> createState() => _UpdateStockScreenState();
}

class _UpdateStockScreenState extends ConsumerState<UpdateStockScreen> {
  late final TextEditingController stockController;

  @override
  void initState() {
    super.initState();
    stockController = TextEditingController(
      text: widget.product.stock.toString(),
    );
  }

  @override
  void dispose() {
    stockController.dispose();
    super.dispose();
  }

  Future<void> _saveStock() async {
    final newStock = int.tryParse(stockController.text.trim());
    if (newStock == null || newStock < 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter a valid stock quantity')),
      );
      return;
    }

    final updated = widget.product.copyWith(stock: newStock);
    await ref.read(productListProvider.notifier).updateProduct(updated);

    if (!mounted) return;

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Stock updated successfully')),
    );

    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Update Stock'),
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
              widget.productName,
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.w600,
                color: AppColors.ink,
              ),
            ),
            const SizedBox(height: 28),
            const Text(
              'Current Stock',
              style: TextStyle(
                fontSize: 14,
                color: AppColors.inkSoft,
              ),
            ),
            const SizedBox(height: 6),
            Text(
              widget.product.stock.toString(),
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w600,
                color: AppColors.ink,
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'New Stock',
              style: TextStyle(
                fontSize: 14,
                color: AppColors.inkSoft,
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: stockController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                hintText: 'Enter new stock',
                filled: true,
                fillColor: AppColors.surface,
              ),
            ),
            const SizedBox(height: 28),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: AppButton(
                label: 'Save Stock',
                onPressed: _saveStock,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
