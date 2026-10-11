import 'package:flutter/material.dart';

import '../services/ai_assistant_service.dart';

class AiAssistantPage extends StatefulWidget {
  AiAssistantPage({
    super.key,
    AiSettingsRepository? settingsRepository,
    OpenAiCompatClient? client,
  }) : settingsRepository = settingsRepository ?? SecureAiSettingsRepository(),
       client = client ?? const OpenAiCompatClient();

  final AiSettingsRepository settingsRepository;
  final OpenAiCompatClient client;

  @override
  State<AiAssistantPage> createState() => _AiAssistantPageState();
}

class _AiAssistantPageState extends State<AiAssistantPage> {
  final _endpoint = TextEditingController();
  final _model = TextEditingController();
  final _apiKey = TextEditingController();
  final _prompt = TextEditingController();
  String _answer = '';
  String? _error;
  bool _loading = true;
  bool _sending = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final settings = await widget.settingsRepository.load();
      _endpoint.text = settings.endpoint;
      _model.text = settings.model;
      _apiKey.text = settings.apiKey;
    } catch (_) {
      _error = '无法读取本机 AI 配置。';
    }
    if (mounted) setState(() => _loading = false);
  }

  AiSettings get _settings => AiSettings(
    endpoint: _endpoint.text,
    model: _model.text,
    apiKey: _apiKey.text,
  );

  Future<void> _save() async {
    try {
      OpenAiCompatClient.validateEndpoint(_endpoint.text);
      if (_model.text.trim().isEmpty)
        throw const AiRequestException('请填写模型名称。');
      await widget.settingsRepository.save(_settings);
      if (mounted) {
        setState(() => _error = null);
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text('AI 连接配置已安全保存到本机。')));
      }
    } on AiRequestException catch (error) {
      if (mounted) setState(() => _error = error.message);
    } catch (_) {
      if (mounted) setState(() => _error = '保存 AI 配置失败。');
    }
  }

  Future<void> _ask() async {
    if (_sending) return;
    setState(() {
      _sending = true;
      _error = null;
      _answer = '';
    });
    try {
      await widget.settingsRepository.save(_settings);
      final answer = await widget.client.chat(
        settings: _settings,
        prompt: _prompt.text,
      );
      if (mounted) setState(() => _answer = answer);
    } on AiRequestException catch (error) {
      if (mounted) setState(() => _error = error.message);
    } catch (_) {
      if (mounted) setState(() => _error = 'AI 请求失败，请检查配置后重试。');
    } finally {
      if (mounted) setState(() => _sending = false);
    }
  }

  @override
  void dispose() {
    _endpoint.dispose();
    _model.dispose();
    _apiKey.dispose();
    _prompt.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI 助手')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(20),
              children: [
                Text('模型连接', style: Theme.of(context).textTheme.titleLarge),
                const SizedBox(height: 12),
                TextField(
                  controller: _endpoint,
                  keyboardType: TextInputType.url,
                  decoration: const InputDecoration(
                    labelText: 'Chat Completions 地址',
                    hintText: 'http://192.168.1.9:11434/v1/chat/completions',
                  ),
                ),
                TextField(
                  controller: _model,
                  decoration: const InputDecoration(labelText: '模型名称'),
                ),
                TextField(
                  controller: _apiKey,
                  obscureText: true,
                  autofillHints: const [AutofillHints.password],
                  decoration: const InputDecoration(
                    labelText: 'API Key（本机安全存储，可留空）',
                  ),
                ),
                const SizedBox(height: 10),
                Align(
                  alignment: Alignment.centerRight,
                  child: OutlinedButton.icon(
                    onPressed: _sending ? null : _save,
                    icon: const Icon(Icons.lock_outline),
                    label: const Text('保存连接'),
                  ),
                ),
                const Divider(height: 32),
                TextField(
                  controller: _prompt,
                  minLines: 3,
                  maxLines: 7,
                  maxLength: 8000,
                  decoration: const InputDecoration(
                    labelText: '问题',
                    hintText: '例如：用一个 Flutter 示例解释状态提升',
                    alignLabelWithHint: true,
                  ),
                ),
                FilledButton.icon(
                  onPressed: _sending ? null : _ask,
                  icon: _sending
                      ? const SizedBox.square(
                          dimension: 18,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.send_outlined),
                  label: Text(_sending ? '正在请求' : '发送问题'),
                ),
                if (_error != null) ...[
                  const SizedBox(height: 12),
                  Text(
                    _error!,
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.error,
                    ),
                  ),
                ],
                if (_answer.isNotEmpty) ...[
                  const SizedBox(height: 20),
                  SelectableText(_answer),
                ],
                const SizedBox(height: 16),
                const Text('问题仅在你主动发送后传给配置的模型服务。API Key 使用 Android 安全存储。'),
              ],
            ),
    );
  }
}
