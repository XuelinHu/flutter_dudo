import 'package:flutter/material.dart';
import '../widgets/demo_page_template.dart';
import 'navigation/navigation_result.dart';
import 'navigation/route_detail_page.dart';

class NavigationPage extends StatefulWidget {
  const NavigationPage({super.key});

  @override
  State<NavigationPage> createState() => _NavigationPageState();
}

class _NavigationPageState extends State<NavigationPage> {
  String _resultText = '尚未收到返回结果';

  Future<void> _goByPush() async {
    final NavigationResult? result = await Navigator.push<NavigationResult>(
      context,
      MaterialPageRoute<NavigationResult>(
        builder: (BuildContext context) =>
            const RouteDetailPage(message: '来自 Navigator.push'),
      ),
    );
    if (result == null) {
      return;
    }
    setState(() {
      _resultText = '来源：${result.source}，时间：${result.timestamp.toLocal()}';
    });
  }

  Future<void> _goByNamedRoute() async {
    final NavigationResult? result =
        await Navigator.pushNamed<NavigationResult>(
          context,
          RouteDetailPage.routeName,
          arguments: '来自 pushNamed',
        );
    if (result == null) {
      return;
    }
    setState(() {
      _resultText = '来源：${result.source}，时间：${result.timestamp.toLocal()}';
    });
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '导航与页面切换',
      scenario: '多页面 App 会通过 Navigator 在页面间跳转，并经常需要传参与回传结果。',
      tips: const <String>[
        '把参数从字符串改成对象，体验复杂传参',
        '尝试 pushReplacement，观察返回行为差异',
        '给详情页增加更多返回数据字段',
      ],
      keyCode: '''
final result = await Navigator.pushNamed<ResultType>(
  context,
  '/route-detail',
  arguments: 'hello',
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
                onPressed: _goByPush,
                child: const Text('使用 push 跳转'),
              ),
              OutlinedButton(
                onPressed: _goByNamedRoute,
                child: const Text('使用 pushNamed 跳转'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text('回传结果：$_resultText'),
        ],
      ),
    );
  }
}
