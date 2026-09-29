import 'package:flutter/material.dart';

/// Craftsy "Kosa Silk" design-token palette — warm, handcrafted, regal.
///
/// Inspired by Indian textile traditions: deep burgundy, warm gold,
/// natural sage, and cream backgrounds. Distinct from the previous
/// Indigo Loom scheme.
///
/// Role hierarchy:
///   burgundy       → every primary action button, app bar, FAB
///   gold           → every secondary/alternate-path button, highlights
///   sage           → accent only (success states, info cards)
///   sienna         → accent only (warnings, error states)
class AppColors {
  // ---------------------------------------------------------------------------
  // Core palette — Kosa Silk
  // ---------------------------------------------------------------------------

  /// Primary action (deep burgundy/wine)
  static const burgundy = Color(0xFF7B2D3E);
  static const burgundyDark = Color(0xFF5A1F2D);
  static const burgundyLight = Color(0xFFF5E6EB);

  /// Secondary action (warm gold/ochre) — drives every secondary / alternate-path button
  static const gold = Color(0xFFC9973E);
  static const goldDark = Color(0xFFA67C2E);
  static const goldLight = Color(0xFFFFF3E0);

  /// Accent 1 (sage) — success states, info cards; never a button fill
  static const sage = Color(0xFF6B8E5A);
  static const sageDark = Color(0xFF4D6B3A);
  static const sageLight = Color(0xFFE8F0E4);

  /// Accent 2 (sienna) — warnings, error states; never a button fill
  static const sienna = Color(0xFFC04F3A);
  static const siennaDark = Color(0xFF9E3B2A);
  static const siennaLight = Color(0xFFFFEBEE);

  // ---------------------------------------------------------------------------
  // Neutrals — warm cream / espresso / taupe family
  // ---------------------------------------------------------------------------

  /// Backgrounds
  static const cream = Color(0xFFFAF7F2);
  static const linen = Color(0xFFF5F0E8);
  static const cardSurface = Color(0xFFFFFFFF);

  /// Text
  static const espresso = Color(0xFF2A1F1B);
  static const warmGray = Color(0xFF6B635E);
  static const taupe = Color(0xFF9E968F);

  /// Structural
  static const warmStone = Color(0xFFD9D2C7);
  static const warmMist = Color(0xFFE8E2D9);
  static const warmShadow = Color(0x1A2A1F1B);

  // ---------------------------------------------------------------------------
  // Semantic convenience aliases
  // ---------------------------------------------------------------------------
  static const textPrimary = espresso;
  static const textSecondary = warmGray;
  static const textTertiary = taupe;
  static const textOnPrimary = Color(0xFFFFFFFF);

  static const background = cream;
  static const surface = cardSurface;
  static const surfaceVariant = linen;

  static const error = sienna;
  static const warning = gold;
  static const border = warmStone;
  static const divider = warmMist;

  static const success = sage;
  static const successLight = sageLight;

  // ---------------------------------------------------------------------------
  // Status badge roles
  // ---------------------------------------------------------------------------
  static const statusActionBg = goldLight;
  static const statusActionFg = goldDark;
  static const statusPendingBg = linen;
  static const statusPendingFg = warmGray;
  static const statusSuccessBg = sageLight;
  static const statusSuccessFg = sage;

  // ---------------------------------------------------------------------------
  // Legacy aliases — kept so un-migrated screens still compile.
  // Updated to point to new Kosa Silk token values.
  // ---------------------------------------------------------------------------
  static const indigo = burgundy;
  static const indigoDark = burgundyDark;
  static const indigoLight = burgundyLight;
  static const amber = gold;
  static const amberDark = goldDark;
  static const amberLight = goldLight;
  static const teal = sage;
  static const tealDark = sageDark;
  static const tealLight = sageLight;
  static const coral = sienna;
  static const coralDark = siennaDark;
  static const coralLight = siennaLight;
  static const ink = espresso;
  static const inkSoft = warmGray;
  static const inkFaint = taupe;
  static const parchment = cream;
  static const parchmentDeep = linen;
  static const dottedBorder = warmStone;
  static const line = warmMist;
  static const shadow = warmShadow;
  static const shadowLifted = Color(0x332A1F1B);
  static const overlay = Color(0x6B0A0A1A);
  static const terracotta = burgundy;
  static const terracottaDark = burgundyDark;
  static const terracottaLight = burgundyLight;
  static const blueAccent = burgundy;
  static const blueAccentDark = burgundyDark;
  static const blueAccentLight = burgundyLight;
  static const plaster = cream;
  static const plasterDark = linen;
  static const oak = warmStone;
  static const mustard = gold;
  static const brick = burgundyDark;
  static const aboveRange = sage;
  static const online = sage;
  static const syncing = gold;
  static const offline = warmGray;
  static const statusLive = sage;
  static const statusPending = gold;
  static const statusDraft = warmGray;
  static const statusSold = gold;
  static const turmeric = gold;
  static const turmericLight = goldLight;
  static const turmericDark = goldDark;
  static const forestGreen = sage;
  static const forestGreenLight = sageLight;
  static const forestGreenDark = sageDark;
  static const info = burgundy;

  AppColors._();
}
