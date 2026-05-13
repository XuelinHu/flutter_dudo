import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import '../../widgets/demo_page_template.dart';

class GpsDemoPage extends StatefulWidget {
  const GpsDemoPage({super.key});

  @override
  State<GpsDemoPage> createState() => _GpsDemoPageState();
}

class _GpsDemoPageState extends State<GpsDemoPage> {
  String _status = '点击按钮开始定位';

  Future<void> _getLocation() async {
    try {
      final bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        setState(() {
          _status = '定位服务未开启，请先打开系统定位';
        });
        return;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
      }
      if (permission == LocationPermission.denied ||
          permission == LocationPermission.deniedForever) {
        setState(() {
          _status = '定位权限被拒绝';
        });
        return;
      }

      final Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() {
        _status =
            '纬度: ${position.latitude.toStringAsFixed(6)}\n经度: ${position.longitude.toStringAsFixed(6)}\n精度: ${position.accuracy.toStringAsFixed(1)} 米';
      });
    } catch (e) {
      setState(() {
        _status = '定位失败: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: 'GPS 定位示例',
      scenario: '适用于外卖、地图、跑步记录、签到打卡等需要获取用户地理位置的场景。',
      tips: const <String>[
        '把精度从 high 改成 low，比较速度与精度',
        '尝试改成持续定位（位置流）',
        '加入经纬度到地址的逆地理编码',
      ],
      keyCode: '''
final position = await Geolocator.getCurrentPosition(
  desiredAccuracy: LocationAccuracy.high,
);
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          FilledButton.icon(
            onPressed: _getLocation,
            icon: const Icon(Icons.my_location),
            label: const Text('获取当前位置'),
          ),
          const SizedBox(height: 12),
          Text(_status),
        ],
      ),
    );
  }
}
