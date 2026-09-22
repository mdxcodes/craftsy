import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:craftsy/features/notifications/screens/notifications_screen.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() async {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      const MethodChannel('plugins.flutter.io/shared_preferences'),
      (MethodCall methodCall) async {
        if (methodCall.method == 'getAll') {
          return <String, Object>{};
        }
        return true;
      },
    );
    await EasyLocalization.ensureInitialized();
  });

  group('NotificationsScreen', () {
    testWidgets('displays notifications with action buttons', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: EasyLocalization(
            supportedLocales: const [Locale('en')],
            path: 'assets/translations',
            fallbackLocale: const Locale('en'),
            useOnlyLangCode: true,
            child: const MaterialApp(
              home: NotificationsScreen(),
            ),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // Should show notification cards
      expect(find.byType(Container), findsWidgets);

      // Should show action buttons (TextButton)
      expect(find.byType(TextButton), findsWidgets);

      // Should show speaker affordance
      expect(find.byIcon(Icons.volume_up_rounded), findsWidgets);
    });

    testWidgets('shows relative time for notifications', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: EasyLocalization(
            supportedLocales: const [Locale('en')],
            path: 'assets/translations',
            fallbackLocale: const Locale('en'),
            useOnlyLangCode: true,
            child: const MaterialApp(
              home: NotificationsScreen(),
            ),
          ),
        ),
      );

      await tester.pumpAndSettle();

      // Should show time indicators (ago, h, m, d)
      expect(find.textContaining('ago'), findsWidgets);
    });
  });
}
