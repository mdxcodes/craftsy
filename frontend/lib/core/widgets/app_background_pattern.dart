import 'package:flutter/material.dart';
import '../theme/app_colors.dart';

/// Craftsy subtle geometric watermark pattern.
///
/// Displays a subtle traditional geometric motif at the bottom of the screen,
/// sitting just above where the bottom navigation bar begins.
///
/// Features:
/// - [opacity]: Configurable opacity (default 0.04, recommended range 0.03–0.06).
/// - [color]: Blend color (defaults to [AppColors.ink]).
/// - [height]: Optional custom height constraint.
/// - [bottomPadding]: Extra bottom inset above the bottom nav bar or safe boundary.
/// - [alignment]: Alignment within parent (defaults to [Alignment.bottomCenter]).
/// - Uses [IgnorePointer] so touch events pass through to content without interception.
/// - Uses [RepaintBoundary] to avoid repainting during scroll and animation events.
class AppBackgroundPattern extends StatelessWidget {
  final double opacity;
  final Color? color;
  final double? height;
  final double bottomPadding;
  final Alignment alignment;
  final BoxFit fit;

  const AppBackgroundPattern({
    super.key,
    this.opacity = 0.04,
    this.color,
    this.height,
    this.bottomPadding = 0.0,
    this.alignment = Alignment.bottomCenter,
    this.fit = BoxFit.fitWidth,
  });

  @override
  Widget build(BuildContext context) {
    if (opacity <= 0.0) {
      return const SizedBox.shrink();
    }

    final tintColor = (color ?? AppColors.ink).withValues(alpha: opacity);

    return IgnorePointer(
      ignoring: true,
      child: RepaintBoundary(
        child: Align(
          alignment: alignment,
          child: Padding(
            padding: EdgeInsets.only(bottom: bottomPadding),
            child: LayoutBuilder(
              builder: (context, constraints) {
                return SizedBox(
                  width: constraints.maxWidth,
                  height: height,
                  child: CustomPaint(
                    painter: _GeometricPatternPainter(color: tintColor),
                    size: Size(constraints.maxWidth, height ?? constraints.maxHeight),
                  ),
                );
              },
            ),
          ),
        ),
      ),
    );
  }
}

class _GeometricPatternPainter extends CustomPainter {
  final Color color;

  _GeometricPatternPainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.2;

    final dotPaint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    final spacing = size.width / 12;
    final rowHeight = size.height / 6;

    for (var row = 0; row < 6; row++) {
      for (var col = 0; col < 12; col++) {
        final x = col * spacing + (row % 2 == 0 ? spacing / 2 : 0);
        final y = size.height - (row + 1) * rowHeight;

        if (x > size.width) continue;

        final radius = spacing * 0.18;

        canvas.drawCircle(Offset(x, y), radius, dotPaint);

        if (col % 3 == 0 && row % 2 == 0) {
          final triSize = spacing * 0.35;
          final path = Path()
            ..moveTo(x - triSize, y + triSize)
            ..lineTo(x + triSize, y + triSize)
            ..lineTo(x, y - triSize)
            ..close();
          canvas.drawPath(path, paint);
        }

        if (col % 4 == 0 && row % 3 == 0) {
          final rectSize = spacing * 0.4;
          final rect = Rect.fromCenter(
            center: Offset(x, y - rowHeight * 0.25),
            width: rectSize,
            height: rectSize,
          );
          canvas.drawRect(rect, paint);
        }
      }
    }
  }

  @override
  bool shouldRepaint(covariant _GeometricPatternPainter oldDelegate) {
    return oldDelegate.color != color;
  }
}
