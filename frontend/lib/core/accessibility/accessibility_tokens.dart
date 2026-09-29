import 'package:flutter/material.dart';

/// Centralized accessibility tokens for Craftsy "Kosa Silk".
///
/// These tokens ensure consistent accessibility behavior across all
/// reusable components. Do not hard-code values in individual widgets —
/// reference these tokens instead.
class AccessibilityTokens {
  // ---------------------------------------------------------------------------
  // Minimum touch targets
  // ---------------------------------------------------------------------------
  static const double minTouchTarget = 48.0;

  static const double minTouchTargetCompact = 40.0;

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
  static const Color primary = Color(0xFF7B2D3E);
  static const Color primaryDark = Color(0xFF5A1F2D);
  static const Color primaryLight = Color(0xFFF5E6EB);

  static const Color secondary = Color(0xFFC9973E);
  static const Color secondaryDark = Color(0xFFA67C2E);
  static const Color secondaryLight = Color(0xFFFFF3E0);

  static const Color success = Color(0xFF6B8E5A);
  static const Color successLight = Color(0xFFE8F0E4);

  static const Color warning = Color(0xFFC9973E);
  static const Color warningLight = Color(0xFFFFF3E0);

  static const Color error = Color(0xFFC04F3A);
  static const Color errorLight = Color(0xFFFFEBEE);

  static const Color offline = Color(0xFF6B635E);
  static const Color offlineLight = Color(0xFFF5F0E8);

  // ---------------------------------------------------------------------------
  // Typography scale (reference AppTextStyles)
  // ---------------------------------------------------------------------------
  static const double fontSizeCaption = 11.0;
  static const double fontSizeBody = 14.0;
  static const double fontSizeBodyLarge = 16.0;
  static const double fontSizeLabel = 13.0;
  static const double fontSizeLabelLarge = 15.0;
  static const double fontSizeHeadline = 18.0;
  static const double fontSizeHeadlineLarge = 22.0;
  static const double fontSizeDisplay = 26.0;

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
