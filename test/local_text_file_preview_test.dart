import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_dudo/services/local_text_file_preview.dart';

void main() {
  late Directory directory;

  setUp(() async {
    directory = await Directory.systemTemp.createTemp('dudo-file-preview-');
  });

  tearDown(() async {
    await directory.delete(recursive: true);
  });

  test('reads a bounded preview and returns only the file name', () async {
    final file = File('${directory.path}${Platform.pathSeparator}notes.txt');
    await file.writeAsString('a' * 450);

    final preview = await LocalTextFilePreview.read(file.path);

    expect(preview.fileName, 'notes.txt');
    expect(preview.content, '${'a' * 400}...');
    expect(preview.fileName, isNot(contains(directory.path)));
  });

  test('rejects files over 5 MiB before reading their contents', () async {
    final file = File('${directory.path}${Platform.pathSeparator}large.txt');
    await file.writeAsBytes(List<int>.filled(LocalTextFilePreview.maxBytes + 1, 0));

    await expectLater(
      LocalTextFilePreview.read(file.path),
      throwsA(isA<FormatException>()),
    );
  });
}
