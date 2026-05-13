import 'package:flutter/material.dart';
import '../widgets/demo_page_template.dart';

class ButtonInteractionPage extends StatefulWidget {
  const ButtonInteractionPage({super.key});

  @override
  State<ButtonInteractionPage> createState() => _ButtonInteractionPageState();
}

class _ButtonInteractionPageState extends State<ButtonInteractionPage> {
  int _clickCount = 0;
  bool _enabled = true;

  void _handleClick() {
    if (!_enabled) {
      return;
    }
    setState(() {
      _clickCount++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '按钮与点击交互',
      scenario: '提交、取消、跳转、收藏等操作都依赖按钮类组件，是交互入口最常见的一类组件。',
      tips: const <String>[
        '把 onPressed 改成 null，观察禁用态样式',
        '尝试修改按钮的 padding、shape、icon',
        '点击后让按钮文案跟随状态变化',
      ],
      keyCode: '''
ElevatedButton(
  onPressed: enabled ? onClick : null,
  child: const Text('主要按钮'),
)

setState(() {
  clickCount++;
});
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Text('当前点击次数：$_clickCount'),
          const SizedBox(height: 12),
          Wrap(
            spacing: 10,
            runSpacing: 10,
            children: <Widget>[
              ElevatedButton(
                onPressed: _enabled ? _handleClick : null,
                child: const Text('ElevatedButton'),
              ),
              OutlinedButton(
                onPressed: _enabled ? _handleClick : null,
                child: const Text('OutlinedButton'),
              ),
              TextButton(
                onPressed: _enabled ? _handleClick : null,
                child: const Text('TextButton'),
              ),
              IconButton(
                onPressed: _enabled ? _handleClick : null,
                icon: const Icon(Icons.thumb_up_alt_outlined),
              ),
              FilledButton.icon(
                onPressed: _enabled ? _handleClick : null,
                icon: const Icon(Icons.send),
                label: const Text('FilledButton'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('启用按钮'),
            value: _enabled,
            onChanged: (bool value) {
              setState(() {
                _enabled = value;
              });
            },
          ),
          Align(
            alignment: Alignment.centerRight,
            child: FloatingActionButton.small(
              onPressed: _enabled ? _handleClick : null,
              child: const Icon(Icons.add),
            ),
          ),
        ],
      ),
    );
  }
}
