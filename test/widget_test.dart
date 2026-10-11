// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_dudo/app.dart';

void main() {
  testWidgets('home lists learning modules and opens a module', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const FlutterWidgetLabApp());

    expect(find.text('Flutter 组件实验手册'), findsOneWidget);
    expect(find.text('文本与显示组件学习'), findsOneWidget);

    await tester.tap(find.text('文本与显示组件学习'));
    await tester.pumpAndSettle();

    expect(find.text('文本与显示组件'), findsOneWidget);
  });
}
