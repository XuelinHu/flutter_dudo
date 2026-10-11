import 'dart:io';

class LocalTextFilePreview {
  static const int maxBytes = 5 * 1024 * 1024;
  static const int previewCharacters = 400;

  final String fileName;
  final String content;

  const LocalTextFilePreview({required this.fileName, required this.content});

  static Future<LocalTextFilePreview> read(String path) async {
    final file = File(path);
    if (await file.length() > maxBytes) {
      throw const FormatException('文件超过 5 MiB 限制');
    }

    final text = await file.readAsString();
    final fileName = Uri.file(path).pathSegments.last;
    final preview = text.length > previewCharacters
        ? '${text.substring(0, previewCharacters)}...'
        : text;
    return LocalTextFilePreview(fileName: fileName, content: preview);
  }
}
