import 'package:flutter/material.dart';
import '../widgets/demo_page_template.dart';

class LayoutWidgetsPage extends StatefulWidget {
  const LayoutWidgetsPage({super.key});

  @override
  State<LayoutWidgetsPage> createState() => _LayoutWidgetsPageState();
}

class _LayoutWidgetsPageState extends State<LayoutWidgetsPage> {
  double _spacing = 8;

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '常见布局组件',
      scenario: '当你需要把组件横向、纵向、换行或层叠摆放时，会频繁使用 Row、Column、Wrap、Stack。',
      tips: const <String>[
        '修改 Expanded 的 flex 比例，观察占位变化',
        '把 Wrap 的 spacing / runSpacing 改大或改小',
        '调整 Stack 中 Positioned 的 top / right 值',
      ],
      keyCode: '''
Row(
  children: const [
    Expanded(flex: 1, child: DemoBox('A')),
    SizedBox(width: 8),
    Expanded(flex: 2, child: DemoBox('B')),
  ],
)
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          const Text('1) Row + Expanded'),
          const SizedBox(height: 8),
          Row(
            children: <Widget>[
              const Expanded(flex: 1, child: _DemoColorBox(label: 'flex:1')),
              SizedBox(width: _spacing),
              const Expanded(flex: 2, child: _DemoColorBox(label: 'flex:2')),
            ],
          ),
          const SizedBox(height: 16),
          const Text('2) Wrap 自动换行'),
          const SizedBox(height: 8),
          Wrap(
            spacing: _spacing,
            runSpacing: _spacing,
            children: const <Widget>[
              Chip(label: Text('Flutter')),
              Chip(label: Text('Dart')),
              Chip(label: Text('Widget')),
              Chip(label: Text('Layout')),
              Chip(label: Text('State')),
            ],
          ),
          const SizedBox(height: 16),
          const Text('3) Stack 层叠'),
          const SizedBox(height: 8),
          SizedBox(
            height: 130,
            child: Stack(
              children: <Widget>[
                Container(
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.primaryContainer,
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                const Positioned(left: 12, bottom: 12, child: Text('底层容器')),
                Positioned(
                  top: _spacing * 1.2,
                  right: _spacing * 1.2,
                  child: const CircleAvatar(child: Icon(Icons.layers)),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Text('间距：${_spacing.toStringAsFixed(0)}'),
          Slider(
            min: 4,
            max: 24,
            value: _spacing,
            onChanged: (double value) {
              setState(() {
                _spacing = value;
              });
            },
          ),
        ],
      ),
    );
  }
}

class _DemoColorBox extends StatelessWidget {
  const _DemoColorBox({required this.label});

  final String label;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 58,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.secondaryContainer,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Text(label),
    );
  }
}
