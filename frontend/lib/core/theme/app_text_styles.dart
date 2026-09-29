import 'package:flutter/material.dart';
import 'app_colors.dart';

/// Craftsy "Kosa Silk" typography tokens.
///
/// Display font : Fraunces (variable OTF) — serif, warm, expressive.
///   Used sparingly for hero text and app branding only.
///
/// Body/UI font : Manrope (variable TTF) — geometric sans, clean, legible.
///   All body, label, caption, and headline styles.
///
/// Both fonts are bundled as assets — safe for offline/zero-connectivity use.
class AppTextStyles {
  // ---------------------------------------------------------------------------
  // Fraunces — reserved for display/hero only
  // ---------------------------------------------------------------------------
  static const _fraunces = 'Fraunces';

  static List<FontVariation> _opsz(double opsz) => [
    FontVariation('opsz', opsz),
  ];

  static TextStyle displayLarge = TextStyle(
    fontFamily: _fraunces,
    fontVariations: _opsz(36),
    fontSize: 34,
    fontWeight: FontWeight.w700,
    height: 1.15,
    color: AppColors.textPrimary,
    letterSpacing: -0.5,
  );

  static TextStyle displayMedium = TextStyle(
    fontFamily: _fraunces,
    fontVariations: _opsz(36),
    fontSize: 26,
    fontWeight: FontWeight.w700,
    height: 1.2,
    color: AppColors.textPrimary,
    letterSpacing: -0.3,
  );

  static TextStyle displaySmall = TextStyle(
    fontFamily: _fraunces,
    fontVariations: _opsz(36),
    fontSize: 22,
    fontWeight: FontWeight.w600,
    height: 1.25,
    color: AppColors.textPrimary,
  );

  // ---------------------------------------------------------------------------
  // Headlines — Manrope, bold, for section headers
  // ---------------------------------------------------------------------------
  static const _manrope = 'Manrope';

  static TextStyle headlineLarge = TextStyle(
    fontFamily: _manrope,
    fontSize: 22,
    fontWeight: FontWeight.w700,
    height: 1.3,
    color: AppColors.textPrimary,
    letterSpacing: -0.2,
  );

  static TextStyle headlineMedium = TextStyle(
    fontFamily: _manrope,
    fontSize: 18,
    fontWeight: FontWeight.w700,
    height: 1.35,
    color: AppColors.textPrimary,
  );

  static TextStyle headlineSmall = TextStyle(
    fontFamily: _manrope,
    fontSize: 16,
    fontWeight: FontWeight.w600,
    height: 1.4,
    color: AppColors.textPrimary,
  );

  // ---------------------------------------------------------------------------
  // Body — Manrope
  // ---------------------------------------------------------------------------
  static const TextStyle bodyLarge = TextStyle(
    fontFamily: _manrope,
    fontSize: 16,
    fontWeight: FontWeight.w400,
    height: 1.5,
    color: AppColors.textPrimary,
  );

  static const TextStyle bodyMedium = TextStyle(
    fontFamily: _manrope,
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 1.55,
    color: AppColors.textPrimary,
  );

  static const TextStyle bodySmall = TextStyle(
    fontFamily: _manrope,
    fontSize: 12,
    fontWeight: FontWeight.w400,
    height: 1.6,
    color: AppColors.textSecondary,
  );

  // ---------------------------------------------------------------------------
  // Labels — Manrope, bold, for buttons, tabs, chips
  // ---------------------------------------------------------------------------
  static const TextStyle labelLarge = TextStyle(
    fontFamily: _manrope,
    fontSize: 15,
    fontWeight: FontWeight.w700,
    height: 1.3,
    letterSpacing: 0.2,
    color: AppColors.textPrimary,
  );

  static const TextStyle labelMedium = TextStyle(
    fontFamily: _manrope,
    fontSize: 13,
    fontWeight: FontWeight.w700,
    height: 1.35,
    letterSpacing: 0.15,
    color: AppColors.textPrimary,
  );

  static const TextStyle labelSmall = TextStyle(
    fontFamily: _manrope,
    fontSize: 11,
    fontWeight: FontWeight.w700,
    height: 1.4,
    letterSpacing: 0.1,
    color: AppColors.textSecondary,
  );

  // ---------------------------------------------------------------------------
  // Utility
  // ---------------------------------------------------------------------------
  static const TextStyle caption = TextStyle(
    fontFamily: _manrope,
    fontSize: 11,
    fontWeight: FontWeight.w500,
    height: 1.5,
    color: AppColors.textTertiary,
  );

  static const TextStyle overline = TextStyle(
    fontFamily: _manrope,
    fontSize: 10,
    fontWeight: FontWeight.w700,
    height: 1.5,
    letterSpacing: 0.8,
    color: AppColors.textSecondary,
  );

  // ---------------------------------------------------------------------------
  // Price — Manrope, bold, tabular
  // ---------------------------------------------------------------------------
  static const TextStyle priceLarge = TextStyle(
    fontFamily: _manrope,
    fontSize: 24,
    fontWeight: FontWeight.w800,
    height: 1.2,
    color: AppColors.burgundy,
    letterSpacing: -0.5,
  );

  static const TextStyle priceMedium = TextStyle(
    fontFamily: _manrope,
    fontSize: 18,
    fontWeight: FontWeight.w700,
    height: 1.25,
    color: AppColors.burgundy,
  );

  static const TextStyle priceSmall = TextStyle(
    fontFamily: _manrope,
    fontSize: 14,
    fontWeight: FontWeight.w600,
    height: 1.3,
    color: AppColors.burgundy,
  );

  AppTextStyles._();
}
