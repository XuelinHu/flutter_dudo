import 'dart:async';
import 'package:flutter/material.dart';
import 'package:sensors_plus/sensors_plus.dart';
import '../../widgets/demo_page_template.dart';

class SensorDemoPage extends StatefulWidget {
  const SensorDemoPage({super.key});

  @override
  State<SensorDemoPage> createState() => _SensorDemoPageState();
}

class _SensorDemoPageState extends State<SensorDemoPage> {
  StreamSubscription<GyroscopeEvent>? _gyroSub;
  StreamSubscription<AccelerometerEvent>? _accSub;
  GyroscopeEvent? _gyro;
  AccelerometerEvent? _acc;
  bool _listening = false;

  void _startListen() {
    _gyroSub?.cancel();
    _accSub?.cancel();
    _gyroSub = gyroscopeEvents.listen((GyroscopeEvent event) {
      setState(() {
        _gyro = event;
      });
    });
    _accSub = accelerometerEvents.listen((AccelerometerEvent event) {
      setState(() {
        _acc = event;
      });
    });
    setState(() {
      _listening = true;
    });
  }

  Future<void> _stopListen() async {
    await _gyroSub?.cancel();
    await _accSub?.cancel();
    setState(() {
      _listening = false;
    });
  }

  @override
  void dispose() {
    _gyroSub?.cancel();
    _accSub?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '陀螺仪/加速度计示例',
      scenario: '适用于体感控制、步态识别、设备姿态判断、运动检测等场景。',
      tips: const <String>[
        '尝试自己加一个低通滤波，观察数据更平滑',
        '把数据保存到列表实现“最近 20 条”',
        '结合阈值实现“摇一摇”触发事件',
      ],
      keyCode: '''
gyroscopeEvents.listen((event) {
  setState(() => gyro = event);
});

accelerometerEvents.listen((event) {
  setState(() => acc = event);
});
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Wrap(
            spacing: 10,
            children: <Widget>[
              FilledButton(
                onPressed: _listening ? null : _startListen,
                child: const Text('开始监听'),
              ),
              OutlinedButton(
                onPressed: _listening ? _stopListen : null,
                child: const Text('停止监听'),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            '陀螺仪(rad/s):\n'
            'x=${_gyro?.x.toStringAsFixed(3) ?? '-'} '
            'y=${_gyro?.y.toStringAsFixed(3) ?? '-'} '
            'z=${_gyro?.z.toStringAsFixed(3) ?? '-'}',
          ),
          const SizedBox(height: 8),
          Text(
            '加速度(m/s²):\n'
            'x=${_acc?.x.toStringAsFixed(3) ?? '-'} '
            'y=${_acc?.y.toStringAsFixed(3) ?? '-'} '
            'z=${_acc?.z.toStringAsFixed(3) ?? '-'}',
          ),
        ],
      ),
    );
  }
}
