# Flutter 组件实验手册

<p align="center">
  <img height="20" alt="Flutter" src="https://img.shields.io/badge/flutter-used-02569B" />
  <img height="20" alt="Dart SDK 3.11.4+" src="https://img.shields.io/badge/dart-3.11.4%2B-0175C2" />
</p>

一个 Flutter 常用组件与设备能力的中文学习应用，包含布局、表单、导航、状态、主题、异步列表、GPS、传感器、相机、文件和蓝牙示例。

## AI 模型示例

首页的“AI 模型接入示例”支持 OpenAI Chat Completions 兼容接口，可连接局域网 Ollama、DeepSeek 或兼容服务。默认地址为 `http://192.168.1.9:11434/v1/chat/completions`，模型名可在应用内修改。任何非本机回环 HTTP 接口都不能发送 API Key，配置密钥时必须使用 HTTPS；无密钥的内网 Ollama 仍可使用 HTTP。API Key 通过 Android 安全存储保存，不写入 APK。没有配置模型服务时，应用其余学习模块仍可离线使用。

## 启动与构建

网页演示入口预留 4006，无本地后端；AI 请求由用户配置的模型服务提供。详细端口约定见 [PORTS.md](./PORTS.md)。

```powershell
flutter test
flutter analyze
flutter build apk --release
```

APK 输出到 `dist/flutter-dudo-release.apk`。release 使用 debug 签名，供内网测试安装。
