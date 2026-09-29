import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/accessibility/accessibility_tokens.dart';
import 'speak_button.dart';

/// Guided step shell — one major task per screen.
///
/// Progress indicator that is understandable visually.
/// Optional spoken guidance. Supports back/cancel.
class GuidedStepShell extends StatefulWidget {
  final int currentStep;
  final int totalSteps;
  final String title;
  final String? spokenGuidance;
  final VoidCallback? onBack;
  final VoidCallback? onCancel;
  final Widget child;
  final Widget? bottomAction;

  const GuidedStepShell({
    super.key,
    required this.currentStep,
    required this.totalSteps,
    required this.title,
    this.spokenGuidance,
    this.onBack,
    this.onCancel,
    required this.child,
    this.bottomAction,
  });

  @override
  State<GuidedStepShell> createState() => _GuidedStepShellState();
}

class _GuidedStepShellState extends State<GuidedStepShell> {
  @override
  Widget build(BuildContext context) {
    final progress = (widget.currentStep + 1) / widget.totalSteps;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: AppColors.background,
        elevation: 0,
        leading: widget.onBack != null
            ? Semantics(
                button: true,
                label: 'back'.tr(),
                child: IconButton(
                  onPressed: widget.onBack,
                  icon: const Icon(Icons.arrow_back_rounded),
                  color: AppColors.espresso,
                ),
              )
            : null,
        title: Text(widget.title, style: AppTextStyles.headlineMedium),
        centerTitle: false,
        actions: [
          if (widget.onCancel != null)
            Semantics(
              button: true,
              label: 'cancel'.tr(),
              child: IconButton(
                onPressed: widget.onCancel,
                icon: const Icon(Icons.close_rounded),
                color: AppColors.taupe,
              ),
            ),
        ],
      ),
      body: Column(
        children: [
          // Progress indicator
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AccessibilityTokens.spacingLg,
              vertical: AccessibilityTokens.spacingMd,
            ),
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'step'.tr(
                        args: [
                          '${widget.currentStep + 1}',
                          '${widget.totalSteps}',
                        ],
                      ),
                      style: AppTextStyles.labelMedium.copyWith(
                        color: AppColors.taupe,
                      ),
                    ),
                    if (widget.spokenGuidance != null)
                      SpeakButton(text: widget.spokenGuidance!, compact: true),
                  ],
                ),
                const SizedBox(height: AccessibilityTokens.spacingSm),
                // Visual progress bar
                ClipRRect(
                  borderRadius: BorderRadius.circular(
                    AccessibilityTokens.radiusFull,
                  ),
                  child: LinearProgressIndicator(
                    value: progress,
                    minHeight: AccessibilityTokens.progressBarHeight,
                    backgroundColor: AppColors.warmMist,
                    valueColor: AlwaysStoppedAnimation<Color>(AppColors.burgundy),
                  ),
                ),
              ],
            ),
          ),
          // Content
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(AccessibilityTokens.spacingLg),
              child: widget.child,
            ),
          ),
          // Bottom action
          if (widget.bottomAction != null)
            Container(
              padding: const EdgeInsets.all(AccessibilityTokens.spacingLg),
              decoration: BoxDecoration(
                color: AppColors.cardSurface,
                boxShadow: [
                  BoxShadow(
                    color: AppColors.warmShadow,
                    blurRadius: 8,
                    offset: const Offset(0, -2),
                  ),
                ],
              ),
              child: widget.bottomAction!,
            ),
        ],
      ),
    );
  }
}
