import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:crop_wise_weather_app/main.dart';

void main() {
  testWidgets('Renders WeatherHomePage', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const WeatherApp());

    // Verify that the title is rendered.
    expect(find.text('Weather App'), findsOneWidget);
  });
}
