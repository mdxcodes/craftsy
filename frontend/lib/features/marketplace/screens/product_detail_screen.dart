import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';

import '../../../core/services/marketplace_service.dart';
import '../../../core/services/commerce_service.dart';
import '../../../core/widgets/speak_button.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/widgets/app_image.dart';
import '../../../core/accessibility/accessibility_tokens.dart';
import '../../../core/widgets/formatted_description.dart';

/// Fetches one live product by id from the public marketplace API.
final productDetailProvider = FutureProvider.autoDispose
    .family<MarketplaceProduct, String>((ref, productId) {
  return marketplaceService.getProduct(productId) as Future<MarketplaceProduct>;
});

/// Add-to-cart mutation with honest success/error feedback.
final addToCartProvider =
    FutureProvider.autoDispose.family<Cart, String>((ref, productId) {
  return ref.read(commerceServiceProvider).addToCart(productId);
});

class MarketplaceProductDetailScreen extends ConsumerStatefulWidget {
  final String productId;

  const MarketplaceProductDetailScreen({super.key, required this.productId});

  @override
  ConsumerState<MarketplaceProductDetailScreen> createState() =>
      _ProductDetailScreenState();
}

class _ProductDetailScreenState
    extends ConsumerState<MarketplaceProductDetailScreen> {
  int _quantity = 1;

  Future<void> _addToCart({bool goCheckout = false}) async {
    // Guard: quantity must not exceed available stock
    final product =
        ref.read(productDetailProvider(widget.productId)).valueOrNull;
    if (product != null && _quantity > product.stock) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'cart_stock_limit'.tr(namedArgs: {'count': '${product.stock}'}),
          ),
          backgroundColor: AppColors.coral,
        ),
      );
      return;
    }

    try {
      await ref
          .read(commerceServiceProvider)
          .addToCart(widget.productId, quantity: _quantity);
      if (!mounted) return;
      ref.invalidate(addToCartProvider);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('cart_added'.tr()),
          backgroundColor: AppColors.teal,
          duration: const Duration(seconds: 2),
        ),
      );
      if (goCheckout) {
        context.push('/my-cart');
      }
    } on CommerceApiException catch (e) {
      if (!mounted) return;
      final key = switch (e.statusCode) {
        401 => 'cart_login_required',
        409 => 'cart_stock_limit_generic',
        _ => 'cart_add_failed',
      };
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(key.tr()),
          backgroundColor: AppColors.coral,
        ),
      );
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('cart_add_failed'.tr()),
          backgroundColor: AppColors.coral,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final productAsync = ref.watch(productDetailProvider(widget.productId));

    return Scaffold(
      body: SafeArea(
        child: productAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (error, _) => Center(
            child: Padding(
              padding: const EdgeInsets.all(AccessibilityTokens.spacingXl),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('marketplace_no_products'.tr()),
                  const SizedBox(height: AccessibilityTokens.spacingMd),
                  TextButton.icon(
                    onPressed: () => context.pop(),
                    icon: const Icon(Icons.arrow_back),
                    label: Text('action_back'.tr()),
                  ),
                ],
              ),
            ),
          ),
          data: (product) => _ProductDetailBody(
            product: product,
            quantity: _quantity,
            onQuantityChanged: (q) => setState(() => _quantity = q),
            onAddToCart: () => _addToCart(),
            onBuyNow: () => _addToCart(goCheckout: true),
          ),
        ),
      ),
    );
  }
}

class _ProductDetailBody extends StatelessWidget {
  final MarketplaceProduct product;
  final int quantity;
  final ValueChanged<int> onQuantityChanged;
  final VoidCallback onAddToCart;
  final VoidCallback onBuyNow;

  const _ProductDetailBody({
    required this.product,
    required this.quantity,
    required this.onQuantityChanged,
    required this.onAddToCart,
    required this.onBuyNow,
  });

  @override
  Widget build(BuildContext context) {
    final outOfStock = product.stock <= 0;

    return Column(
      children: [
        // App bar row
        Padding(
          padding: EdgeInsets.all(AppSpacing.screenPadding),
          child: Row(
            children: [
              _RoundIconButton(
                icon: Icons.arrow_back,
                tooltip: 'action_back'.tr(),
                onPressed: () => context.pop(),
              ),
              const Spacer(),
              SpeakButton(
                compact: true,
                text: [
                  product.title,
                  '₹${product.price.toStringAsFixed(0)}',
                  if (product.description.isNotEmpty) product.description,
                ].join('. '),
              ),
            ],
          ),
        ),

        Expanded(
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Product image
                AspectRatio(
                  aspectRatio: 1.2,
                  child: AppImage(
                    imageUrl: product.imageUrl,
                    fallbackWidget: Container(
                      color: AppColors.parchmentDeep,
                      child: const Icon(
                        Icons.image,
                        size: 64,
                        color: AppColors.textSecondary,
                      ),
                    ),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.all(AppSpacing.screenPadding),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Title
                      Text(
                        product.title,
                        style: AppTextStyles.headlineLarge,
                      ),

                      // Price
                      const SizedBox(height: AppSpacing.xs),
                      Text(
                        '₹${product.price.toStringAsFixed(0)}',
                        style: AppTextStyles.displayLarge.copyWith(
                          color: AppColors.indigo,
                          fontWeight: FontWeight.w800,
                        ),
                      ),

                      // Category + stock
                      const SizedBox(height: AppSpacing.sm),
                      Wrap(
                        spacing: AppSpacing.sm,
                        runSpacing: AppSpacing.sm,
                        children: [
                          if (product.category.isNotEmpty)
                            _InfoChip(
                              icon: Icons.category_outlined,
                              label: product.category,
                            ),
                          _InfoChip(
                            icon: outOfStock
                                ? Icons.error_outline
                                : Icons.inventory_2_outlined,
                            label: outOfStock
                                ? 'product_out_of_stock'.tr()
                                : 'product_in_stock'
                                    .tr(namedArgs: {'count': '${product.stock}'}),
                            color: outOfStock
                                ? AppColors.coral
                                : AppColors.teal,
                          ),
                        ],
                      ),

                       // Description
                       if (product.description.isNotEmpty) ...[
                         const SizedBox(height: AppSpacing.lg),
                         FormattedDescription(
                           text: product.description,
                           style: AppTextStyles.bodyMedium,
                         ),
                       ],

                      // Quantity selector
                      const SizedBox(height: AppSpacing.lg),
                      if (!outOfStock)
                        Row(
                          children: [
                            Text(
                              'product_quantity'.tr(),
                              style: AppTextStyles.labelLarge,
                            ),
                            const Spacer(),
                            _QuantityButton(
                              icon: Icons.remove,
                              tooltip: 'product_decrease_quantity'.tr(),
                              onPressed:
                                  quantity > 1 ? () => onQuantityChanged(quantity - 1) : null,
                            ),
                            Padding(
                              padding: const EdgeInsets.symmetric(
                                  horizontal: AppSpacing.md),
                              child: Text(
                                '$quantity',
                                style: AppTextStyles.headlineMedium,
                              ),
                            ),
                            _QuantityButton(
                              icon: Icons.add,
                              tooltip: 'product_increase_quantity'.tr(),
                              onPressed: quantity < product.stock
                                  ? () => onQuantityChanged(quantity + 1)
                                  : null,
                            ),
                          ],
                        ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),

        // Action buttons — large, accessible, clear
        Container(
          padding: EdgeInsets.all(AppSpacing.screenPadding),
          decoration: BoxDecoration(
            color: AppColors.cardSurface,
            border: Border(top: BorderSide(color: AppColors.parchmentDeep)),
          ),
          child: Row(
            children: [
              Expanded(
                child: Semantics(
                  button: true,
                  label: 'product_add_to_cart'.tr(),
                  child: FilledButton.icon(
                    onPressed: outOfStock ? null : onAddToCart,
                    style: FilledButton.styleFrom(
                      backgroundColor: AppColors.amber,
                      foregroundColor: AppColors.indigoDark,
                      minimumSize: const Size.fromHeight(
                          AccessibilityTokens.minTouchTarget),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(
                            AccessibilityTokens.radiusFull),
                      ),
                    ),
                    icon: const Icon(Icons.add_shopping_cart),
                    label: Text('product_add_to_cart'.tr()),
                  ),
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: Semantics(
                  button: true,
                  label: 'product_buy_now'.tr(),
                  child: FilledButton(
                    onPressed: outOfStock ? null : onBuyNow,
                    style: FilledButton.styleFrom(
                      backgroundColor: AppColors.indigo,
                      foregroundColor: AppColors.textOnPrimary,
                      minimumSize: const Size.fromHeight(
                          AccessibilityTokens.minTouchTarget),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(
                            AccessibilityTokens.radiusFull),
                      ),
                    ),
                    child: Text('product_buy_now'.tr()),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

}

// ── Small building blocks ────────────────────────────────────────────────────

class _RoundIconButton extends StatelessWidget {
  final IconData icon;
  final String tooltip;
  final VoidCallback onPressed;

  const _RoundIconButton({
    required this.icon,
    required this.tooltip,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: AppColors.cardSurface,
      shape: const CircleBorder(
        side: BorderSide(color: AppColors.parchmentDeep),
      ),
      child: Tooltip(
        message: tooltip,
        child: InkWell(
          customBorder: const CircleBorder(),
          onTap: onPressed,
          child: SizedBox(
            width: AccessibilityTokens.minTouchTarget,
            height: AccessibilityTokens.minTouchTarget,
            child: Icon(icon, color: AppColors.textPrimary),
          ),
        ),
      ),
    );
  }
}

class _InfoChip extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color? color;

  const _InfoChip({required this.icon, required this.label, this.color});

  @override
  Widget build(BuildContext context) {
    final effectiveColor = color ?? AppColors.textSecondary;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: AppColors.parchmentDeep,
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusFull),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: effectiveColor),
          const SizedBox(width: 4),
          Text(
            label,
            style: AppTextStyles.labelMedium.copyWith(
              color: effectiveColor,
            ),
          ),
        ],
      ),
    );
  }
}

class _QuantityButton extends StatelessWidget {
  final IconData icon;
  final String tooltip;
  final VoidCallback? onPressed;

  const _QuantityButton({
    required this.icon,
    required this.tooltip,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return IconButton.outlined(
      onPressed: onPressed,
      icon: Icon(icon),
      tooltip: tooltip,
      style: IconButton.styleFrom(
        minimumSize: const Size(AccessibilityTokens.minTouchTarget,
            AccessibilityTokens.minTouchTarget),
      ),
    );
  }
}
