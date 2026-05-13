import 'package:flutter/material.dart';
import '../widgets/demo_page_template.dart';

class AsyncListPage extends StatefulWidget {
  const AsyncListPage({super.key});

  @override
  State<AsyncListPage> createState() => _AsyncListPageState();
}

class _AsyncListPageState extends State<AsyncListPage> {
  late Future<List<String>> _futureItems;
  bool _simulateError = false;

  @override
  void initState() {
    super.initState();
    _futureItems = _loadItems();
  }

  Future<List<String>> _loadItems() async {
    await Future<void>.delayed(const Duration(seconds: 2));
    if (_simulateError) {
      throw Exception('模拟网络异常');
    }
    return List<String>.generate(12, (int index) => '异步数据项 #${index + 1}');
  }

  void _reload() {
    setState(() {
      _futureItems = _loadItems();
    });
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '异步加载与列表展示',
      scenario: '请求接口、分页列表、下拉刷新都属于异步加载场景，FutureBuilder 是入门首选写法。',
      tips: const <String>[
        '把延迟从 2 秒改成 500ms，对比加载体验',
        '把 ListView.builder 改成 ListView.separated',
        '增加“空列表”分支，模拟无数据状态',
      ],
      keyCode:
          '''
FutureBuilder<List<String>>(
  future: futureItems,
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const CircularProgressIndicator();
    }
    if (snapshot.hasError) {
      return Text('加载失败: \${snapshot.error}');
    }
    return ListView.builder(...);
  },
)
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('模拟接口错误'),
            value: _simulateError,
            onChanged: (bool value) {
              setState(() {
                _simulateError = value;
              });
            },
          ),
          const SizedBox(height: 8),
          FilledButton.icon(
            onPressed: _reload,
            icon: const Icon(Icons.refresh),
            label: const Text('重新加载'),
          ),
          const SizedBox(height: 12),
          FutureBuilder<List<String>>(
            future: _futureItems,
            builder:
                (BuildContext context, AsyncSnapshot<List<String>> snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Padding(
                      padding: EdgeInsets.symmetric(vertical: 20),
                      child: Center(child: CircularProgressIndicator()),
                    );
                  }
                  if (snapshot.hasError) {
                    return Text(
                      '加载失败：${snapshot.error}',
                      style: TextStyle(
                        color: Theme.of(context).colorScheme.error,
                      ),
                    );
                  }
                  final List<String> items = snapshot.data ?? <String>[];
                  if (items.isEmpty) {
                    return const Text('暂无数据');
                  }
                  return ListView.separated(
                    physics: const NeverScrollableScrollPhysics(),
                    shrinkWrap: true,
                    itemCount: items.length,
                    separatorBuilder: (BuildContext context, int index) =>
                        const Divider(height: 1),
                    itemBuilder: (BuildContext context, int index) {
                      return ListTile(
                        leading: const Icon(Icons.list_alt_outlined),
                        title: Text(items[index]),
                      );
                    },
                  );
                },
          ),
        ],
      ),
    );
  }
}
