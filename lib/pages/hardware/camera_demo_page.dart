import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../../widgets/demo_page_template.dart';

class CameraDemoPage extends StatefulWidget {
  const CameraDemoPage({super.key});

  @override
  State<CameraDemoPage> createState() => _CameraDemoPageState();
}

class _CameraDemoPageState extends State<CameraDemoPage> {
  final ImagePicker _picker = ImagePicker();
  XFile? _photo;
  String _status = '还没有拍照';

  Future<void> _takePhoto() async {
    try {
      final XFile? file = await _picker.pickImage(
        source: ImageSource.camera,
        imageQuality: 85,
      );
      if (file == null) {
        setState(() {
          _status = '用户取消了拍照';
        });
        return;
      }
      setState(() {
        _photo = file;
        _status = '拍照成功：${file.path}';
      });
    } catch (e) {
      setState(() {
        _status = '拍照失败: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '相机示例',
      scenario: '适用于头像上传、工单拍照、扫码前置拍摄、OCR 拍照上传等场景。',
      tips: const <String>[
        '修改 imageQuality，比较清晰度和体积',
        '改成 ImageSource.gallery 做相册选择',
        '拍照后增加裁剪/压缩步骤',
      ],
      keyCode: '''
final photo = await ImagePicker().pickImage(
  source: ImageSource.camera,
  imageQuality: 85,
);
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          FilledButton.icon(
            onPressed: _takePhoto,
            icon: const Icon(Icons.camera_alt_outlined),
            label: const Text('打开相机拍照'),
          ),
          const SizedBox(height: 12),
          Text(_status),
          const SizedBox(height: 12),
          if (_photo != null)
            ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Image.file(
                File(_photo!.path),
                height: 220,
                fit: BoxFit.cover,
              ),
            ),
        ],
      ),
    );
  }
}
