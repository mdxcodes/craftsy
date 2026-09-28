import 'package:flutter/material.dart';

import '../theme/app_text_styles.dart';

class FormattedDescription extends StatelessWidget {
  final String text;
  final TextStyle? style;
  final TextAlign textAlign;

  const FormattedDescription({
    super.key,
    required this.text,
    this.style,
    this.textAlign = TextAlign.start,
  });

  @override
  Widget build(BuildContext context) {
    final paragraphs = text
        .split('\n\n')
        .map((p) => p.trim())
        .where((p) => p.isNotEmpty)
        .toList();

    if (paragraphs.isEmpty) {
      return Text(
        text.trim(),
        style: style ?? AppTextStyles.bodyMedium,
        textAlign: textAlign,
      );
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        for (int i = 0; i < paragraphs.length; i++)
          Text(
            paragraphs[i],
            style: style ?? AppTextStyles.bodyMedium,
            textAlign: textAlign,
          ),
        if (paragraphs.length > 1)
          const SizedBox(height: 8),
      ],
    );
  }
}
