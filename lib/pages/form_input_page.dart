import 'package:flutter/material.dart';
import '../widgets/demo_page_template.dart';

class FormInputPage extends StatefulWidget {
  const FormInputPage({super.key});

  @override
  State<FormInputPage> createState() => _FormInputPageState();
}

class _FormInputPageState extends State<FormInputPage> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController _nameController = TextEditingController();

  String _city = '北京';
  bool _acceptProtocol = false;
  String _result = '尚未提交';

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  void _submit() {
    final bool valid = _formKey.currentState?.validate() ?? false;
    if (!valid) {
      return;
    }
    if (!_acceptProtocol) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('请先勾选同意协议')));
      return;
    }
    setState(() {
      _result = '姓名：${_nameController.text}，城市：$_city';
    });
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('提交成功')));
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '输入组件与表单',
      scenario: '登录注册、资料编辑、搜索筛选都离不开输入组件和表单校验。',
      tips: const <String>[
        '给 TextFormField 增加 maxLength 和 keyboardType',
        '修改 validator 的校验规则',
        '把 DropdownButtonFormField 的选项换成你自己的业务枚举',
      ],
      keyCode: '''
Form(
  key: formKey,
  child: TextFormField(
    controller: nameController,
    validator: (value) => value == null || value.isEmpty ? '请输入姓名' : null,
  ),
)
''',
      demoChild: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            TextFormField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: '姓名',
                hintText: '请输入你的姓名',
                border: OutlineInputBorder(),
              ),
              validator: (String? value) {
                if (value == null || value.trim().isEmpty) {
                  return '请输入姓名';
                }
                if (value.trim().length < 2) {
                  return '姓名至少 2 个字符';
                }
                return null;
              },
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _city,
              decoration: const InputDecoration(
                labelText: '城市',
                border: OutlineInputBorder(),
              ),
              items: const <DropdownMenuItem<String>>[
                DropdownMenuItem(value: '北京', child: Text('北京')),
                DropdownMenuItem(value: '上海', child: Text('上海')),
                DropdownMenuItem(value: '广州', child: Text('广州')),
              ],
              onChanged: (String? value) {
                if (value == null) {
                  return;
                }
                setState(() {
                  _city = value;
                });
              },
            ),
            const SizedBox(height: 12),
            CheckboxListTile(
              contentPadding: EdgeInsets.zero,
              value: _acceptProtocol,
              title: const Text('我已阅读并同意协议'),
              onChanged: (bool? value) {
                setState(() {
                  _acceptProtocol = value ?? false;
                });
              },
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: FilledButton(onPressed: _submit, child: const Text('提交')),
            ),
            const SizedBox(height: 12),
            Text('提交结果：$_result'),
          ],
        ),
      ),
    );
  }
}
