import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../core/widgets/app_button.dart';
import '../../../core/widgets/app_scaffold.dart';
import '../../../core/widgets/app_image.dart';
import '../../../core/widgets/app_confirmation_dialog.dart';
import '../../../core/widgets/visual_status_chip.dart';
import '../../../core/widgets/motifs/craft_category_badge.dart';
import '../../../core/widgets/formatted_description.dart';
import '../../commerce/widgets/where_i_sell_section.dart';
import '../../../core/providers/commerce_hub_provider.dart';
import '../../../core/providers/app_providers.dart';
import '../../../data/models/product.dart';
import '../../social_media/providers/social_media_provider.dart';
import '../../social_media/widgets/social_media_launchpad_sheet.dart';

class ProductDetailScreen extends ConsumerWidget {
  final String productId;

  const ProductDetailScreen({super.key, required this.productId});

  void _showEditDialog(BuildContext context, WidgetRef ref, Product product) {
    final titleCtrl = TextEditingController(text: product.title);
    final descCtrl = TextEditingController(text: product.description);
    final priceCtrl = TextEditingController(
      text: product.price.toStringAsFixed(0),
    );

    showDialog(
      context: context,
      builder: (ctx) {
        return Dialog(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppRadii.dialog),
          ),
          backgroundColor: AppColors.cardSurface,
          insetPadding: const EdgeInsets.symmetric(
            horizontal: AppSpacing.screenPadding,
            vertical: AppSpacing.lg,
          ),
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.cardPadding),
            child: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'edit_product_title'.tr(),
                    style: AppTextStyles.headlineSmall.copyWith(
                      color: AppColors.espresso,
                      fontWeight: FontWeight.w600,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: AppSpacing.md),
                  TextField(
                    controller: titleCtrl,
                    decoration: InputDecoration(
                      labelText: 'product_title_label'.tr(),
                      filled: true,
                      fillColor: AppColors.cardSurface,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  TextField(
                    controller: priceCtrl,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      labelText: '${'price_label'.tr()} (₹)',
                      prefixText: '₹ ',
                      filled: true,
                      fillColor: AppColors.cardSurface,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  TextField(
                    controller: descCtrl,
                    maxLines: 3,
                    decoration: InputDecoration(
                      labelText: 'product_desc_label'.tr(),
                      filled: true,
                      fillColor: AppColors.cardSurface,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.lg),
                  AppButton(
                    label: 'save'.tr(),
                    onPressed: () async {
                      final updated = product.copyWith(
                        title: titleCtrl.text.trim(),
                        description: descCtrl.text.trim(),
                        price: double.tryParse(priceCtrl.text) ?? product.price,
                      );
                      await ref
                          .read(productListProvider.notifier)
                          .updateProduct(updated);
                      if (ctx.mounted) {
                        Navigator.pop(ctx);
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('product_updated_success'.tr()),
                          ),
                        );
                      }
                    },
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  AppButton(
                    label: 'cancel'.tr(),
                    type: AppButtonType.secondary,
                    onPressed: () => Navigator.pop(ctx),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  void _showDeleteDialog(BuildContext context, WidgetRef ref) {
    showAppConfirmationDialog(
      context: context,
      title: 'delete_product_confirm_title'.tr(),
      message: 'delete_product_confirm_msg'.tr(),
      icon: Icons.delete_outline_rounded,
      confirmLabel: 'delete'.tr(),
      isDestructive: true,
      onConfirm: () async {
        await ref.read(productListProvider.notifier).deleteProduct(productId);
        if (context.mounted) {
          Navigator.of(context, rootNavigator: true).pop();
          context.pop();
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('product_deleted_success'.tr())),
          );
        }
      },
    );
  }

  void _showSoldOutDialog(
    BuildContext context,
    WidgetRef ref,
    Product product,
  ) {
    showAppConfirmationDialog(
      context: context,
      title: 'mark_sold_out_dialog_title'.tr(),
      message: 'mark_sold_out_dialog_msg'.tr(),
      icon: Icons.pause_circle_outline_rounded,
      confirmLabel: 'mark_sold_out_btn'.tr(),
      confirmColor: AppColors.sienna,
      onConfirm: () async {
        final updated = product.copyWith(
          status: ProductStatus.soldOut,
          statusUpdatedAt: DateTime.now(),
        );
        await ref.read(productListProvider.notifier).updateProduct(updated);
        if (context.mounted) {
          Navigator.of(context, rootNavigator: true).pop();
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('product_marked_sold_out'.tr()),
              backgroundColor: AppColors.sienna,
            ),
          );
        }
      },
    );
  }

  void _showRemoveListingDialog(
    BuildContext context,
    WidgetRef ref,
    Product product,
  ) {
    showAppConfirmationDialog(
      context: context,
      title: 'remove_listing_dialog_title'.tr(),
      icon: Icons.visibility_off_outlined,
      confirmLabel: 'remove_listing_btn'.tr(),
      confirmColor: AppColors.goldDark,
      contentWidget: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(height: AppSpacing.sm),
          Text(
            'remove_listing_dialog_msg'.tr(),
            style: const TextStyle(fontSize: 14, color: AppColors.espresso),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: AppSpacing.sm),
          Container(
            padding: const EdgeInsets.all(AppSpacing.sm),
            decoration: BoxDecoration(
              color: AppColors.warmMist,
              borderRadius: BorderRadius.circular(AppRadii.sm),
              border: Border.all(color: AppColors.line),
            ),
            child: Text(
              '• ${'remove_listing_note_1'.tr()}\n• ${'remove_listing_note_2'.tr()}\n• ${'remove_listing_note_3'.tr()}',
              style: const TextStyle(
                fontSize: 13,
                color: AppColors.taupe,
                height: 1.4,
              ),
            ),
          ),
        ],
      ),
      onConfirm: () async {
        final updated = product.copyWith(
          status: ProductStatus.listingRemoved,
          statusUpdatedAt: DateTime.now(),
        );
        await ref.read(productListProvider.notifier).updateProduct(updated);
        if (context.mounted) {
          Navigator.of(context, rootNavigator: true).pop();
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('product_removed_ondc'.tr()),
              backgroundColor: AppColors.espresso,
            ),
          );
        }
      },
    );
  }

  Future<void> _relistProduct(
    BuildContext context,
    WidgetRef ref,
    Product product,
  ) async {
    final updated = product.copyWith(
      status: ProductStatus.live,
      statusUpdatedAt: DateTime.now(),
    );
    await ref.read(productListProvider.notifier).updateProduct(updated);
    if (context.mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('product_relisted_live'.tr()),
          backgroundColor: AppColors.statusSuccessFg,
        ),
      );
    }
  }

  void _showLegendDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (ctx) => Dialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppRadii.dialog),
        ),
        backgroundColor: AppColors.cardSurface,
        insetPadding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.screenPadding,
          vertical: AppSpacing.lg,
        ),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.cardPadding),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                'listing_guide_title'.tr(),
                style: AppTextStyles.headlineSmall.copyWith(
                  color: AppColors.espresso,
                  fontWeight: FontWeight.w600,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: AppSpacing.md),
              Text(
                '• ${'mark_sold_out_dialog_title'.tr()}:',
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  color: AppColors.espresso,
                ),
              ),
              Text(
                '${'mark_sold_out_dialog_msg'.tr()}\n',
                style: const TextStyle(color: AppColors.taupe),
              ),
              Text(
                '• ${'remove_listing_dialog_title'.tr()}:',
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  color: AppColors.espresso,
                ),
              ),
              Text(
                '${'remove_vs_delete_hint'.tr()}\n',
                style: const TextStyle(color: AppColors.taupe),
              ),
              Text(
                '• ${'delete_product_confirm_title'.tr()}:',
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  color: AppColors.error,
                ),
              ),
              Text(
                'delete_product_confirm_msg'.tr(),
                style: const TextStyle(color: AppColors.taupe),
              ),
              const SizedBox(height: AppSpacing.lg),
              AppButton(
                label: 'understood_btn'.tr(),
                onPressed: () => Navigator.pop(ctx),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _statusLabelKey(ProductStatus status) {
    switch (status) {
      case ProductStatus.live:
        return 'status_live';
      case ProductStatus.pendingSync:
        return 'status_pending_sync';
      case ProductStatus.draft:
        return 'status_draft';
      case ProductStatus.sold:
        return 'status_sold';
      case ProductStatus.soldOut:
        return 'status_sold_out';
      case ProductStatus.listingRemoved:
        return 'status_listing_removed';
    }
  }

  VisualStatusType _mapStatusToVisualType(ProductStatus status) {
    switch (status) {
      case ProductStatus.live:
        return VisualStatusType.success;
      case ProductStatus.pendingSync:
        return VisualStatusType.warning;
      case ProductStatus.draft:
        return VisualStatusType.pending;
      case ProductStatus.sold:
        return VisualStatusType.success;
      case ProductStatus.soldOut:
        return VisualStatusType.error;
      case ProductStatus.listingRemoved:
        return VisualStatusType.offline;
    }
  }

  Widget _buildCategoryBadge(String category) {
    final l = category.toLowerCase();
    if (l.contains('pottery') || l.contains('ceramic') || l.contains('clay')) {
      return CraftCategoryBadge(
        label: category,
        icon: CraftCategoryIcons.pottery(),
        isActive: false,
      );
    }
    if (l.contains('textile') ||
        l.contains('saree') ||
        l.contains('chanderi') ||
        l.contains('silk') ||
        l.contains('cotton') ||
        l.contains('fabric') ||
        l.contains('dupatta')) {
      return CraftCategoryBadge(
        label: category,
        icon: CraftCategoryIcons.textile(),
        isActive: false,
      );
    }
    if (l.contains('jewel')) {
      return CraftCategoryBadge(
        label: category,
        icon: CraftCategoryIcons.jewelry(),
        isActive: false,
      );
    }
    if (l.contains('wood')) {
      return CraftCategoryBadge(
        label: category,
        icon: CraftCategoryIcons.woodwork(),
        isActive: false,
      );
    }
    return CraftCategoryBadge.all(label: category, isActive: false);
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final _ = Localizations.maybeLocaleOf(context);
    final _ = ref.watch(userProfileProvider).preferredLanguage;
    final productsAsync = ref.watch(productListProvider);

    return AppScaffold(
      body: productsAsync.when(
        loading: () => Center(
          child: Semantics(
            label: 'loading'.tr(),
            liveRegion: true,
            child: const CircularProgressIndicator(),
          ),
        ),
        error: (err, stack) => Center(
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.screenPadding),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(
                  Icons.error_outline,
                  size: 48,
                  color: AppColors.siennaDark,
                ),
                const SizedBox(height: AppSpacing.md),
                Text(
                  'error_loading_product'.tr(),
                  style: AppTextStyles.headlineMedium,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: AppSpacing.sm),
                AppButton(
                  label: 'retry'.tr(),
                  width: 140,
                  onPressed: () {
                    ref
                        .read(productListProvider.notifier)
                        .loadProducts(forceRefresh: true);
                  },
                ),
              ],
            ),
          ),
        ),
        data: (products) {
          final product = products.firstWhere(
            (p) => p.id == productId,
            orElse: () => Product(
              id: productId,
              title: 'product_fallback_title'.tr(),
              description: 'product_fallback_desc'.tr(),
              price: 0,
              photoPath: '',
              category: 'General',
            ),
          );

          final visualType = _mapStatusToVisualType(product.status);
          final isNonLive = product.isNonLive;

          return CustomScrollView(
            slivers: [
              SliverAppBar(
                expandedHeight: 340,
                pinned: true,
                backgroundColor: AppColors.background,
                elevation: 0,
                leading: Padding(
                  padding: const EdgeInsets.only(
                    left: AppSpacing.screenPadding,
                  ),
                  child: Center(
                    child: _CircleHeaderButton(
                      onTap: () => Navigator.of(context).pop(),
                      child: const Icon(
                        Icons.arrow_back,
                        color: AppColors.espresso,
                        size: 20,
                      ),
                    ),
                  ),
                ),
                actions: [
                  Center(
                    child: _CircleHeaderButton(
                      tooltip: 'edit'.tr(),
                      onTap: () => _showEditDialog(context, ref, product),
                      child: const Icon(
                        Icons.edit_outlined,
                        color: AppColors.espresso,
                        size: 19,
                      ),
                    ),
                  ),
                  const SizedBox(width: AppSpacing.xs),
                  Padding(
                    padding: const EdgeInsets.only(
                      right: AppSpacing.screenPadding,
                    ),
                    child: Center(
                      child: Container(
                        width: 38,
                        height: 38,
                        decoration: BoxDecoration(
                          color: AppColors.cardSurface.withValues(alpha: 0.92),
                          shape: BoxShape.circle,
                          border: Border.all(color: AppColors.line),
                          boxShadow: AppElevation.cardShadow,
                        ),
                        child: PopupMenuButton<String>(
                          padding: EdgeInsets.zero,
                          icon: const Icon(
                            Icons.more_vert,
                            color: AppColors.espresso,
                            size: 20,
                          ),
                          tooltip: 'listing_actions'.tr(),
                          color: AppColors.cardSurface,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(AppRadii.card),
                            side: const BorderSide(color: AppColors.line),
                          ),
                          onSelected: (val) {
                            switch (val) {
                              case 'sold_out':
                                _showSoldOutDialog(context, ref, product);
                                break;
                              case 'remove_listing':
                                _showRemoveListingDialog(context, ref, product);
                                break;
                              case 'relist':
                                _relistProduct(context, ref, product);
                                break;
                              case 'delete':
                                _showDeleteDialog(context, ref);
                                break;
                              case 'legend':
                                _showLegendDialog(context);
                                break;
                            }
                          },
                          itemBuilder: (ctx) => [
                            if (isNonLive)
                              PopupMenuItem(
                                value: 'relist',
                                child: Row(
                                  children: [
                                    const Icon(
                                      Icons.refresh,
                                      color: AppColors.sage,
                                      size: 18,
                                    ),
                                    const SizedBox(width: 8),
                                    Text('relist_item_btn'.tr()),
                                  ],
                                ),
                              )
                            else ...[
                              PopupMenuItem(
                                value: 'sold_out',
                                child: Row(
                                  children: [
                                    const Icon(
                                      Icons.remove_shopping_cart_outlined,
                                      color: AppColors.sienna,
                                      size: 18,
                                    ),
                                    const SizedBox(width: 8),
                                    Text('mark_sold_out_btn'.tr()),
                                  ],
                                ),
                              ),
                              PopupMenuItem(
                                value: 'remove_listing',
                                child: Row(
                                  children: [
                                    const Icon(
                                      Icons.visibility_off_outlined,
                                      color: AppColors.taupe,
                                      size: 18,
                                    ),
                                    const SizedBox(width: 8),
                                    Text('remove_listing_btn'.tr()),
                                  ],
                                ),
                              ),
                            ],
                            const PopupMenuDivider(),
                            PopupMenuItem(
                              value: 'legend',
                              child: Row(
                                children: [
                                  const Icon(
                                    Icons.info_outline,
                                    size: 18,
                                    color: AppColors.taupe,
                                  ),
                                  const SizedBox(width: 8),
                                  Text('listing_info_btn'.tr()),
                                ],
                              ),
                            ),
                            PopupMenuItem(
                              value: 'delete',
                              child: Row(
                                children: [
                                  const Icon(
                                    Icons.delete_outline,
                                    color: AppColors.error,
                                    size: 18,
                                  ),
                                  const SizedBox(width: 8),
                                  Text(
                                    'delete'.tr(),
                                    style: const TextStyle(
                                      color: AppColors.error,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
                flexibleSpace: FlexibleSpaceBar(
                  background: ColorFiltered(
                    colorFilter: isNonLive
                        ? const ColorFilter.mode(
                            Colors.grey,
                            BlendMode.saturation,
                          )
                        : const ColorFilter.mode(
                            Colors.transparent,
                            BlendMode.multiply,
                          ),
                    child: Opacity(
                      opacity: isNonLive ? 0.72 : 1.0,
                      child: AppImage(
                        imageUrl: product.displayPhotoPath,
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                ),
              ),
              SliverPadding(
                padding: const EdgeInsets.all(AppSpacing.screenPadding),
                sliver: SliverList(
                  delegate: SliverChildListDelegate([
                    if (product.allPhotoPaths.length > 1) ...[
                      SizedBox(
                        height: 68,
                        child: ListView(
                          scrollDirection: Axis.horizontal,
                          children: [
                            for (final path in product.allPhotoPaths)
                              Padding(
                                padding: const EdgeInsets.only(
                                  right: AppSpacing.xs,
                                ),
                                child: Container(
                                  width: 68,
                                  height: 68,
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(
                                      AppRadii.card,
                                    ),
                                    border: Border.all(color: AppColors.line),
                                    boxShadow: AppElevation.cardShadow,
                                  ),
                                  clipBehavior: Clip.antiAlias,
                                  child: ColorFiltered(
                                    colorFilter: isNonLive
                                        ? const ColorFilter.mode(
                                            Colors.grey,
                                            BlendMode.saturation,
                                          )
                                        : const ColorFilter.mode(
                                            Colors.transparent,
                                            BlendMode.multiply,
                                          ),
                                    child: AppImage(
                                      imageUrl: path,
                                      fit: BoxFit.cover,
                                    ),
                                  ),
                                ),
                              ),
                          ],
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),
                    ],

                    // Category badge & status row
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        if (product.category.trim().isNotEmpty) ...[
                          Flexible(
                            child: _buildCategoryBadge(product.category),
                          ),
                          const SizedBox(width: 8),
                        ],
                        VisualStatusChip(
                          type: visualType,
                          label: _statusLabelKey(product.status).tr(),
                          compact: true,
                        ),
                      ],
                    ),

                    const SizedBox(height: AppSpacing.sm),

                    // Title
                    Builder(
                      builder: (context) {
                        final isHindi =
                            (Localizations.maybeLocaleOf(
                                  context,
                                )?.languageCode ??
                                EasyLocalization.of(
                                  context,
                                )?.locale.languageCode) ==
                            'hi';
                        final primaryTitle =
                            (isHindi && product.titleHi.trim().isNotEmpty)
                            ? product.titleHi
                            : product.title;
                        final secondaryTitle =
                            (isHindi && product.titleHi.trim().isNotEmpty)
                            ? product.title
                            : (product.titleHi.trim().isNotEmpty
                                  ? product.titleHi
                                  : null);

                        return Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              primaryTitle,
                              style: AppTextStyles.headlineMedium.copyWith(
                                color: AppColors.espresso,
                                fontWeight: FontWeight.w600,
                                height: 1.25,
                              ),
                            ),
                            if (secondaryTitle != null &&
                                secondaryTitle.isNotEmpty) ...[
                              const SizedBox(height: 4),
                              Text(
                                secondaryTitle,
                                style: AppTextStyles.bodyMedium.copyWith(
                                  color: AppColors.taupe,
                                ),
                              ),
                            ],
                          ],
                        );
                      },
                    ),

                    const SizedBox(height: AppSpacing.sm),

                    // Price
                    Text(
                      '₹${product.price.toStringAsFixed(0)}',
                      style: AppTextStyles.headlineLarge.copyWith(
                        color: isNonLive
                            ? AppColors.taupe
                            : AppColors.burgundyDark,
                        fontWeight: FontWeight.w700,
                      ),
                    ),

                    const SizedBox(height: AppSpacing.md),

                    // Promote on Social Media Action Button
                    AppButton(
                      label: 'social_media_helper'.tr(),
                      icon: Icons.share_rounded,
                      onPressed: () => showSocialMediaLaunchpadSheet(
                        context,
                        SocialMediaArgs(
                          listingId: product.id,
                          source: 'catalogue',
                          allImages: product.allPhotoPaths,
                          title: product.title,
                          category: product.category,
                          description: product.description,
                          materials: product.tags,
                        ),
                      ),
                    ),

                    const SizedBox(height: AppSpacing.md),

                    // Listing Management Actions Box
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(AppSpacing.cardPadding),
                      decoration: BoxDecoration(
                        color: isNonLive
                            ? AppColors.warmMist.withValues(alpha: 0.6)
                            : AppColors.cardSurface,
                        borderRadius: BorderRadius.circular(AppRadii.card),
                        border: Border.all(color: AppColors.line),
                        boxShadow: AppElevation.cardShadow,
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Flexible(
                                child: Text(
                                  'listing_status_header'.tr(),
                                  style: AppTextStyles.labelSmall.copyWith(
                                    color: AppColors.taupe,
                                    letterSpacing: 0.8,
                                    fontWeight: FontWeight.w700,
                                  ),
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                              if (product.statusUpdatedAt != null) ...[
                                const SizedBox(width: 8),
                                Flexible(
                                  child: Text(
                                    'status_updated_at'.tr(
                                      namedArgs: {
                                        'date':
                                            '${product.statusUpdatedAt!.day}/${product.statusUpdatedAt!.month}/${product.statusUpdatedAt!.year}',
                                      },
                                    ),
                                    style: AppTextStyles.caption.copyWith(
                                      color: AppColors.taupe,
                                    ),
                                    textAlign: TextAlign.end,
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ),
                              ],
                            ],
                          ),
                          const SizedBox(height: AppSpacing.sm),
                          if (isNonLive) ...[
                            AppButton(
                              label: 'relist_item_btn'.tr(),
                              icon: Icons.refresh,
                              type: AppButtonType.secondary,
                              onPressed: () =>
                                  _relistProduct(context, ref, product),
                            ),
                          ] else ...[
                            IntrinsicHeight(
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.stretch,
                                children: [
                                  Expanded(
                                    child: OutlinedButton(
                                      onPressed: () => _showSoldOutDialog(
                                        context,
                                        ref,
                                        product,
                                      ),
                                      style: OutlinedButton.styleFrom(
                                        backgroundColor:
                                            AppColors.warmMist,
                                        side: const BorderSide(
                                          color: AppColors.line,
                                        ),
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(
                                            AppRadii.button,
                                          ),
                                        ),
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 8,
                                          vertical: 10,
                                        ),
                                      ),
                                      child: Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.center,
                                        children: [
                                          const Icon(
                                            Icons.remove_shopping_cart_outlined,
                                            size: 16,
                                            color: AppColors.sienna,
                                          ),
                                          const SizedBox(width: 6),
                                          Flexible(
                                            child: Text(
                                              'mark_sold_out_btn'.tr(),
                                              textAlign: TextAlign.center,
                                              maxLines: 2,
                                              style: AppTextStyles.labelMedium
                                                  .copyWith(
                                                    color: AppColors.sienna,
                                                    fontWeight: FontWeight.w600,
                                                    fontSize: 12,
                                                    height: 1.2,
                                                  ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                  const SizedBox(width: AppSpacing.sm),
                                  Expanded(
                                    child: OutlinedButton(
                                      onPressed: () => _showRemoveListingDialog(
                                        context,
                                        ref,
                                        product,
                                      ),
                                      style: OutlinedButton.styleFrom(
                                        backgroundColor:
                                            AppColors.warmMist,
                                        side: const BorderSide(
                                          color: AppColors.line,
                                        ),
                                        shape: RoundedRectangleBorder(
                                          borderRadius: BorderRadius.circular(
                                            AppRadii.button,
                                          ),
                                        ),
                                        padding: const EdgeInsets.symmetric(
                                          horizontal: 8,
                                          vertical: 10,
                                        ),
                                      ),
                                      child: Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.center,
                                        children: [
                                          const Icon(
                                            Icons.visibility_off_outlined,
                                            size: 16,
                                            color: AppColors.taupe,
                                          ),
                                          const SizedBox(width: 6),
                                          Flexible(
                                            child: Text(
                                              'remove_listing_btn'.tr(),
                                              textAlign: TextAlign.center,
                                              maxLines: 2,
                                              style: AppTextStyles.labelMedium
                                                  .copyWith(
                                                    color: AppColors.taupe,
                                                    fontWeight: FontWeight.w600,
                                                    fontSize: 12,
                                                    height: 1.2,
                                                  ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                          const SizedBox(height: AppSpacing.sm),
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Icon(
                                Icons.info_outline,
                                size: 14,
                                color: AppColors.taupe,
                              ),
                              const SizedBox(width: 6),
                              Expanded(
                                child: Text(
                                  'remove_vs_delete_hint'.tr(),
                                  style: AppTextStyles.caption.copyWith(
                                    color: AppColors.taupe,
                                    fontSize: 11,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: AppSpacing.md),

                    // Where I Sell — Channel Status Section
                    WhereISellSection(
                      productId: product.id,
                      onRefresh: () {
                        ref.invalidate(productChannelsProvider(product.id));
                      },
                    ),

                    const SizedBox(height: AppSpacing.md),

                    // Description Card
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(AppSpacing.cardPadding),
                      decoration: BoxDecoration(
                        color: AppColors.cardSurface,
                        borderRadius: BorderRadius.circular(AppRadii.card),
                        border: Border.all(color: AppColors.line),
                        boxShadow: AppElevation.cardShadow,
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'product_desc_label'.tr(),
                            style: AppTextStyles.labelSmall.copyWith(
                              color: AppColors.taupe,
                              letterSpacing: 0.8,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                          const SizedBox(height: AppSpacing.xs),
                          FormattedDescription(
                            text: product.description,
                            style: AppTextStyles.bodyMedium.copyWith(
                              color: AppColors.espresso,
                              height: 1.5,
                            ),
                          ),
                          if (product.descriptionHi.isNotEmpty) ...[
                            const SizedBox(height: AppSpacing.sm),
                            FormattedDescription(
                              text: product.descriptionHi,
                              style: AppTextStyles.bodyMedium.copyWith(
                                color: AppColors.taupe,
                                height: 1.5,
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),

                    if (product.tags.isNotEmpty) ...[
                      const SizedBox(height: AppSpacing.md),
                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(AppSpacing.cardPadding),
                        decoration: BoxDecoration(
                          color: AppColors.cardSurface,
                          borderRadius: BorderRadius.circular(AppRadii.card),
                          border: Border.all(color: AppColors.line),
                          boxShadow: AppElevation.cardShadow,
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'tags_label'.tr(),
                              style: AppTextStyles.labelSmall.copyWith(
                                color: AppColors.taupe,
                                letterSpacing: 0.8,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                            const SizedBox(height: AppSpacing.xs),
                            Wrap(
                              spacing: AppSpacing.xs,
                              runSpacing: AppSpacing.xs,
                              children: product.tags.map((tag) {
                                return Container(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 10,
                                    vertical: 5,
                                  ),
                                  decoration: BoxDecoration(
                                    color: AppColors.warmMist,
                                    borderRadius: BorderRadius.circular(
                                      AppRadii.chip,
                                    ),
                                    border: Border.all(color: AppColors.line),
                                  ),
                                  child: Text(
                                    '#$tag',
                                    style: AppTextStyles.labelSmall.copyWith(
                                      color: AppColors.taupe,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                );
                              }).toList(),
                            ),
                          ],
                        ),
                      ),
                    ],

                    const SizedBox(height: AppSpacing.md),

                    Center(
                      child: Text(
                        '${'created_on'.tr()}: ${product.createdAt.day}/${product.createdAt.month}/${product.createdAt.year}',
                        style: AppTextStyles.caption.copyWith(
                          color: AppColors.taupe,
                        ),
                      ),
                    ),

                    const SizedBox(height: AppSpacing.xxl),
                  ]),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

class _CircleHeaderButton extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final String? tooltip;

  const _CircleHeaderButton({required this.child, this.onTap, this.tooltip});

  @override
  Widget build(BuildContext context) {
    Widget button = Container(
      width: 38,
      height: 38,
      decoration: BoxDecoration(
        color: AppColors.cardSurface.withValues(alpha: 0.92),
        shape: BoxShape.circle,
        border: Border.all(color: AppColors.line),
        boxShadow: AppElevation.cardShadow,
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(19),
          onTap: onTap,
          child: Center(child: child),
        ),
      ),
    );

    if (tooltip != null) {
      return Tooltip(message: tooltip!, child: button);
    }
    return button;
  }
}
