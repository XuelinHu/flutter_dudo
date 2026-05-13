import 'package:flutter/material.dart';
import 'pages/home_page.dart';
import 'pages/navigation/route_detail_page.dart';

class FlutterWidgetLabApp extends StatefulWidget {
  const FlutterWidgetLabApp({super.key});

  @override
  State<FlutterWidgetLabApp> createState() => _FlutterWidgetLabAppState();
}

class _FlutterWidgetLabAppState extends State<FlutterWidgetLabApp> {
  ThemeMode _themeMode = ThemeMode.light;

  void _updateThemeMode(ThemeMode mode) {
    setState(() {
      _themeMode = mode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter 组件实验手册',
      debugShowCheckedModeBanner: false,
      themeMode: _themeMode,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        appBarTheme: const AppBarTheme(centerTitle: true),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.dark,
        ),
        appBarTheme: const AppBarTheme(centerTitle: true),
      ),
      routes: <String, WidgetBuilder>{
        RouteDetailPage.routeName: (BuildContext context) {
          final Object? args = ModalRoute.of(context)?.settings.arguments;
          final String message = args is String ? args : '未传递参数';
          return RouteDetailPage(message: message);
        },
      },
      home: HomePage(
        currentThemeMode: _themeMode,
        onThemeModeChanged: _updateThemeMode,
      ),
    );
  }
}
