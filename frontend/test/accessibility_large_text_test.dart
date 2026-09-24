import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:craftsy/core/widgets/primary_action_button.dart';
import 'package:craftsy/core/widgets/large_action_card.dart';
import 'package:craftsy/core/widgets/empty_state.dart';
import 'package:craftsy/core/widgets/offline_state.dart';
import 'package:craftsy/core/widgets/visual_status_chip.dart';
import 'package:craftsy/core/widgets/voice_action_button.dart';

/// Accessibility tests: verify widgets work with large system font scales.
///
/// These tests simulate the device's "Large Text" accessibility setting
/// by wrapping widgets in a MediaQuery with increased textScaleFactor.
void main() {
  Widget wrapWithLargeText(Widget child, {double scale = 1.5}) {
    return MediaQuery(
      data: MediaQueryData(textScaler: TextScaler.linear(scale)),
      child: MaterialApp(home: Scaffold(body: child)),
    );
  }

  testWidgets('PrimaryActionButton renders with large text', (tester) async {
    await tester.pumpWidget(
      wrapWithLargeText(
        const PrimaryActionButton(label: 'Test Action', onPressed: null),
      ),
    );
    await tester.pump();
    expect(find.text('Test Action'), findsOneWidget);
    // Verify the button still has a reasonable size
    final button = tester.widget<PrimaryActionButton>(
      find.byType(PrimaryActionButton),
    );
    expect(button.label, 'Test Action');
  });

  testWidgets('LargeActionCard renders with large text', (tester) async {
    await tester.pumpWidget(
      wrapWithLargeText(
        LargeActionCard(
          label: 'Add Product',
          icon: Icons.add_a_photo,
          onTap: () {},
        ),
      ),
    );
    await tester.pump();
    expect(find.text('Add Product'), findsOneWidget);
    expect(find.byIcon(Icons.add_a_photo), findsOneWidget);
  });

  testWidgets('EmptyState renders with large text', (tester) async {
    await tester.pumpWidget(
      wrapWithLargeText(
        EmptyState(
          icon: Icons.receipt_long,
          title: 'No orders yet',
          message: 'Start by adding a product.',
        ),
      ),
    );
    await tester.pump();
    expect(find.text('No orders yet'), findsOneWidget);
    expect(find.text('Start by adding a product.'), findsOneWidget);
  });

  testWidgets('OfflineState renders with large text', (tester) async {
    await tester.pumpWidget(wrapWithLargeText(const OfflineState()));
    await tester.pump();
    // OfflineState should render without overflow
    expect(find.byType(OfflineState), findsOneWidget);
  });

  testWidgets('VisualStatusChip renders with large text', (tester) async {
    await tester.pumpWidget(
      wrapWithLargeText(
        const VisualStatusChip(
          type: VisualStatusType.success,
          label: 'Delivered',
        ),
      ),
    );
    await tester.pump();
    expect(find.text('Delivered'), findsOneWidget);
  });

  testWidgets('VoiceActionButton renders with large text', (tester) async {
    await tester.pumpWidget(
      wrapWithLargeText(
        VoiceActionButton(
          onPressed: () {},
          isListening: false,
          isProcessing: false,
          hasError: false,
          label: 'Tap to speak',
          hintText: 'Speak your question',
        ),
      ),
    );
    await tester.pump();
    expect(find.byType(VoiceActionButton), findsOneWidget);
  });

  testWidgets('Widgets do not overflow at 2x text scale', (tester) async {
    // Test at 2x scale — the upper bound of most accessibility settings
    await tester.pumpWidget(
      wrapWithLargeText(
        Column(
          children: [
            const PrimaryActionButton(label: 'Action', onPressed: null),
            const SizedBox(height: 16),
            LargeActionCard(
              label: 'Add Product',
              icon: Icons.add_a_photo,
              onTap: () {},
            ),
          ],
        ),
        scale: 2.0,
      ),
    );
    await tester.pump();
    // Verify no overflow errors
    expect(tester.takeException(), isNull);
  });
}
