import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:go_router/go_router.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../../core/providers/app_providers.dart';
import '../../auth/providers/auth_provider.dart';
import '../../../core/router/app_route_constants.dart';
import '../../../core/services/app_sound_service.dart';
import '../../catalogue/screens/catalogue_screen.dart';
import '../screens/home_v2_screen.dart';
import '../../orders/screens/my_orders_screen.dart';
import '../../add_product/screens/add_product_flow_screen.dart';
import '../../profile/screens/profile_screen.dart';
import '../../chatbot/widgets/craftmitra_fab.dart';

final homeTabIndexProvider = StateProvider<int>((ref) => 0);

class HomeShell extends ConsumerStatefulWidget {
  const HomeShell({super.key});

  @override
  ConsumerState<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends ConsumerState<HomeShell> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkAndLaunchTutorialIfFirstTime();
    });
  }

  Future<void> _checkAndLaunchTutorialIfFirstTime() async {
    if (!mounted) return;
    final currentTab = ref.read(homeTabIndexProvider);
    if (currentTab != 0) return;

    final authState = ref.read(authStateProvider);
    final userId =
        authState.userId ?? authState.phoneNumber ?? 'default_artisan';

    final shouldLaunch = await ref
        .read(listingTutorialProvider.notifier)
        .checkAndMarkTutorialSeen(userId);

    if (shouldLaunch && mounted) {
      context.pushNamed(AppRouteConstants.listingTutorial);
    }
  }

  Future<void> _handleTabTap(int index) async {
    AppSoundService.instance.playTapSound();
    if (index == 3) {
      final draft = ref.read(addProductFlowProvider);
      if (draft.hasExistingDraft && !draft.resumePromptHandled) {
        final shouldResume = await showDialog<bool>(
          context: context,
          barrierDismissible: false,
          builder: (context) => AlertDialog(
            title: Text('resume_draft_title'.tr(context: context)),
            content: Text('resume_draft_msg'.tr(context: context)),
            actions: [
              TextButton(
                onPressed: () => Navigator.of(context).pop(false),
                child: Text('start_fresh_btn'.tr(context: context)),
              ),
              FilledButton(
                onPressed: () => Navigator.of(context).pop(true),
                child: Text('resume_btn'.tr(context: context)),
              ),
            ],
          ),
        );

        if (shouldResume == true) {
          ref.read(addProductFlowProvider.notifier).resumeExistingDraft();
        } else {
          ref.read(addProductFlowProvider.notifier).discardPreviousDraft();
        }
      }
    }

    ref.read(homeTabIndexProvider.notifier).state = index;
    if (index == 0) {
      _checkAndLaunchTutorialIfFirstTime();
    }
  }

  @override
  Widget build(BuildContext context) {
    final _ = Localizations.maybeLocaleOf(context);
    final _ = ref.watch(userProfileProvider).preferredLanguage;

    final currentIndex = ref.watch(homeTabIndexProvider);

    final screens = [
      const HomeV2Screen(),
      const CatalogueScreen(),
      const MyOrdersScreen(),
      const AddProductFlowScreen(),
      const ProfileScreen(),
    ];

    return Scaffold(
      resizeToAvoidBottomInset: false,
      body: AnimatedSwitcher(
        duration: const Duration(milliseconds: 200),
        switchInCurve: Curves.easeOut,
        switchOutCurve: Curves.easeIn,
        child: IndexedStack(
          key: ValueKey<int>(currentIndex),
          index: currentIndex,
          children: screens,
        ),
      ),
      floatingActionButton: const CraftMitraFab(),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: AppColors.cardSurface,
          border: Border(top: BorderSide(color: AppColors.warmMist, width: 1)),
        ),
        child: SafeArea(
          top: false,
          minimum: const EdgeInsets.only(bottom: 6),
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 6),
              child: Row(
                children: [
                  Expanded(
                    child: _NavItem(
                      icon: Icons.home_outlined,
                      label: 'home_tab'.tr(context: context),
                      isActive: currentIndex == 0,
                      onTap: () => _handleTabTap(0),
                    ),
                  ),
                  Expanded(
                    child: _NavItem(
                      icon: Icons.grid_view_outlined,
                      label: 'tab_catalogue'.tr(context: context),
                      isActive: currentIndex == 1,
                      onTap: () => _handleTabTap(1),
                    ),
                  ),
                  Expanded(
                    child: _NavItem(
                      icon: Icons.receipt_long_outlined,
                      label: 'tab_my_orders'.tr(context: context),
                      isActive: currentIndex == 2,
                      onTap: () => _handleTabTap(2),
                    ),
                  ),
                  Expanded(
                    child: _NavItem(
                      icon: Icons.add_photo_alternate_outlined,
                      label: 'tab_add_product'.tr(context: context),
                      isActive: currentIndex == 3,
                      onTap: () => _handleTabTap(3),
                    ),
                  ),
                  Expanded(
                    child: _NavItem(
                      icon: Icons.person_outline,
                      label: 'tab_profile'.tr(context: context),
                      isActive: currentIndex == 4,
                      onTap: () => _handleTabTap(4),
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

class _NavItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool isActive;
  final VoidCallback onTap;

  const _NavItem({
    required this.icon,
    required this.label,
    required this.isActive,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final color = isActive ? AppColors.burgundy : AppColors.taupe;

    return Semantics(
      label: label,
      button: true,
      selected: isActive,
      child: GestureDetector(
        onTap: onTap,
        behavior: HitTestBehavior.opaque,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 2.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 22, color: color),
              const SizedBox(height: 3),
              FittedBox(
                fit: BoxFit.scaleDown,
                child: Text(
                  label,
                  style: AppTextStyles.labelSmall.copyWith(
                    fontSize: 10.5,
                    color: color,
                    fontWeight: FontWeight.w700,
                  ),
                  maxLines: 1,
                ),
              ),
              const SizedBox(height: 3),
              if (isActive)
                SizedBox(
                  width: 14,
                  height: 2,
                  child: CustomPaint(
                    painter: _DashedLinePainter(color: AppColors.burgundy),
                  ),
                )
              else
                const SizedBox(height: 2),
            ],
          ),
        ),
      ),
    );
  }
}

class _DashedLinePainter extends CustomPainter {
  final Color color;
  const _DashedLinePainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    const dashWidth = 3.0;
    const dashGap = 2.5;
    double x = 0;
    while (x < size.width) {
      canvas.drawLine(Offset(x, 0), Offset(x + dashWidth, 0), paint);
      x += dashWidth + dashGap;
    }
  }

  @override
  bool shouldRepaint(_DashedLinePainter old) => old.color != color;
}
