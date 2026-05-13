import 'package:flutter/material.dart';
import '../widgets/demo_page_template.dart';

class ThemeStudyPage extends StatelessWidget {
  const ThemeStudyPage({
    super.key,
    required this.currentMode,
    required this.onThemeModeChanged,
  });

  final ThemeMode currentMode;
  final ValueChanged<ThemeMode> onThemeModeChanged;

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '主题样式学习',
      scenario: '主题可以统一控制颜色、圆角、字体和亮暗模式，适合全局视觉风格管理。',
      tips: const <String>[
        '修改 seedColor，观察全局组件颜色联动',
        '给 CardTheme 或 InputDecorationTheme 增加统一样式',
        '尝试新增 ThemeMode.system，跟随系统亮暗主题',
      ],
      keyCode: '''
MaterialApp(
  theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue)),
  darkTheme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.blue,
      brightness: Brightness.dark,
    ),
  ),
  themeMode: currentMode,
)
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          SegmentedButton<ThemeMode>(
            segments: const <ButtonSegment<ThemeMode>>[
              ButtonSegment<ThemeMode>(
                value: ThemeMode.light,
                label: Text('浅色'),
                icon: Icon(Icons.light_mode),
              ),
              ButtonSegment<ThemeMode>(
                value: ThemeMode.dark,
                label: Text('深色'),
                icon: Icon(Icons.dark_mode),
              ),
            ],
            selected: <ThemeMode>{currentMode},
            onSelectionChanged: (Set<ThemeMode> values) {
              onThemeModeChanged(values.first);
            },
          ),
          const SizedBox(height: 14),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text(
                    '主题预览卡片',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  const Text('这段文字和按钮会自动跟随当前主题色与亮暗模式。'),
                  const SizedBox(height: 8),
                  FilledButton(onPressed: () {}, child: const Text('主题按钮')),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
