import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';

import '../../../core/services/commerce_service.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/widgets/app_image.dart';
import '../../../core/widgets/empty_state.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

/// Fetches the authenticated user's cart from the backend (authoritative data).
final cartProvider = FutureProvider<Cart>(
    (ref) => ref.watch(commerceServiceProvider).getCart());

class CartScreen extends ConsumerWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final cartAsync = ref.watch(cartProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text('cart_title'.tr()),
      ),
      body: SafeArea(
        child: cartAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (error, _) => _CartError(
            error: error,
            onRetry: () => ref.invalidate(cartProvider),
          ),
          data: (cart) {
            if (cart.items.isEmpty) {
              return EmptyState(
                icon: Icons.shopping_cart_outlined,
                title: 'cart_empty'.tr(),
                message: 'cart_empty_desc'.tr(),
                actionLabel: 'cart_continue_shopping'.tr(),
                onAction: () => context.go('/marketplace'),
              );
            }
            return _CartContent(cart: cart);
          },
        ),
      ),
    );
  }
}

class _CartError extends StatelessWidget {
  final Object error;
  final VoidCallback onRetry;

  const _CartError({required this.error, required this.onRetry});

  @override
  Widget build(BuildContext context) {
    final isAuth = error is CommerceApiException &&
        (error as CommerceApiException).statusCode == 401;

    return EmptyState(
      icon: isAuth ? Icons.lock_outline : Icons.wifi_off,
      title: isAuth ? 'cart_login_required'.tr() : 'cart_load_failed'.tr(),
      message: isAuth ? 'cart_login_required_desc'.tr() : null,
      actionLabel: 'action_retry'.tr(),
      onAction: onRetry,
    );
  }
}

class _CartContent extends ConsumerStatefulWidget {
  final Cart cart;

  const _CartContent({required this.cart});

  @override
  ConsumerState<_CartContent> createState() => _CartContentState();
}

class _CartContentState extends ConsumerState<_CartContent> {
  final Set<String> _busyItemIds = {};

  Future<void> _mutate(
    Future<Cart> Function(CommerceService) mutation, {
    String? errorKey,
  }) async {
    try {
      await mutation(ref.read(commerceServiceProvider));
      ref.invalidate(cartProvider);
    } on CommerceApiException catch (e) {
      if (!mounted) return;
      final key = e.statusCode == 409
          ? 'cart_stock_limit_generic'
          : (errorKey ?? 'cart_update_failed');
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(key.tr()),
          backgroundColor: AppColors.coral,
        ),
      );
      ref.invalidate(cartProvider);
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text((errorKey ?? 'cart_update_failed').tr()),
          backgroundColor: AppColors.coral,
        ),
      );
    }
  }

  Future<void> _confirmClearCart() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('cart_clear_confirm_title'.tr()),
        content: Text('cart_clear_confirm_message'.tr()),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text('action_cancel'.tr()),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            style: FilledButton.styleFrom(
              backgroundColor: AppColors.coral,
            ),
            child: Text('cart_clear'.tr()),
          ),
        ],
      ),
    );
    if (confirmed == true) {
      await _mutate(
          (svc) => svc.clearCart().then((_) => widget.cart),
          errorKey: 'cart_clear_failed');
    }
  }

  @override
  Widget build(BuildContext context) {
    final cart = widget.cart;

    return Column(
      children: [
        Expanded(
          child: ListView.separated(
            padding: EdgeInsets.all(AppSpacing.screenPadding),
            itemCount: cart.items.length,
            separatorBuilder: (_, _) => const SizedBox(height: AppSpacing.md),
            itemBuilder: (context, index) {
              final item = cart.items[index];
              return _CartItemCard(
                item: item,
                isBusy: _busyItemIds.contains(item.id),
                onIncrease: () => _updateQuantity(item, item.quantity + 1),
                onDecrease: () => _updateQuantity(item, item.quantity - 1),
                onRemove: () => _mutate(
                  (svc) => svc.removeCartItem(item.id),
                  errorKey: 'cart_remove_failed',
                ),
              );
            },
          ),
        ),

        // Summary + checkout — totals are display-only; server is authoritative
        Container(
          padding: EdgeInsets.all(AppSpacing.screenPadding),
          decoration: BoxDecoration(
            color: AppColors.cardSurface,
            border: Border(top: BorderSide(color: AppColors.parchmentDeep)),
          ),
          child: SafeArea(
            top: false,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  children: [
                    Text(
                      'cart_subtotal'.tr(),
                      style: AppTextStyles.labelLarge,
                    ),
                    const Spacer(),
                    Text(
                      '₹${cart.subtotal.toStringAsFixed(0)}',
                      style: AppTextStyles.headlineMedium.copyWith(
                        color: AppColors.indigo,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.xs),
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    'cart_totals_note'.tr(),
                    style: AppTextStyles.labelSmall.copyWith(
                      color: AppColors.textSecondary,
                    ),
                  ),
                ),
                const SizedBox(height: AppSpacing.md),
                Row(
                  children: [
                    // Clear cart
                    Semantics(
                      button: true,
                      label: 'cart_clear'.tr(),
                      child: OutlinedButton(
                        onPressed: _confirmClearCart,
                        style: OutlinedButton.styleFrom(
                          minimumSize: const Size(
                            AccessibilityTokens.minTouchTargetLarge,
                            AccessibilityTokens.minTouchTarget,
                          ),
                          foregroundColor: AppColors.coral,
                          side: const BorderSide(color: AppColors.coral),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(
                                AccessibilityTokens.radiusFull),
                          ),
                        ),
                        child: Text('cart_clear'.tr()),
                      ),
                    ),
                    const SizedBox(width: AppSpacing.md),
                    Expanded(
                      child: Semantics(
                        button: true,
                        label: 'cart_checkout'.tr(),
                        child: FilledButton(
                          onPressed: () => context.push('/checkout'),
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
                          child: Text('cart_checkout'.tr()),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Future<void> _updateQuantity(CartItem item, int newQuantity) async {
    if (newQuantity > item.stock) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'cart_stock_limit'.tr(namedArgs: {'count': '${item.stock}'}),
          ),
          backgroundColor: AppColors.coral,
        ),
      );
      return;
    }
    setState(() => _busyItemIds.add(item.id));
    try {
      await _mutate(
        (svc) => svc.updateCartItem(item.id, newQuantity),
        errorKey: 'cart_update_failed',
      );
    } finally {
      if (mounted) setState(() => _busyItemIds.remove(item.id));
    }
  }
}

class _CartItemCard extends StatelessWidget {
  final CartItem item;
  final bool isBusy;
  final VoidCallback onIncrease;
  final VoidCallback onDecrease;
  final VoidCallback onRemove;

  const _CartItemCard({
    required this.item,
    required this.isBusy,
    required this.onIncrease,
    required this.onDecrease,
    required this.onRemove,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: AppColors.cardSurface,
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
        border: Border.all(color: AppColors.parchmentDeep),
      ),
      child: Opacity(
        opacity: isBusy ? 0.5 : 1,
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Image
            ClipRRect(
              borderRadius: BorderRadius.circular(AccessibilityTokens.radiusMd),
              child: SizedBox(
                width: 72,
                height: 72,
                child: AppImage(
                  imageUrl: item.imageUrl,
                  fallbackWidget: Container(
                    color: AppColors.parchmentDeep,
                    child: const Icon(Icons.image,
                        color: AppColors.textSecondary),
                  ),
                ),
              ),
            ),
            const SizedBox(width: AppSpacing.md),

            // Info
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    item.title.isNotEmpty
                        ? item.title
                        : 'cart_item_unavailable'.tr(),
                    style: AppTextStyles.labelLarge,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    '₹${item.unitPrice.toStringAsFixed(0)}',
                    style: AppTextStyles.labelMedium.copyWith(
                      color: AppColors.textSecondary,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  Row(
                    children: [
                      // Decrease (removes item at quantity 1)
                      _QtyIconButton(
                        icon: item.quantity <= 1
                            ? Icons.delete_outline
                            : Icons.remove,
                        tooltip: item.quantity <= 1
                            ? 'cart_remove_item'.tr()
                            : 'product_decrease_quantity'.tr(),
                        onPressed: isBusy ? null : onDecrease,
                      ),
                      Padding(
                        padding: const EdgeInsets.symmetric(
                            horizontal: AppSpacing.md),
                        child: Text(
                          '${item.quantity}',
                          style: AppTextStyles.labelLarge,
                        ),
                      ),
                      _QtyIconButton(
                        icon: Icons.add,
                        tooltip: 'product_increase_quantity'.tr(),
                        onPressed: isBusy ? null : onIncrease,
                      ),
                      const Spacer(),
                      Text(
                        '₹${item.lineTotal.toStringAsFixed(0)}',
                        style: AppTextStyles.headlineSmall.copyWith(
                          color: AppColors.indigo,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            // Remove
            IconButton(
              icon: const Icon(Icons.close),
              tooltip: 'cart_remove_item'.tr(),
              onPressed: isBusy ? null : onRemove,
            ),
          ],
        ),
      ),
    );
  }
}

class _QtyIconButton extends StatelessWidget {
  final IconData icon;
  final String tooltip;
  final VoidCallback? onPressed;

  const _QtyIconButton({
    required this.icon,
    required this.tooltip,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return IconButton.outlined(
      onPressed: onPressed,
      icon: Icon(icon, size: 20),
      tooltip: tooltip,
      style: IconButton.styleFrom(
        minimumSize: const Size(
          AccessibilityTokens.minTouchTargetCompact,
          AccessibilityTokens.minTouchTargetCompact,
        ),
      ),
    );
  }
}
