import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import '../../services/local_text_file_preview.dart';
import '../../widgets/demo_page_template.dart';

class FileReadDemoPage extends StatefulWidget {
  const FileReadDemoPage({super.key});

  @override
  State<FileReadDemoPage> createState() => _FileReadDemoPageState();
}

class _FileReadDemoPageState extends State<FileReadDemoPage> {
  String _status = '请选择一个 txt/json 文件';
  String _contentPreview = '';

  Future<void> _pickAndReadFile() async {
    try {
      final FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: <String>['txt', 'json', 'md'],
      );
      if (result == null || result.files.single.path == null) {
        setState(() {
          _status = '用户取消选择';
        });
        return;
      }
      final String filePath = result.files.single.path!;
      final preview = await LocalTextFilePreview.read(filePath);
      setState(() {
        _status = '读取成功：${preview.fileName}';
        _contentPreview = preview.content;
      });
    } on FormatException {
      setState(() => _status = '文件超过 5 MiB 限制，请选择较小的文本文件。');
    } catch (_) {
      setState(() {
        _status = '读取失败，请确认文件可访问且编码为 UTF-8。';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '文件读取示例',
      scenario: '适用于导入配置、读取日志、选择本地文档、离线数据分析等场景。',
      tips: const <String>[
        '把允许后缀扩展为 csv、xml 等',
        '把 readAsString 改成 readAsBytes 读取二进制',
        '单个文本文件限制为 5 MiB，避免大文件占满内存',
      ],
      keyCode: '''
final result = await FilePicker.platform.pickFiles();
final content = await File(result.files.single.path!).readAsString();
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          FilledButton.icon(
            onPressed: _pickAndReadFile,
            icon: const Icon(Icons.folder_open),
            label: const Text('选择并读取文件'),
          ),
          const SizedBox(height: 12),
          Text(_status),
          const SizedBox(height: 12),
          if (_contentPreview.isNotEmpty)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surfaceContainerHighest,
                borderRadius: BorderRadius.circular(10),
              ),
              child: SelectableText(_contentPreview),
            ),
        ],
      ),
    );
  }
}
