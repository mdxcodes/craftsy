import 'package:flutter/material.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';
import 'speak_button.dart';

/// Large action card for low-literacy flows.
///
/// Icon/illustration + very short label + optional spoken description.
/// Large touch target, usable in low-literacy flows.
class LargeActionCard extends StatefulWidget {
  final IconData icon;
  final String label;
  final String? spokenDescription;
  final VoidCallback? onTap;
  final Color? backgroundColor;
  final Color? iconColor;
  final bool isEnabled;

  const LargeActionCard({
    super.key,
    required this.icon,
    required this.label,
    this.spokenDescription,
    this.onTap,
    this.backgroundColor,
    this.iconColor,
    this.isEnabled = true,
  });

  @override
  State<LargeActionCard> createState() => _LargeActionCardState();
}

class _LargeActionCardState extends State<LargeActionCard> {
  @override
  Widget build(BuildContext context) {
    final effectiveBg = widget.backgroundColor ?? AppColors.cardSurface;
    final effectiveIconColor = widget.iconColor ?? AppColors.indigo;

    return Semantics(
      button: true,
      label: widget.label,
      hint: widget.spokenDescription,
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: widget.isEnabled ? widget.onTap : null,
          borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
          child: Container(
            constraints: const BoxConstraints(
              minHeight: AccessibilityTokens.minTouchTargetLarge * 2,
              minWidth: AccessibilityTokens.minTouchTargetLarge * 2,
            ),
            padding: const EdgeInsets.all(AccessibilityTokens.spacingLg),
            decoration: BoxDecoration(
              color: widget.isEnabled ? effectiveBg : AppColors.parchmentDeep,
              borderRadius: BorderRadius.circular(AccessibilityTokens.radiusLg),
              border: Border.all(
                color: widget.isEnabled
                    ? AppColors.indigo.withValues(alpha: 0.2)
                    : AppColors.line,
                width: 1.5,
              ),
              boxShadow: [
                BoxShadow(
                  color: AppColors.shadow,
                  blurRadius: 8,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Icon
                Container(
                  width: 56,
                  height: 56,
                  decoration: BoxDecoration(
                    color: widget.isEnabled
                        ? effectiveIconColor.withValues(alpha: 0.12)
                        : AppColors.parchmentDeep,
                    borderRadius: BorderRadius.circular(
                      AccessibilityTokens.radiusMd,
                    ),
                  ),
                  child: Icon(
                    widget.icon,
                    size: 32,
                    color: widget.isEnabled
                        ? effectiveIconColor
                        : AppColors.inkFaint,
                  ),
                ),
                const SizedBox(height: AccessibilityTokens.spacingMd),
                // Label
                Text(
                  widget.label,
                  style: AppTextStyles.labelLarge.copyWith(
                    color: widget.isEnabled
                        ? AppColors.textPrimary
                        : AppColors.inkFaint,
                    fontWeight: FontWeight.w700,
                  ),
                  textAlign: TextAlign.center,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                // Speak button
                if (widget.spokenDescription != null)
                  Padding(
                    padding: const EdgeInsets.only(
                      top: AccessibilityTokens.spacingSm,
                    ),
                    child: SpeakButton(
                      text: widget.spokenDescription!,
                      compact: true,
                      color: effectiveIconColor,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
