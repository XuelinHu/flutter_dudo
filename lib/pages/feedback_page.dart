import 'package:flutter/material.dart';
import '../widgets/demo_page_template.dart';

class FeedbackPage extends StatelessWidget {
  const FeedbackPage({super.key});

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '弹窗与提示反馈',
      scenario: '用户执行操作后，需要及时反馈结果，比如成功提示、错误提醒或二次确认。',
      tips: const <String>[
        '把 SnackBar 的持续时间和行为按钮改掉',
        '尝试将 Dialog 换成 AlertDialog 或 SimpleDialog',
        '修改 BottomSheet 内容为你的业务菜单',
      ],
      keyCode: '''
ScaffoldMessenger.of(context).showSnackBar(
  const SnackBar(content: Text('保存成功')),
);

showDialog<void>(
  context: context,
  builder: (_) => const AlertDialog(title: Text('提示')),
);
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: <Widget>[
              FilledButton(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: const Text('这是一个 SnackBar 提示'),
                      action: SnackBarAction(label: '撤销', onPressed: () {}),
                    ),
                  );
                },
                child: const Text('显示 SnackBar'),
              ),
              OutlinedButton(
                onPressed: () {
                  showDialog<void>(
                    context: context,
                    builder: (BuildContext context) {
                      return AlertDialog(
                        title: const Text('删除确认'),
                        content: const Text('确定要删除这条记录吗？'),
                        actions: <Widget>[
                          TextButton(
                            onPressed: () => Navigator.pop(context),
                            child: const Text('取消'),
                          ),
                          FilledButton(
                            onPressed: () => Navigator.pop(context),
                            child: const Text('确定'),
                          ),
                        ],
                      );
                    },
                  );
                },
                child: const Text('显示 Dialog'),
              ),
              ElevatedButton(
                onPressed: () {
                  showModalBottomSheet<void>(
                    context: context,
                    showDragHandle: true,
                    builder: (BuildContext context) {
                      return SafeArea(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: <Widget>[
                            ListTile(
                              leading: const Icon(Icons.edit_outlined),
                              title: const Text('编辑'),
                              onTap: () => Navigator.pop(context),
                            ),
                            ListTile(
                              leading: const Icon(Icons.delete_outline),
                              title: const Text('删除'),
                              onTap: () => Navigator.pop(context),
                            ),
                          ],
                        ),
                      );
                    },
                  );
                },
                child: const Text('显示 BottomSheet'),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
