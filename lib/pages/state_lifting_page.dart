import 'package:flutter/material.dart';
import '../widgets/demo_page_template.dart';

class StateLiftingPage extends StatefulWidget {
  const StateLiftingPage({super.key});

  @override
  State<StateLiftingPage> createState() => _StateLiftingPageState();
}

class _StateLiftingPageState extends State<StateLiftingPage> {
  int _count = 0;
  int _step = 1;

  void _add() {
    setState(() {
      _count += _step;
    });
  }

  void _minus() {
    setState(() {
      _count -= _step;
    });
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '状态更新与父子传值',
      scenario: '父组件保存状态，子组件通过回调通知父组件更新，是 Flutter 初学阶段最核心的状态模式。',
      tips: const <String>[
        '把 step 从下拉改成 Slider，体验不同交互方式',
        '在子组件中增加重置按钮，回调父组件清零',
        '尝试把 count 封装成独立模型对象再传递',
      ],
      keyCode: '''
ChildCounter(
  value: count,
  onAdd: handleAdd,
  onMinus: handleMinus,
)
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          _StepSelector(
            step: _step,
            onStepChanged: (int value) {
              setState(() {
                _step = value;
              });
            },
          ),
          const SizedBox(height: 12),
          ChildCounter(value: _count, onAdd: _add, onMinus: _minus),
        ],
      ),
    );
  }
}

class ChildCounter extends StatelessWidget {
  const ChildCounter({
    super.key,
    required this.value,
    required this.onAdd,
    required this.onMinus,
  });

  final int value;
  final VoidCallback onAdd;
  final VoidCallback onMinus;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text('当前值：$value', style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 10),
            Wrap(
              spacing: 10,
              children: <Widget>[
                FilledButton(onPressed: onAdd, child: const Text('+ 增加')),
                OutlinedButton(onPressed: onMinus, child: const Text('- 减少')),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _StepSelector extends StatelessWidget {
  const _StepSelector({required this.step, required this.onStepChanged});

  final int step;
  final ValueChanged<int> onStepChanged;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: <Widget>[
        const Text('步长：'),
        const SizedBox(width: 8),
        DropdownButton<int>(
          value: step,
          items: const <DropdownMenuItem<int>>[
            DropdownMenuItem(value: 1, child: Text('1')),
            DropdownMenuItem(value: 2, child: Text('2')),
            DropdownMenuItem(value: 5, child: Text('5')),
          ],
          onChanged: (int? value) {
            if (value == null) {
              return;
            }
            onStepChanged(value);
          },
        ),
      ],
    );
  }
}
