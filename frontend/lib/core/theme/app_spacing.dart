import 'package:flutter/material.dart';

/// Craftsy "Kosa Silk" spacing system — 8pt base grid.
class AppSpacing {
  // Base spacing units
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double xl = 32.0;
  static const double xxl = 48.0;
  static const double xxxl = 64.0;

  // Semantic spacing — Kosa Silk
  static const double screenPadding = 20.0;
  static const double cardPadding = 18.0;
  static const double sectionSpacing = 28.0;
  static const double itemSpacing = 14.0;

  // Touch targets — 48dp minimum per WCAG / Material
  static const double minTouchTarget = 48.0;
  static const double minTouchTargetCompact = 40.0;

  // Icon sizes
  static const double iconSize = 24.0;
  static const double iconSizeLarge = 32.0;
  static const double iconSizeSmall = 20.0;
  static const double iconSizeXLarge = 48.0;

  // Responsive screen padding
  static double getScreenPadding(BuildContext context) {
    final w = MediaQuery.of(context).size.width;
    if (w < 360) return 14.0;
    if (w < 480) return 18.0;
    if (w < 600) return 22.0;
    if (w < 900) return 32.0;
    return 44.0;
  }

  // Responsive font-size scale
  static double getResponsiveFontScale(BuildContext context) {
    final w = MediaQuery.of(context).size.width;
    if (w < 360) return 0.88;
    if (w < 480) return 0.94;
    if (w < 600) return 1.0;
    if (w < 900) return 1.06;
    return 1.12;
  }

  // Responsive button height
  static double getButtonHeight(BuildContext context, {bool compact = false}) {
    final w = MediaQuery.of(context).size.width;
    if (compact) return w < 480 ? 38.0 : minTouchTargetCompact;
    return w < 480 ? 46.0 : minTouchTarget;
  }

  // Responsive list gap
  static double getListGap(BuildContext context) {
    final w = MediaQuery.of(context).size.width;
    if (w < 480) return 10.0;
    if (w < 600) return 14.0;
    if (w < 900) return 18.0;
    return 22.0;
  }

  AppSpacing._();
}

/// Warm rounded corners for Kosa Silk — approachable, organic feel
class AppRadii {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 12.0;
  static const double lg = 16.0;
  static const double xl = 20.0;
  static const double xxl = 24.0;
  static const double full = 999.0;

  // Semantic radii — Kosa Silk
  static const double button = 999.0; // fully rounded pill buttons
  static const double card = 16.0;
  static const double chip = 999.0; // pill chips
  static const double bottomSheet = 24.0;
  static const double dialog = 20.0;
  static const double inputField = 12.0;

  // Responsive card radius
  static double getCardRadius(BuildContext context) {
    final w = MediaQuery.of(context).size.width;
    if (w < 360) return 12.0;
    if (w < 600) return 16.0;
    return 20.0;
  }

  AppRadii._();
}

/// Elevation and shadow definitions — Kosa Silk warm-toned shadows
class AppElevation {
  static const double none = 0;
  static const double subtle = 2;
  static const double low = 4;
  static const double medium = 8;
  static const double high = 12;
  static const double highest = 16;

  /// Resting card shadow — rgba(42,31,27,0.06) shallow and tactile
  static const List<BoxShadow> cardShadow = [
    BoxShadow(
      color: Color(0x0F2A1F1B), // 0.06 opacity
      blurRadius: 12,
      offset: Offset(0, 3),
    ),
    BoxShadow(
      color: Color(0x082A1F1B), // 0.03 opacity
      blurRadius: 4,
      offset: Offset(0, 1),
    ),
  ];

  /// Lifted shadow — for open bottom sheets / hovered cards
  static const List<BoxShadow> cardShadowLifted = [
    BoxShadow(
      color: Color(0x332A1F1B), // 0.2 opacity
      blurRadius: 32,
      spreadRadius: -12,
      offset: Offset(0, 14),
    ),
    BoxShadow(
      color: Color(0x0F2A1F1B),
      blurRadius: 10,
      offset: Offset(0, 3),
    ),
  ];

  /// Button press shadow
  static const List<BoxShadow> buttonShadow = [
    BoxShadow(
      color: Color(0x332A1F1B),
      blurRadius: 12,
      offset: Offset(0, 4),
    ),
  ];

  /// Responsive version (kept for backward compat; returns cardShadow always)
  static List<BoxShadow> getCardShadow(BuildContext context) => cardShadow;

  AppElevation._();
}
