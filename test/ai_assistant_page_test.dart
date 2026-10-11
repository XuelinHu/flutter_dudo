import 'package:flutter/material.dart';
import 'package:flutter_dudo/pages/ai_assistant_page.dart';
import 'package:flutter_dudo/services/ai_assistant_service.dart';
import 'package:flutter_test/flutter_test.dart';

class _MemorySettings implements AiSettingsRepository {
  AiSettings value = const AiSettings();
  int saveCount = 0;

  @override
  Future<AiSettings> load() async => value;

  @override
  Future<void> save(AiSettings settings) async {
    saveCount++;
    value = settings;
  }
}

void main() {
  testWidgets(
    'AI assistant exposes endpoint, model, key, and prompt controls',
    (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: AiAssistantPage(settingsRepository: _MemorySettings()),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('AI 助手'), findsOneWidget);
      expect(find.text('Chat Completions 地址'), findsOneWidget);
      expect(find.text('模型名称'), findsOneWidget);
      expect(find.text('API Key（本机安全存储，可留空）'), findsOneWidget);
      expect(find.text('发送问题'), findsOneWidget);
    },
  );

  testWidgets('rejects a LAN HTTP key before saving or sending a prompt', (
    tester,
  ) async {
    final settings = _MemorySettings()
      ..value = const AiSettings(
        endpoint: 'http://192.168.1.9:8999/v1/chat/completions',
        model: 'test-model',
        apiKey: 'test-key',
      );
    await tester.pumpWidget(
      MaterialApp(home: AiAssistantPage(settingsRepository: settings)),
    );
    await tester.pumpAndSettle();
    await tester.enterText(find.byType(TextField).last, 'test prompt');
    await tester.scrollUntilVisible(
      find.text('发送问题'),
      240,
      scrollable: find.byType(Scrollable).first,
    );
    await tester.tap(find.text('发送问题'));
    await tester.pumpAndSettle();

    expect(
      find.text('发送 API Key 必须使用 HTTPS；HTTP 仅允许本机回环地址。'),
      findsOneWidget,
    );
    expect(settings.saveCount, 0);
    await tester.pumpWidget(const SizedBox.shrink());
  });
}
