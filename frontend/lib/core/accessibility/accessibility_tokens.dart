import 'package:flutter/material.dart';

/// Centralized accessibility tokens for Craftsy V2.
///
/// These tokens ensure consistent accessibility behavior across all
/// reusable components. Do not hard-code values in individual widgets —
/// reference these tokens instead.
class AccessibilityTokens {
  // ---------------------------------------------------------------------------
  // Minimum touch targets
  // ---------------------------------------------------------------------------
  /// Minimum touch target size per WCAG 2.5.5 / Material guidelines.
  static const double minTouchTarget = 48.0;

  /// Compact minimum touch target for dense layouts.
  static const double minTouchTargetCompact = 40.0;

  /// Large touch target for primary actions.
  static const double minTouchTargetLarge = 56.0;

  // ---------------------------------------------------------------------------
  // Spacing
  // ---------------------------------------------------------------------------
  static const double spacingXs = 4.0;
  static const double spacingSm = 8.0;
  static const double spacingMd = 16.0;
  static const double spacingLg = 24.0;
  static const double spacingXl = 32.0;

  // ---------------------------------------------------------------------------
  // Corner radii
  // ---------------------------------------------------------------------------
  static const double radiusSm = 8.0;
  static const double radiusMd = 12.0;
  static const double radiusLg = 16.0;
  static const double radiusXl = 20.0;
  static const double radiusFull = 999.0;

  // ---------------------------------------------------------------------------
  // Elevation
  // ---------------------------------------------------------------------------
  static const double elevationNone = 0;
  static const double elevationSubtle = 2;
  static const double elevationLow = 4;
  static const double elevationMedium = 8;
  static const double elevationHigh = 12;

  // ---------------------------------------------------------------------------
  // Semantic colors (reference AppColors)
  // ---------------------------------------------------------------------------
  static const Color primary = Color(0xFF2D3A8C); // indigo
  static const Color primaryDark = Color(0xFF1A1A2E);
  static const Color primaryLight = Color(0xFFE8EAF6);

  static const Color secondary = Color(0xFFE8912D); // amber
  static const Color secondaryDark = Color(0xFFC75B39);
  static const Color secondaryLight = Color(0xFFFFF3E0);

  static const Color success = Color(0xFF00696E); // teal
  static const Color successLight = Color(0xFFE0F2F1);

  static const Color warning = Color(0xFFE8912D); // amber
  static const Color warningLight = Color(0xFFFFF3E0);

  static const Color error = Color(0xFFD84343); // coral
  static const Color errorLight = Color(0xFFFFEBEE);

  static const Color offline = Color(0xFF545468); // inkSoft
  static const Color offlineLight = Color(0xFFE8E8F0);

  // ---------------------------------------------------------------------------
  // Typography scale (reference AppTextStyles)
  // ---------------------------------------------------------------------------
  static const double fontSizeCaption = 12.0;
  static const double fontSizeBody = 15.0;
  static const double fontSizeBodyLarge = 17.0;
  static const double fontSizeLabel = 14.0;
  static const double fontSizeLabelLarge = 16.0;
  static const double fontSizeHeadline = 20.0;
  static const double fontSizeHeadlineLarge = 22.0;
  static const double fontSizeDisplay = 28.0;

  // ---------------------------------------------------------------------------
  // Animation durations
  // ---------------------------------------------------------------------------
  static const Duration animationFast = Duration(milliseconds: 150);
  static const Duration animationNormal = Duration(milliseconds: 250);
  static const Duration animationSlow = Duration(milliseconds: 400);

  // ---------------------------------------------------------------------------
  // Voice state indicators
  // ---------------------------------------------------------------------------
  static const double voiceIndicatorSize = 24.0;
  static const double voiceIndicatorSizeLarge = 32.0;

  // ---------------------------------------------------------------------------
  // Progress indicator
  // ---------------------------------------------------------------------------
  static const double progressBarHeight = 4.0;
  static const double progressBarWidth = 200.0;

  AccessibilityTokens._();
}
