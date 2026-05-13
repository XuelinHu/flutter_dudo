import 'package:flutter/material.dart';
import 'navigation_result.dart';

class RouteDetailPage extends StatelessWidget {
  const RouteDetailPage({super.key, required this.message});

  static const String routeName = '/route-detail';

  final String message;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('详情页')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text('接收到的参数：$message'),
            const SizedBox(height: 16),
            FilledButton(
              onPressed: () {
                Navigator.pop(
                  context,
                  NavigationResult(source: message, timestamp: DateTime.now()),
                );
              },
              child: const Text('返回并携带结果'),
            ),
          ],
        ),
      ),
    );
  }
}
