# 软著事实摘要

## 软件名称候选
- 基于Flutter的安卓开发学习移动应用软件（推荐）
- Flutter组件实验学习手册软件
- 安卓开发基础组件学习平台软件
- 移动端Flutter组件教学演示系统
- Flutter硬件能力实验教学软件

推荐名称说明：当前应用既覆盖 Flutter 基础组件教学，又明确以 Android 真机运行和移动端学习为交付形态，因此“基于Flutter的安卓开发学习移动应用软件”最能准确反映软件用途、实现技术和运行平台。

## 已核验事实
- 项目类型：Flutter Android 移动应用，仓库目录同时包含 `android/`、`ios/`、`lib/` 等 Flutter 标准结构。
- 应用标题：`Flutter组件实验手册`。
- Android 包名：`com.example.flutter_dudo`。
- 当前版本：`1.0.0`。
- 运行真机：`OPPO PKS110`，系统 `Android 16`，分辨率 `1080x2412`。
- 核心代码规模：约 2009 行自研代码。
- 页面模块：文本显示、布局、按钮交互、表单、反馈、导航、状态提升、主题、异步列表、硬件入口、GPS、传感器、相机、文件读取、蓝牙扫描。
- 使用插件：`geolocator`、`sensors_plus`、`image_picker`、`file_picker`、`flutter_blue_plus`。
- Android 权限：粗略定位、精确定位、相机、媒体图片读取、蓝牙、蓝牙管理、蓝牙扫描、蓝牙连接。
- 构建方式：Flutter + Android Gradle Kotlin DSL + Kotlin Android 插件。

## 冲突与缺失
- 仓库 README 仍为 Flutter 默认模板，未描述真实业务背景，本次软著说明以代码和真机截图事实为准。
- Android `applicationId` 仍使用示例包名 `com.example.flutter_dudo`，可用于当前材料，但如后续正式发布建议替换为稳定产品包名。
- 开发机 CPU、内存和操作系统已从当前环境提取；若登记主体要求填写更细的开发工具版本清单，可继续补充 IDE 版本信息。
- GPS 页面截图已完成入口页采集，当前截图体现“定位按钮与结果区域”结构；若需要展示实时经纬度数值，可在后续人工触发定位后补采一张结果页。
