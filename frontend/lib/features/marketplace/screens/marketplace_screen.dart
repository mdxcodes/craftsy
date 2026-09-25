import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';
import '../../../core/services/marketplace_service.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/widgets/app_image.dart';
import '../../../core/widgets/empty_state.dart';

// ── Providers ────────────────────────────────────────────────────────────────

final marketplaceSearchQueryProvider = StateProvider<String>((ref) => '');
final marketplaceSelectedCategoryProvider = StateProvider<String?>((ref) => null);

/// Live products for the current search + category filter.
final marketplaceProductsProvider =
    FutureProvider<List<MarketplaceProduct>>((ref) async {
  final search = ref.watch(marketplaceSearchQueryProvider);
  final category = ref.watch(marketplaceSelectedCategoryProvider);
  return marketplaceService.getProducts(
    category: category,
    search: search.isEmpty ? null : search,
  );
});

final marketplaceCategoriesProvider = FutureProvider<List<String>>((ref) async {
  return marketplaceService.getCategories();
});

// ── Screen ───────────────────────────────────────────────────────────────────

class MarketplaceScreen extends ConsumerStatefulWidget {
  const MarketplaceScreen({super.key});

  @override
  ConsumerState<MarketplaceScreen> createState() => _MarketplaceScreenState();
}

class _MarketplaceScreenState extends ConsumerState<MarketplaceScreen> {
  Timer? _debounce;

  @override
  void dispose() {
    _debounce?.cancel();
    super.dispose();
  }

  void _onSearchChanged(String value) {
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 300), () {
      ref.read(marketplaceSearchQueryProvider.notifier).state = value.trim();
    });
  }

  @override
  Widget build(BuildContext context) {
    final productsAsync = ref.watch(marketplaceProductsProvider);
    final categoriesAsync = ref.watch(marketplaceCategoriesProvider);
    final selectedCategory = ref.watch(marketplaceSelectedCategoryProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text('marketplace_title'.tr()),
        actions: [
          IconButton(
            icon: const Icon(Icons.shopping_cart_outlined),
            tooltip: 'cart_title'.tr(),
            onPressed: () => context.push('/my-cart'),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Subtitle
            Padding(
              padding: EdgeInsets.symmetric(
                horizontal: AppSpacing.screenPadding,
              ),
              child: Text(
                'marketplace_subtitle'.tr(),
                style: AppTextStyles.bodyMedium,
              ),
            ),

            // Search bar
            Padding(
              padding: EdgeInsets.symmetric(
                horizontal: AppSpacing.screenPadding,
              ),
              child: TextField(
                onChanged: _onSearchChanged,
                decoration: InputDecoration(
                  hintText: 'marketplace_search_hint'.tr(),
                  prefixIcon: const Icon(Icons.search),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide.none,
                  ),
                  filled: true,
                  fillColor: AppColors.cardSurface,
                ),
              ),
            ),

            const SizedBox(height: AppSpacing.md),

            // Category chips
            categoriesAsync.when(
              data: (categories) {
                if (categories.isEmpty) return const SizedBox.shrink();
                return SizedBox(
                  height: 40,
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    padding: EdgeInsets.symmetric(
                      horizontal: AppSpacing.screenPadding,
                    ),
                    itemCount: categories.length + 1,
                    itemBuilder: (context, index) {
                      if (index == 0) {
                        return _CategoryChip(
                          label: 'marketplace_all'.tr(),
                          isSelected: selectedCategory == null,
                          onTap: () => ref
                              .read(marketplaceSelectedCategoryProvider
                                  .notifier)
                              .state = null,
                        );
                      }
                      final category = categories[index - 1];
                      return _CategoryChip(
                        label: category,
                        isSelected: selectedCategory == category,
                        onTap: () => ref
                            .read(marketplaceSelectedCategoryProvider.notifier)
                            .state = category,
                      );
                    },
                  ),
                );
              },
              loading: () => const SizedBox.shrink(),
              error: (_, _) => const SizedBox.shrink(),
            ),

            const SizedBox(height: AppSpacing.md),

            // Products grid
            Expanded(
              child: productsAsync.when(
                data: (products) {
                  if (products.isEmpty) {
                    return EmptyState(
                      icon: Icons.shopping_bag_outlined,
                      title: 'marketplace_no_products'.tr(),
                      message: 'marketplace_no_products_desc'.tr(),
                    );
                  }

                  return RefreshIndicator(
                    onRefresh: () async =>
                        ref.refresh(marketplaceProductsProvider.future),
                    child: GridView.builder(
                      padding: EdgeInsets.symmetric(
                        horizontal: AppSpacing.screenPadding,
                      ),
                      gridDelegate:
                          const SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: 2,
                        childAspectRatio: 0.65,
                        crossAxisSpacing: AppSpacing.md,
                        mainAxisSpacing: AppSpacing.md,
                      ),
                      itemCount: products.length,
                      itemBuilder: (context, index) {
                        final product = products[index];
                        return _ProductCard(product: product);
                      },
                    ),
                  );
                },
                loading: () => const Center(
                  child: CircularProgressIndicator(),
                ),
                error: (error, _) => Center(
                  child: Text('Error: $error'),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _CategoryChip extends StatelessWidget {
  final String label;
  final bool isSelected;
  final VoidCallback onTap;

  const _CategoryChip({
    required this.label,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: isSelected ? AppColors.indigo : AppColors.cardSurface,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: isSelected ? AppColors.indigo : AppColors.parchmentDeep,
            ),
          ),
          child: Text(
            label,
            style: AppTextStyles.labelLarge.copyWith(
              color: isSelected ? AppColors.textOnPrimary : AppColors.textPrimary,
            ),
          ),
        ),
      ),
    );
  }
}

class _ProductCard extends StatelessWidget {
  final MarketplaceProduct product;

  const _ProductCard({required this.product});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/marketplace/product/${product.id}'),
      child: Container(
        decoration: BoxDecoration(
          color: AppColors.cardSurface,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.parchmentDeep),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Product image
            Expanded(
              child: ClipRRect(
                borderRadius: const BorderRadius.vertical(
                  top: Radius.circular(12),
                ),
                child: AppImage(
                  imageUrl: product.imageUrl,
                  fallbackWidget: Container(
                    color: AppColors.parchmentDeep,
                    child: const Icon(
                      Icons.image,
                      size: 48,
                      color: AppColors.textSecondary,
                    ),
                  ),
                ),
              ),
            ),

            // Product info
            Padding(
              padding: const EdgeInsets.all(8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    product.title,
                    style: AppTextStyles.labelLarge,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '₹${product.price.toStringAsFixed(0)}',
                    style: AppTextStyles.headlineSmall.copyWith(
                      color: AppColors.indigo,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
