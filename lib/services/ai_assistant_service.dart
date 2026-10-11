import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AiSettings {
  const AiSettings({
    this.endpoint = 'http://192.168.1.9:11434/v1/chat/completions',
    this.model = 'qwen3:14b',
    this.apiKey = '',
  });

  final String endpoint;
  final String model;
  final String apiKey;
}

abstract interface class AiSettingsRepository {
  Future<AiSettings> load();
  Future<void> save(AiSettings settings);
}

class SecureAiSettingsRepository implements AiSettingsRepository {
  SecureAiSettingsRepository({FlutterSecureStorage? storage})
    : _storage = storage ?? const FlutterSecureStorage();

  final FlutterSecureStorage _storage;
  static const _endpointKey = 'ai.endpoint';
  static const _modelKey = 'ai.model';
  static const _apiKey = 'ai.api_key';

  @override
  Future<AiSettings> load() async => AiSettings(
    endpoint:
        await _storage.read(key: _endpointKey) ?? const AiSettings().endpoint,
    model: await _storage.read(key: _modelKey) ?? const AiSettings().model,
    apiKey: await _storage.read(key: _apiKey) ?? '',
  );

  @override
  Future<void> save(AiSettings settings) async {
    await _storage.write(key: _endpointKey, value: settings.endpoint.trim());
    await _storage.write(key: _modelKey, value: settings.model.trim());
    if (settings.apiKey.trim().isEmpty) {
      await _storage.delete(key: _apiKey);
    } else {
      await _storage.write(key: _apiKey, value: settings.apiKey.trim());
    }
  }
}

class OpenAiCompatClient {
  const OpenAiCompatClient();

  static Uri validateEndpoint(String value) {
    final uri = Uri.tryParse(value.trim());
    if (uri == null ||
        uri.host.isEmpty ||
        uri.userInfo.isNotEmpty ||
        uri.query.isNotEmpty ||
        uri.fragment.isNotEmpty ||
        !uri.path.endsWith('/chat/completions') ||
        (uri.scheme != 'http' && uri.scheme != 'https')) {
      throw const AiRequestException('请输入有效的 Chat Completions 接口地址。');
    }
    if (uri.scheme == 'http' && !_isPrivateHost(uri.host)) {
      throw const AiRequestException('HTTP 仅允许内网地址；公网服务请使用 HTTPS。');
    }
    return uri;
  }

  static bool _isPrivateHost(String host) {
    final octets = host.split('.').map(int.tryParse).toList();
    if (octets.length != 4 ||
        octets.any((part) => part == null || part > 255)) {
      return host == 'localhost';
    }
    final first = octets[0]!;
    final second = octets[1]!;
    return first == 10 ||
        first == 127 ||
        (first == 172 && second >= 16 && second <= 31) ||
        (first == 192 && second == 168);
  }

  Future<String> chat({
    required AiSettings settings,
    required String prompt,
  }) async {
    final uri = validateEndpoint(settings.endpoint);
    if (settings.model.trim().isEmpty) {
      throw const AiRequestException('请填写模型名称。');
    }
    if (prompt.trim().isEmpty || prompt.length > 8000) {
      throw const AiRequestException('问题不能为空，且不能超过 8000 个字符。');
    }

    final client = HttpClient()..connectionTimeout = const Duration(seconds: 8);
    try {
      final request = await client.postUrl(uri);
      request.followRedirects = false;
      request.headers.contentType = ContentType.json;
      if (settings.apiKey.trim().isNotEmpty) {
        request.headers.set(
          HttpHeaders.authorizationHeader,
          'Bearer ${settings.apiKey.trim()}',
        );
      }
      request.write(
        jsonEncode({
          'model': settings.model.trim(),
          'stream': false,
          'max_tokens': 800,
          'messages': [
            {
              'role': 'system',
              'content':
                  '你是 Flutter 组件实验手册中的 AI 助手。回答准确、简洁，并优先给出可运行的 Flutter 示例。',
            },
            {'role': 'user', 'content': prompt.trim()},
          ],
        }),
      );
      final response = await request.close().timeout(
        const Duration(seconds: 60),
      );
      if (response.statusCode < 200 || response.statusCode >= 300) {
        throw AiRequestException('AI 服务返回 HTTP ${response.statusCode}。');
      }
      const maxResponseBytes = 1024 * 1024;
      final bytes = await response
          .fold<List<int>>(<int>[], (buffer, chunk) {
            if (buffer.length + chunk.length > maxResponseBytes) {
              throw const AiRequestException('AI 服务响应超过 1 MiB 限制。');
            }
            buffer.addAll(chunk);
            return buffer;
          })
          .timeout(const Duration(seconds: 60));
      final body = utf8.decode(bytes);
      final content = (jsonDecode(body) as Map<String, dynamic>)
          .getValue<String>('choices.0.message.content');
      if (content == null || content.trim().isEmpty) {
        throw const AiRequestException('AI 服务没有返回文本内容。');
      }
      return content.trim();
    } on TimeoutException {
      throw const AiRequestException('AI 请求超时，请检查服务状态后重试。');
    } on SocketException {
      throw const AiRequestException('无法连接 AI 服务，请检查地址和局域网连接。');
    } on FormatException {
      throw const AiRequestException('AI 服务返回的数据格式无效。');
    } finally {
      client.close(force: true);
    }
  }
}

extension on Map<String, dynamic> {
  T? getValue<T>(String path) {
    Object? value = this;
    for (final key in path.split('.')) {
      if (value is Map<String, dynamic>) {
        value = value[key];
      } else if (value is List) {
        final index = int.tryParse(key);
        if (index == null || index < 0 || index >= value.length) return null;
        value = value[index];
      } else {
        return null;
      }
    }
    return value is T ? value : null;
  }
}

class AiRequestException implements Exception {
  const AiRequestException(this.message);
  final String message;
  @override
  String toString() => message;
}
