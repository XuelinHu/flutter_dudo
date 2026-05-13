import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import '../../widgets/demo_page_template.dart';

class BluetoothDemoPage extends StatefulWidget {
  const BluetoothDemoPage({super.key});

  @override
  State<BluetoothDemoPage> createState() => _BluetoothDemoPageState();
}

class _BluetoothDemoPageState extends State<BluetoothDemoPage> {
  final List<ScanResult> _results = <ScanResult>[];
  StreamSubscription<List<ScanResult>>? _scanSub;
  bool _scanning = false;
  String _status = '尚未扫描';

  Future<void> _scan() async {
    try {
      _results.clear();
      setState(() {
        _scanning = true;
        _status = '正在扫描 6 秒...';
      });

      await FlutterBluePlus.turnOn();
      _scanSub?.cancel();
      _scanSub = FlutterBluePlus.scanResults.listen((List<ScanResult> data) {
        setState(() {
          _results
            ..clear()
            ..addAll(data);
        });
      });
      await FlutterBluePlus.startScan(timeout: const Duration(seconds: 6));
      setState(() {
        _scanning = false;
        _status = '扫描完成，找到 ${_results.length} 个设备';
      });
    } catch (e) {
      setState(() {
        _scanning = false;
        _status = '扫描失败: $e';
      });
    }
  }

  @override
  void dispose() {
    _scanSub?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return DemoPageTemplate(
      title: '蓝牙示例',
      scenario: '适用于连接手环、温度计、蓝牙打印机、物联网设备等近场通信场景。',
      tips: const <String>[
        '把扫描时间从 6 秒改成 10 秒',
        '按设备名称过滤列表',
        '后续可继续加“连接设备并读写特征值”',
      ],
      keyCode: '''
await FlutterBluePlus.startScan(timeout: const Duration(seconds: 6));
FlutterBluePlus.scanResults.listen((results) {
  setState(() => devices = results);
});
''',
      demoChild: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          FilledButton.icon(
            onPressed: _scanning ? null : _scan,
            icon: const Icon(Icons.bluetooth_searching),
            label: Text(_scanning ? '扫描中...' : '开始蓝牙扫描'),
          ),
          const SizedBox(height: 12),
          Text(_status),
          const SizedBox(height: 12),
          if (_results.isNotEmpty)
            ListView.separated(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _results.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (BuildContext context, int index) {
                final ScanResult result = _results[index];
                final String name = result.device.platformName.isEmpty
                    ? '未命名设备'
                    : result.device.platformName;
                return ListTile(
                  title: Text(name),
                  subtitle: Text(result.device.remoteId.str),
                  trailing: Text('RSSI ${result.rssi}'),
                );
              },
            ),
        ],
      ),
    );
  }
}
