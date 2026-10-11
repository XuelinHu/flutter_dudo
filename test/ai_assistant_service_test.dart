import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_dudo/services/ai_assistant_service.dart';

void main() {
  test('requires HTTPS for public endpoints and permits private LAN HTTP', () {
    expect(
      () => OpenAiCompatClient.validateEndpoint(
        'http://api.example.com/v1/chat/completions',
      ),
      throwsA(isA<AiRequestException>()),
    );
    expect(
      OpenAiCompatClient.validateEndpoint(
        'http://192.168.1.9:11434/v1/chat/completions',
      ).host,
      '192.168.1.9',
    );
    expect(
      OpenAiCompatClient.validateEndpoint(
        'https://api.example.com/v1/chat/completions',
      ).host,
      'api.example.com',
    );
  });

  test('sends a bounded OpenAI-compatible chat request', () async {
    final server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    final handler = () async {
      await for (final request in server) {
        final body = await utf8.decoder.bind(request).join();
        expect(
          request.headers.value(HttpHeaders.authorizationHeader),
          'Bearer test-key',
        );
        expect(
          (jsonDecode(body) as Map<String, dynamic>)['model'],
          'test-model',
        );
        request.response
          ..headers.contentType = ContentType.json
          ..write(
            jsonEncode({
              'choices': [
                {
                  'message': {'content': '可运行的回答'},
                },
              ],
            }),
          );
        await request.response.close();
        break;
      }
    }();
    final endpoint = 'http://127.0.0.1:${server.port}/v1/chat/completions';

    final answer = await const OpenAiCompatClient().chat(
      settings: AiSettings(
        endpoint: endpoint,
        model: 'test-model',
        apiKey: 'test-key',
      ),
      prompt: '解释状态提升',
    );
    await handler;
    await server.close(force: true);
    expect(answer, '可运行的回答');
  });

  test('rejects redirects without forwarding the API key', () async {
    final destination = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    var redirectedRequests = 0;
    final destinationHandler = () async {
      await for (final _ in destination) {
        redirectedRequests += 1;
      }
    }();
    final server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    final handler = () async {
      await for (final request in server) {
        await request.drain<void>();
        request.response
          ..statusCode = HttpStatus.found
          ..headers.set(
            HttpHeaders.locationHeader,
            'http://127.0.0.1:${destination.port}/capture',
          );
        await request.response.close();
        break;
      }
    }();

    await expectLater(
      const OpenAiCompatClient().chat(
        settings: AiSettings(
          endpoint: 'http://127.0.0.1:${server.port}/v1/chat/completions',
          model: 'test-model',
          apiKey: 'test-key',
        ),
        prompt: 'test',
      ),
      throwsA(isA<AiRequestException>()),
    );
    await handler;
    await server.close(force: true);
    await destination.close(force: true);
    await destinationHandler;
    expect(redirectedRequests, 0);
  });

  test('rejects responses larger than 1 MiB', () async {
    final server = await HttpServer.bind(InternetAddress.loopbackIPv4, 0);
    final handler = () async {
      await for (final request in server) {
        await request.drain<void>();
        request.response
          ..headers.contentType = ContentType.json
          ..write('{"choices":[],"padding":"${'x' * (1024 * 1024)}"}');
        await request.response.close();
        break;
      }
    }();

    await expectLater(
      const OpenAiCompatClient().chat(
        settings: AiSettings(
          endpoint: 'http://127.0.0.1:${server.port}/v1/chat/completions',
          model: 'test-model',
        ),
        prompt: 'test',
      ),
      throwsA(isA<AiRequestException>()),
    );
    await handler;
    await server.close(force: true);
  });
}
