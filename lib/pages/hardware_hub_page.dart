import 'package:flutter/material.dart';
import 'hardware/bluetooth_demo_page.dart';
import 'hardware/camera_demo_page.dart';
import 'hardware/file_read_demo_page.dart';
import 'hardware/gps_demo_page.dart';
import 'hardware/sensor_demo_page.dart';

class HardwareHubPage extends StatelessWidget {
  const HardwareHubPage({super.key});

  @override
  Widget build(BuildContext context) {
    final List<_HardwareItem> items = <_HardwareItem>[
      _HardwareItem(
        title: 'GPS 定位示例',
        subtitle: '获取权限 + 读取经纬度',
        icon: Icons.my_location,
        builder: (_) => const GpsDemoPage(),
      ),
      _HardwareItem(
        title: '陀螺仪/加速度计示例',
        subtitle: '实时读取传感器数据',
        icon: Icons.screen_rotation_alt,
        builder: (_) => const SensorDemoPage(),
      ),
      _HardwareItem(
        title: '相机示例',
        subtitle: '拍照并在页面中预览',
        icon: Icons.camera_alt_outlined,
        builder: (_) => const CameraDemoPage(),
      ),
      _HardwareItem(
        title: '文件读取示例',
        subtitle: '选择本地文件并读取文本',
        icon: Icons.insert_drive_file_outlined,
        builder: (_) => const FileReadDemoPage(),
      ),
      _HardwareItem(
        title: '蓝牙示例',
        subtitle: '打开蓝牙 + 扫描附近设备',
        icon: Icons.bluetooth_searching,
        builder: (_) => const BluetoothDemoPage(),
      ),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('硬件设备示例')),
      body: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: items.length,
        separatorBuilder: (_, __) => const SizedBox(height: 10),
        itemBuilder: (BuildContext context, int index) {
          final _HardwareItem item = items[index];
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

class _HardwareItem {
  _HardwareItem({
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
