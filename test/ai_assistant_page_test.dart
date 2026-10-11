import 'package:flutter/material.dart';
import 'package:flutter_dudo/pages/ai_assistant_page.dart';
import 'package:flutter_dudo/services/ai_assistant_service.dart';
import 'package:flutter_test/flutter_test.dart';

class _MemorySettings implements AiSettingsRepository {
  AiSettings value = const AiSettings();

  @override
  Future<AiSettings> load() async => value;

  @override
  Future<void> save(AiSettings settings) async => value = settings;
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
}
