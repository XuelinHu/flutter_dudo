import 'package:flutter/material.dart';
import 'async_list_page.dart';
import 'button_interaction_page.dart';
import 'feedback_page.dart';
import 'form_input_page.dart';
import 'hardware_hub_page.dart';
import 'layout_widgets_page.dart';
import 'navigation_page.dart';
import 'state_lifting_page.dart';
import 'text_display_page.dart';
import 'theme_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({
    super.key,
    required this.currentThemeMode,
    required this.onThemeModeChanged,
  });

  final ThemeMode currentThemeMode;
  final ValueChanged<ThemeMode> onThemeModeChanged;

  @override
  Widget build(BuildContext context) {
    final List<_ModuleItem> modules = <_ModuleItem>[
      _ModuleItem(
        title: '文本与显示组件学习',
        subtitle: 'Text / RichText / Image / Icon',
        icon: Icons.text_fields,
        builder: (BuildContext context) => const TextDisplayPage(),
      ),
      _ModuleItem(
        title: '常见布局组件学习',
        subtitle: 'Row / Column / Expanded / Wrap / Stack',
        icon: Icons.dashboard_customize_outlined,
        builder: (BuildContext context) => const LayoutWidgetsPage(),
      ),
      _ModuleItem(
        title: '按钮与点击交互学习',
        subtitle: 'ElevatedButton / OutlinedButton / IconButton',
        icon: Icons.touch_app_outlined,
        builder: (BuildContext context) => const ButtonInteractionPage(),
      ),
      _ModuleItem(
        title: '输入组件与表单学习',
        subtitle: 'TextField / Form / Dropdown / Switch',
        icon: Icons.edit_note_outlined,
        builder: (BuildContext context) => const FormInputPage(),
      ),
      _ModuleItem(
        title: '弹窗与提示反馈学习',
        subtitle: 'SnackBar / Dialog / BottomSheet',
        icon: Icons.notifications_active_outlined,
        builder: (BuildContext context) => const FeedbackPage(),
      ),
      _ModuleItem(
        title: '导航与页面切换学习',
        subtitle: 'Navigator.push / pushNamed / pop',
        icon: Icons.route_outlined,
        builder: (BuildContext context) => const NavigationPage(),
      ),
      _ModuleItem(
        title: '状态更新与父子传值学习',
        subtitle: 'setState + 回调函数传值',
        icon: Icons.swap_horiz_outlined,
        builder: (BuildContext context) => const StateLiftingPage(),
      ),
      _ModuleItem(
        title: '主题样式学习',
        subtitle: 'ThemeData / ThemeMode',
        icon: Icons.palette_outlined,
        builder: (BuildContext context) => ThemeStudyPage(
          currentMode: currentThemeMode,
          onThemeModeChanged: onThemeModeChanged,
        ),
      ),
      _ModuleItem(
        title: '异步加载与列表展示学习',
        subtitle: 'FutureBuilder + ListView',
        icon: Icons.cloud_download_outlined,
        builder: (BuildContext context) => const AsyncListPage(),
      ),
      _ModuleItem(
        title: '硬件设备示例学习',
        subtitle: 'GPS / 传感器 / 相机 / 文件 / 蓝牙',
        icon: Icons.memory_outlined,
        builder: (BuildContext context) => const HardwareHubPage(),
      ),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Flutter 组件实验手册')),
      body: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: modules.length,
        separatorBuilder: (BuildContext context, int index) =>
            const SizedBox(height: 10),
        itemBuilder: (BuildContext context, int index) {
          final _ModuleItem item = modules[index];
          return Card(
            child: ListTile(
              leading: CircleAvatar(child: Icon(item.icon)),
              title: Text(item.title),
              subtitle: Text(item.subtitle),
              trailing: const Icon(Icons.chevron_right),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute<Widget>(builder: item.builder),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

class _ModuleItem {
  _ModuleItem({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.builder,
  });

  final String title;
  final String subtitle;
  final IconData icon;
  final WidgetBuilder builder;
}
