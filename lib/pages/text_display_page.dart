import 'package:flutter/material.dart';
import '../widgets/demo_page_template.dart';
import '../widgets/network_image_with_fallback.dart';

class TextDisplayPage extends StatefulWidget {
  const TextDisplayPage({super.key});

  @override
  State<TextDisplayPage> createState() => _TextDisplayPageState();
}

class _TextDisplayPageState extends State<TextDisplayPage> {
  double _fontSize = 18;
  bool _ellipsis = true;

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '文本与显示组件',
      scenario: '用于展示标题、正文、标签、头像和图片，是几乎所有页面都会用到的基础能力。',
      tips: const <String>[
        '修改 Text 的 fontSize、fontWeight、color',
        '把 maxLines 从 1 改成 2 或 3，观察省略号变化',
        '替换网络图片 URL，故意写错看看兜底效果',
      ],
      keyCode: '''
Text(
  'Flutter 文本展示示例',
  style: TextStyle(fontSize: fontSize, fontWeight: FontWeight.bold),
  maxLines: 1,
  overflow: TextOverflow.ellipsis,
)

Image.network(
  url,
  errorBuilder: (_, __, ___) => const Icon(Icons.broken_image),
)
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Text(
            'Flutter 文本展示示例（可调字号）',
            maxLines: _ellipsis ? 1 : 2,
            overflow: _ellipsis ? TextOverflow.ellipsis : TextOverflow.visible,
            style: TextStyle(fontSize: _fontSize, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          RichText(
            text: TextSpan(
              style: Theme.of(context).textTheme.bodyMedium,
              children: const <InlineSpan>[
                TextSpan(text: 'RichText 可以在同一行里设置 '),
                TextSpan(
                  text: '不同颜色',
                  style: TextStyle(color: Colors.blue),
                ),
                TextSpan(text: ' 和 '),
                TextSpan(
                  text: '不同粗细',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                TextSpan(text: '。'),
              ],
            ),
          ),
          const SizedBox(height: 10),
          const Row(
            children: <Widget>[
              Icon(Icons.star, color: Colors.orange),
              SizedBox(width: 8),
              Chip(label: Text('常用展示组件')),
              SizedBox(width: 8),
              CircleAvatar(child: Text('F')),
            ],
          ),
          const SizedBox(height: 14),
          const NetworkImageWithFallback(url: 'https://picsum.photos/600/260'),
          const SizedBox(height: 14),
          Text('字体大小：${_fontSize.toStringAsFixed(0)}'),
          Slider(
            min: 14,
            max: 32,
            value: _fontSize,
            onChanged: (double value) {
              setState(() {
                _fontSize = value;
              });
            },
          ),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('开启单行省略'),
            value: _ellipsis,
            onChanged: (bool value) {
              setState(() {
                _ellipsis = value;
              });
            },
          ),
        ],
      ),
    );
  }
}
