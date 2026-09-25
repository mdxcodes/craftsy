import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';

import '../../../core/services/commerce_service.dart';
import 'cart_screen.dart' show cartProvider;
import '../../../core/theme/app_colors.dart';
// commerceService usages below go through commerceServiceProvider for testability
import '../../../core/theme/app_spacing.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';

final addressesProvider = FutureProvider<List<Address>>((ref) {
  return ref.watch(commerceServiceProvider).getAddresses();
});

class CheckoutScreen extends ConsumerStatefulWidget {
  const CheckoutScreen({super.key});

  @override
  ConsumerState<CheckoutScreen> createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends ConsumerState<CheckoutScreen> {
  String? _selectedAddressId;
  bool _placing = false;
  String? _errorMessage;

  @override
  Widget build(BuildContext context) {
    final addressesAsync = ref.watch(addressesProvider);
    final cartAsync = ref.watch(cartProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text('checkout_title'.tr()),
      ),
      body: SafeArea(
        child: addressesAsync.when(
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (error, _) => Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text('checkout_load_failed'.tr()),
                const SizedBox(height: AccessibilityTokens.spacingMd),
                TextButton.icon(
                  onPressed: () => ref.invalidate(addressesProvider),
                  icon: const Icon(Icons.refresh),
                  label: Text('action_retry'.tr()),
                ),
              ],
            ),
          ),
          data: (addresses) {
            final cart = cartAsync.valueOrNull;
            final hasItems = cart != null && cart.items.isNotEmpty;

            return Column(
              children: [
                Expanded(
                  child: ListView(
                    padding: EdgeInsets.all(AppSpacing.screenPadding),
                    children: [
                      // ── 1. Delivery address ──────────────────────────
                      Text(
                        'checkout_delivery_address'.tr(),
                        style: AppTextStyles.headlineMedium,
                      ),
                      const SizedBox(height: AppSpacing.md),
                      if (addresses.isEmpty)
                        _EmptyAddressCard(onAdd: () => _showAddressForm())
                      else ...[
                        ...addresses.map((address) => _AddressCard(
                              address: address,
                              selected:
                                  _selectedAddressId == address.id ||
                                      (addresses.length == 1 &&
                                          _selectedAddressId == null),
                              onTap: () =>
                                  setState(() => _selectedAddressId = address.id),
                              onEdit: () => _showAddressForm(address: address),
                            )),
                        TextButton.icon(
                          onPressed: () => _showAddressForm(),
                          icon: const Icon(Icons.add),
                          label: Text('address_add_new'.tr()),
                        ),
                      ],

                      const SizedBox(height: AppSpacing.lg),

                      // ── 2. Payment method — honest COD-only ─────────
                      Text(
                        'checkout_payment_method'.tr(),
                        style: AppTextStyles.headlineMedium,
                      ),
                      const SizedBox(height: AppSpacing.md),
                      _PaymentMethodCard(
                        selected: true,
                        onTap: () {},
                      ),
                      const SizedBox(height: AppSpacing.md),
                      // Honest disclosure: online payment is not integrated
                      Container(
                        padding: EdgeInsets.all(AppSpacing.cardPadding),
                        decoration: BoxDecoration(
                          color: AppColors.amberLight,
                          borderRadius: BorderRadius.circular(
                              AccessibilityTokens.radiusMd),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.info_outline,
                                color: AppColors.amberDark),
                            const SizedBox(width: AppSpacing.sm),
                            Expanded(
                              child: Text(
                                'checkout_upi_coming_later'.tr(),
                                style: AppTextStyles.labelMedium.copyWith(
                                  color: AppColors.amberDark,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: AppSpacing.lg),

                      // ── 3. Order summary (display-only totals) ───────
                      Text(
                        'checkout_order_summary'.tr(),
                        style: AppTextStyles.headlineMedium,
                      ),
                      const SizedBox(height: AppSpacing.md),
                      if (!hasItems)
                        Text('checkout_cart_empty'.tr())
                      else ...[
                        ...cart.items.map(
                          (item) => Padding(
                            padding:
                                const EdgeInsets.only(bottom: AppSpacing.xs),
                            child: Row(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Expanded(
                                  child: Text(
                                    '${item.title}  ×${item.quantity}',
                                    style: AppTextStyles.bodyMedium,
                                  ),
                                ),
                                Text(
                                  '₹${item.lineTotal.toStringAsFixed(0)}',
                                  style: AppTextStyles.bodyMedium,
                                ),
                              ],
                            ),
                          ),
                        ),
                        Divider(color: AppColors.parchmentDeep),
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
                      ],
                    ],
                  ),
                ),

                // ── Place order ──────────────────────────────────────
                Container(
                  padding: EdgeInsets.all(AppSpacing.screenPadding),
                  decoration: BoxDecoration(
                    color: AppColors.cardSurface,
                    border:
                        Border(top: BorderSide(color: AppColors.parchmentDeep)),
                  ),
                  child: SafeArea(
                    top: false,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        if (_errorMessage != null) ...[
                          Text(
                            _errorMessage!,
                            style: AppTextStyles.labelMedium
                                .copyWith(color: AppColors.coral),
                          ),
                          const SizedBox(height: AppSpacing.sm),
                        ],
                        Semantics(
                          button: true,
                          label: 'checkout_place_order'.tr(),
                          child: FilledButton(
                            onPressed: _placing || !hasItems
                                ? null
                                : () => _placeOrder(addresses),
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
                            child: _placing
                                ? const SizedBox(
                                    width: 22,
                                    height: 22,
                                    child: CircularProgressIndicator(
                                        strokeWidth: 2),
                                  )
                                : Text('checkout_place_order'.tr()),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }

  Future<void> _placeOrder(List<Address> addresses) async {
    final effectiveAddressId = _selectedAddressId ??
        (addresses.length == 1 ? addresses.first.id : null);

    if (effectiveAddressId == null) {
      setState(() =>
          _errorMessage = 'checkout_select_address_error'.tr());
      return;
    }

    setState(() {
      _placing = true;
      _errorMessage = null;
    });

    try {
      final svc = ref.read(commerceServiceProvider);
      final cart = await svc.getCart();
      final order = await svc.checkout(
        addressId: effectiveAddressId,
        items: cart.items,
        paymentMethod: 'cod',
      );
      if (!mounted) return;
      // Clear local cart cache; next view comes from the server
      ref.invalidate(cartProvider);
      ref.invalidate(addressesProvider);
      context.pushReplacement('/order-confirmation', extra: order);
    } on CommerceApiException catch (e) {
      if (!mounted) return;
      setState(() {
        _placing = false;
        _errorMessage = switch (e.statusCode) {
          400 => e.message, // server detail (stock/product/address problems)
          401 => 'cart_login_required'.tr(),
          409 => 'cart_stock_limit_generic'.tr(),
          _ => 'checkout_failed'.tr(),
        };
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _placing = false;
        _errorMessage = 'checkout_failed'.tr();
      });
    }
  }

  void _showAddressForm({Address? address}) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) => _AddressFormSheet(
        address: address,
        onSaved: () => ref.invalidate(addressesProvider),
      ),
    );
  }
}

// ── Address cards ────────────────────────────────────────────────────────────

class _EmptyAddressCard extends StatelessWidget {
  final VoidCallback onAdd;

  const _EmptyAddressCard({required this.onAdd});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        border: Border.all(
            color: AppColors.dottedBorder,
            style: BorderStyle.solid,
            width: 1.5),
        borderRadius:
            BorderRadius.circular(AccessibilityTokens.radiusLg),
      ),
      child: Column(
        children: [
          Text(
            'address_none_yet'.tr(),
            style: AppTextStyles.bodyMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: AppSpacing.md),
          FilledButton.icon(
            onPressed: onAdd,
            style: FilledButton.styleFrom(
              backgroundColor: AppColors.amber,
              foregroundColor: AppColors.indigoDark,
            ),
            icon: const Icon(Icons.add_location_alt_outlined),
            label: Text('address_add_new'.tr()),
          ),
        ],
      ),
    );
  }
}

class _AddressCard extends StatelessWidget {
  final Address address;
  final bool selected;
  final VoidCallback onTap;
  final VoidCallback onEdit;

  const _AddressCard({
    required this.address,
    required this.selected,
    required this.onTap,
    required this.onEdit,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(bottom: AppSpacing.md),
        padding: EdgeInsets.all(AppSpacing.cardPadding),
        decoration: BoxDecoration(
          color: selected
              ? AppColors.indigoLight
              : AppColors.cardSurface,
          borderRadius:
              BorderRadius.circular(AccessibilityTokens.radiusLg),
          border: Border.all(
            color: selected ? AppColors.indigo : AppColors.parchmentDeep,
            width: selected ? 2 : 1,
          ),
        ),
        child: Row(
          children: [
            Icon(
              selected
                  ? Icons.radio_button_checked
                  : Icons.radio_button_unchecked,
              color: selected ? AppColors.indigo : AppColors.textSecondary,
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Flexible(
                        child: Text(
                          '${address.name} · ${address.phone}',
                          style: AppTextStyles.labelLarge,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      if (address.isDefault) ...[
                        const SizedBox(width: AppSpacing.sm),
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 8, vertical: 2),
                          decoration: BoxDecoration(
                            color: AppColors.tealLight,
                            borderRadius: BorderRadius.circular(
                                AccessibilityTokens.radiusFull),
                          ),
                          child: Text(
                            'address_default'.tr(),
                            style: AppTextStyles.labelSmall.copyWith(
                              color: AppColors.teal,
                            ),
                          ),
                        ),
                      ],
                    ],
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    address.oneLine,
                    style: AppTextStyles.labelMedium.copyWith(
                      color: AppColors.textSecondary,
                    ),
                  ),
                ],
              ),
            ),
            IconButton(
              icon: const Icon(Icons.edit_outlined),
              tooltip: 'action_edit'.tr(),
              onPressed: onEdit,
            ),
          ],
        ),
      ),
    );
  }
}

// ── Payment method ───────────────────────────────────────────────────────────

class _PaymentMethodCard extends StatelessWidget {
  final bool selected;
  final VoidCallback onTap;

  const _PaymentMethodCard({required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(AppSpacing.cardPadding),
      decoration: BoxDecoration(
        color: selected ? AppColors.indigoLight : AppColors.cardSurface,
        borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
        border: Border.all(
          color: selected ? AppColors.indigo : AppColors.parchmentDeep,
          width: selected ? 2 : 1,
        ),
      ),
      child: Row(
        children: [
          Icon(
            selected
                ? Icons.radio_button_checked
                : Icons.radio_button_unchecked,
            color: selected ? AppColors.indigo : AppColors.textSecondary,
          ),
          const SizedBox(width: AppSpacing.md),
          const Icon(Icons.payments_outlined),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'checkout_cod'.tr(),
                  style: AppTextStyles.labelLarge,
                ),
                Text(
                  'checkout_cod_desc'.tr(),
                  style: AppTextStyles.labelSmall.copyWith(
                    color: AppColors.textSecondary,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ── Address form bottom sheet ────────────────────────────────────────────────

class _AddressFormSheet extends ConsumerStatefulWidget {
  final Address? address;
  final VoidCallback onSaved;

  const _AddressFormSheet({this.address, required this.onSaved});

  @override
  ConsumerState<_AddressFormSheet> createState() => _AddressFormSheetState();
}

class _AddressFormSheetState extends ConsumerState<_AddressFormSheet> {
  TextEditingController? _name;
  TextEditingController? _phone;
  TextEditingController? _line1;
  TextEditingController? _line2;
  TextEditingController? _city;
  TextEditingController? _state;
  TextEditingController? _pincode;
  bool _isDefault = false;
  bool _saving = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _name = TextEditingController(text: widget.address?.name ?? '');
    _phone = TextEditingController(text: widget.address?.phone ?? '');
    _line1 = TextEditingController(text: widget.address?.line1 ?? '');
    _line2 = TextEditingController(text: widget.address?.line2 ?? '');
    _city = TextEditingController(text: widget.address?.city ?? '');
    _state = TextEditingController(text: widget.address?.state ?? '');
    _pincode = TextEditingController(text: widget.address?.pincode ?? '');
    _isDefault = widget.address?.isDefault ?? false;
  }

  TextEditingController get _nameC => _name!;
  TextEditingController get _phoneC => _phone!;
  TextEditingController get _line1C => _line1!;
  TextEditingController get _line2C => _line2!;
  TextEditingController get _cityC => _city!;
  TextEditingController get _stateC => _state!;
  TextEditingController get _pincodeC => _pincode!;

  @override
  void dispose() {
    _name?.dispose();
    _phone?.dispose();
    _line1?.dispose();
    _line2?.dispose();
    _city?.dispose();
    _state?.dispose();
    _pincode?.dispose();
    super.dispose();
  }

  bool get _formValid =>
      _nameC.text.trim().isNotEmpty &&
      _phoneC.text.trim().length >= 10 &&
      _line1C.text.trim().isNotEmpty &&
      _cityC.text.trim().isNotEmpty &&
      _stateC.text.trim().isNotEmpty &&
      _pincodeC.text.trim().length == 6;

  Future<void> _save() async {
    if (!_formValid) {
      setState(() => _error = 'address_form_invalid'.tr());
      return;
    }
    setState(() {
      _saving = true;
      _error = null;
    });

    final newAddress = Address(
      id: widget.address?.id ?? '',
      name: _nameC.text.trim(),
      phone: _phoneC.text.trim(),
      line1: _line1C.text.trim(),
      line2: _line2C.text.trim(),
      city: _cityC.text.trim(),
      state: _stateC.text.trim(),
      pincode: _pincodeC.text.trim(),
      isDefault: _isDefault,
    );

    try {
      final svc = ref.read(commerceServiceProvider);
      if (widget.address == null) {
        await svc.createAddress(newAddress);
      } else {
        await svc.updateAddress(widget.address!.id, {
          'name': newAddress.name,
          'phone': newAddress.phone,
          'line1': newAddress.line1,
          'line2': newAddress.line2,
          'city': newAddress.city,
          'state': newAddress.state,
          'pincode': newAddress.pincode,
          'is_default': newAddress.isDefault,
        });
      }
      widget.onSaved();
      if (mounted) Navigator.pop(context);
    } catch (_) {
      if (mounted) {
        setState(() {
          _saving = false;
          _error = 'address_save_failed'.tr();
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom,
      ),
      child: SingleChildScrollView(
        padding: EdgeInsets.all(AppSpacing.screenPadding),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              widget.address == null ? 'address_add_new'.tr() : 'address_edit'.tr(),
              style: AppTextStyles.headlineMedium,
            ),
            const SizedBox(height: AppSpacing.lg),
            _AddressField(
                controller: _nameC, label: 'address_name'.tr(), keyboardType: TextInputType.name),
            _AddressField(
                controller: _phoneC,
                label: 'address_phone'.tr(),
                keyboardType: TextInputType.phone),
            _AddressField(
                controller: _line1C, label: 'address_line1'.tr()),
            _AddressField(
                controller: _line2C, label: 'address_line2'.tr(), required: false),
            _AddressField(
                controller: _cityC, label: 'address_city'.tr()),
            _AddressField(
                controller: _stateC, label: 'address_state'.tr()),
            _AddressField(
                controller: _pincodeC,
                label: 'address_pincode'.tr(),
                keyboardType: TextInputType.number,
                maxLength: 6),
            SwitchListTile(
              value: _isDefault,
              onChanged: (v) => setState(() => _isDefault = v),
              title: Text('address_set_default'.tr()),
              contentPadding: EdgeInsets.zero,
            ),
            if (_error != null)
              Text(_error!, style: const TextStyle(color: AppColors.coral)),
            const SizedBox(height: AppSpacing.md),
            FilledButton(
              onPressed: _saving ? null : _save,
              style: FilledButton.styleFrom(
                backgroundColor: AppColors.indigo,
                foregroundColor: AppColors.textOnPrimary,
                minimumSize: const Size.fromHeight(
                    AccessibilityTokens.minTouchTarget),
                shape: RoundedRectangleBorder(
                  borderRadius:
                      BorderRadius.circular(AccessibilityTokens.radiusFull),
                ),
              ),
              child: _saving
                  ? const SizedBox(
                      width: 22,
                      height: 22,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : Text('action_save'.tr()),
            ),
            const SizedBox(height: AppSpacing.lg),
          ],
        ),
      ),
    );
  }
}

class _AddressField extends StatelessWidget {
  final TextEditingController controller;
  final String label;
  final TextInputType? keyboardType;
  final int? maxLength;
  final bool required;

  const _AddressField({
    required this.controller,
    required this.label,
    this.keyboardType,
    this.maxLength,
    this.required = true,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: AppSpacing.md),
      child: TextField(
        controller: controller,
        keyboardType: keyboardType,
        maxLength: maxLength,
        onChanged: (_) {},
        decoration: InputDecoration(
          labelText:
              required ? label : '$label (${('action_optional'.tr())})',
          border: OutlineInputBorder(
            borderRadius:
                BorderRadius.circular(AccessibilityTokens.radiusMd),
          ),
        ),
      ),
    );
  }
}
