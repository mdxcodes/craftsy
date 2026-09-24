import 'package:flutter/material.dart';

/// Craftsy v4 design-token palette — "Indigo Loom"
///
/// A deep, premium indigo base with warm amber accents.
/// Completely distinct from the previous terracotta/gold/berry scheme.
///
/// Role hierarchy:
///   indigo       → every primary action button, app bar, FAB
///   amber        → every secondary/alternate-path button, highlights
///   teal         → accent only (success states, info cards)
///   coral        → accent only (warnings, error states)
class AppColors {
  // ---------------------------------------------------------------------------
  // Core palette — Indigo Loom
  // ---------------------------------------------------------------------------

  /// Primary action (deep indigo)
  static const indigo = Color(0xFF2D3A8C);
  static const indigoDark = Color(0xFF1A1A2E);
  static const indigoLight = Color(0xFFE8EAF6);

  /// Secondary action (warm amber) — drives every secondary / alternate-path button
  static const amber = Color(0xFFE8912D);
  static const amberDark = Color(0xFFC75B39);
  static const amberLight = Color(0xFFFFF3E0);

  /// Accent 1 (teal) — success states, info cards; never a button fill
  static const teal = Color(0xFF00696E);
  static const tealDark = Color(0xFF004F52);
  static const tealLight = Color(0xFFE0F2F1);

  /// Accent 2 (coral) — warnings, error states; never a button fill
  static const coral = Color(0xFFD84343);
  static const coralDark = Color(0xFFB71C1C);
  static const coralLight = Color(0xFFFFEBEE);

  // ---------------------------------------------------------------------------
  // Ink — cool near-black text
  // ---------------------------------------------------------------------------
  static const ink = Color(0xFF1A1A2E);
  static const inkSoft = Color(0xFF545468);
  static const inkFaint = Color(0xFF9E9EB0);

  // ---------------------------------------------------------------------------
  // Surfaces
  // ---------------------------------------------------------------------------
  static const parchment = Color(0xFFF5F5FA);
  static const parchmentDeep = Color(0xFFE8E8F0);
  static const cardSurface = Color(0xFFFFFFFF);

  // ---------------------------------------------------------------------------
  // Structural
  // ---------------------------------------------------------------------------
  static const dottedBorder = Color(0xFFD0D0E0);
  static const line = Color(0x241A1A2E);
  static const shadow = Color(0x141A1A2E);
  static const shadowLifted = Color(0x471A1A2E);
  static const overlay = Color(0x6B0A0A1A);

  // ---------------------------------------------------------------------------
  // Semantic convenience aliases
  // ---------------------------------------------------------------------------
  static const textPrimary = ink;
  static const textSecondary = inkSoft;
  static const textTertiary = inkFaint;
  static const textOnPrimary = Color(0xFFFFFFFF);

  static const background = parchment;
  static const surface = cardSurface;
  static const surfaceVariant = parchmentDeep;

  static const error = coral;
  static const warning = amber;
  static const border = dottedBorder;
  static const divider = line;

  // ---------------------------------------------------------------------------
  // Status badge roles
  // ---------------------------------------------------------------------------
  static const statusActionBg = indigoLight;
  static const statusActionFg = indigoDark;
  static const statusPendingBg = amberLight;
  static const statusPendingFg = amberDark;
  static const statusSuccessBg = tealLight;
  static const statusSuccessFg = teal;

  // ---------------------------------------------------------------------------
  // Legacy aliases — kept so un-migrated screens still compile.
  // Updated to point to new v4 token values.
  // ---------------------------------------------------------------------------
  static const terracotta = indigo;
  static const terracottaDark = indigoDark;
  static const terracottaLight = indigoLight;
  static const gold = amber;
  static const goldDark = amberDark;
  static const goldLight = amberLight;
  static const berry = teal;
  static const berryDark = tealDark;
  static const berryLight = tealLight;
  static const blueAccent = indigo;
  static const blueAccentDark = indigoDark;
  static const blueAccentLight = indigoLight;
  static const success = teal;
  static const successLight = tealLight;

  static const plaster = parchment;
  static const plasterDark = parchmentDeep;
  static const charcoal = ink;
  static const charcoalSoft = inkSoft;
  static const cream = cardSurface;
  static const oak = dottedBorder;
  static const mustard = amber;
  static const brick = indigoDark;
  static const aboveRange = teal;
  static const online = teal;
  static const syncing = amber;
  static const offline = inkSoft;
  static const statusLive = teal;
  static const statusPending = amber;
  static const statusDraft = inkSoft;
  static const statusSold = amber;
  static const turmeric = amber;
  static const turmericLight = amberLight;
  static const turmericDark = amberDark;
  static const forestGreen = teal;
  static const forestGreenLight = tealLight;
  static const forestGreenDark = tealDark;
  static const info = indigo;

  AppColors._();
}
