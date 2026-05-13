import 'package:flutter/material.dart';
import 'code_block.dart';
import 'section_card.dart';

class DemoPageTemplate extends StatelessWidget {
  const DemoPageTemplate({
    super.key,
    required this.title,
    required this.scenario,
    required this.tips,
    required this.keyCode,
    required this.demoChild,
  });

  final String title;
  final String scenario;
  final List<String> tips;
  final String keyCode;
  final Widget demoChild;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            SectionCard(title: '这个组件的使用场景', child: Text(scenario)),
            SectionCard(
              title: '你可以尝试修改这些参数',
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: tips
                    .map(
                      (String tip) => Padding(
                        padding: const EdgeInsets.only(bottom: 6),
                        child: Text('• $tip'),
                      ),
                    )
                    .toList(),
              ),
            ),
            SectionCard(
              title: '关键代码展示',
              child: CodeBlock(code: keyCode),
            ),
            SectionCard(title: '运行效果', child: demoChild),
          ],
        ),
      ),
    );
  }
}
