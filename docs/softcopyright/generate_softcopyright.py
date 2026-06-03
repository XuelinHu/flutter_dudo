from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from xml.sax.saxutils import escape

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image as RLImage,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / "docs" / "softcopyright"
ASSET_DIR = ROOT / "docs" / "assets"
DIAGRAM_DIR = ASSET_DIR / "diagrams"
SCREENSHOT_DIR = ASSET_DIR / "screenshots"
TMP_SCREENSHOT_DIR = ROOT / ".tmp" / "softdocs" / "screenshots"
ARCHIVE_ROOT = Path(r"D:\软著")

SOFTWARE_NAME = "基于Flutter的安卓开发学习移动应用软件"
SOFTWARE_VERSION = "V1.0.0"
PACKAGE_NAME = "com.example.flutter_dudo"
APP_TITLE = "Flutter组件实验手册"
DEVICE_MODEL = "OPPO PKS110"
DEVICE_OS = "Android 16"
DEVICE_RESOLUTION = "1080x2412"
BUILD_DATE = "2026-05-13"
FLUTTER_VERSION = "Flutter 3.41.6"
DART_VERSION = "Dart 3.11.4"
DEV_OS = "Microsoft Windows 10 家庭版"
DEV_CPU = "Intel(R) Core(TM) Ultra 9 285H"
DEV_MEMORY = "31.5GB"

SOURCE_DOC_NAME = f"{SOFTWARE_NAME}源代码"
DESIGN_DOC_NAME = "软件设计说明书"


@dataclass(frozen=True)
class SourceFile:
    path: str
    module: str
    purpose: str


SCREENSHOTS = [
    {
        "src": "4-2-home.png",
        "dst": "4-2-home.png",
        "title": "图4-2 系统首页模块列表",
        "entry": "应用启动后默认进入首页",
        "state": "展示全部学习模块入口",
    },
    {
        "src": "6-2-form.png",
        "dst": "6-2-form.png",
        "title": "图6-2 表单输入与校验页面",
        "entry": "首页 -> 输入组件与表单学习",
        "state": "展示文本输入、下拉选择、勾选协议与提交区域",
    },
    {
        "src": "6-3-navigation.png",
        "dst": "6-3-navigation.png",
        "title": "图6-3 页面导航与返回结果页面",
        "entry": "首页 -> 导航与页面切换学习",
        "state": "展示 push 与 pushNamed 两种跳转入口",
    },
    {
        "src": "6-3-route-detail.png",
        "dst": "6-4-route-detail.png",
        "title": "图6-4 路由详情结果页面",
        "entry": "导航页面 -> 使用 push 跳转",
        "state": "展示路由参数接收结果与回传按钮",
    },
    {
        "src": "6-4-theme.png",
        "dst": "6-5-theme.png",
        "title": "图6-5 主题样式切换页面",
        "entry": "首页 -> 主题样式学习",
        "state": "展示浅色/深色主题切换与主题预览卡片",
    },
    {
        "src": "6-5-hardware-hub.png",
        "dst": "6-6-hardware-hub.png",
        "title": "图6-6 硬件能力学习入口页面",
        "entry": "首页 -> 硬件设备示例学习",
        "state": "展示 GPS、传感器、相机、文件与蓝牙五类能力入口",
    },
    {
        "src": "6-6-gps.png",
        "dst": "6-7-gps.png",
        "title": "图6-7 GPS 定位示例页面",
        "entry": "硬件设备示例 -> GPS 定位示例",
        "state": "展示定位按钮、代码示例与定位结果区域",
    },
    {
        "src": "6-7-sensor.png",
        "dst": "6-8-sensor.png",
        "title": "图6-8 传感器监听示例页面",
        "entry": "硬件设备示例 -> 陀螺仪/加速度计示例",
        "state": "已启动监听，显示实时传感器数据",
    },
]


SOURCE_FILES = [
    SourceFile("pubspec.yaml", "项目配置", "定义应用名称、版本号、Flutter SDK 约束和硬件插件依赖。"),
    SourceFile("android/app/build.gradle.kts", "Android 构建配置", "定义 Android 应用命名空间、应用包名、版本号和构建类型。"),
    SourceFile("android/app/src/main/AndroidManifest.xml", "Android 权限配置", "声明定位、相机、蓝牙和媒体读取权限，并配置主入口 Activity。"),
    SourceFile("android/app/src/main/kotlin/com/example/flutter_dudo/MainActivity.kt", "Android 启动入口", "提供 FlutterActivity 宿主，作为 Android 端启动壳。"),
    SourceFile("lib/main.dart", "应用入口", "完成 Flutter 绑定初始化并启动根组件。"),
    SourceFile("lib/app.dart", "根应用", "配置 MaterialApp、主题模式、命名路由和首页挂载。"),
    SourceFile("lib/pages/home_page.dart", "首页模块", "展示全部学习模块列表并负责进入各功能页面。"),
    SourceFile("lib/pages/text_display_page.dart", "基础展示模块", "演示文本、富文本、图片、图标和开关式参数调整。"),
    SourceFile("lib/pages/layout_widgets_page.dart", "布局模块", "演示 Row、Expanded、Wrap、Stack 等常见布局组件。"),
    SourceFile("lib/pages/button_interaction_page.dart", "按钮交互模块", "演示多种按钮组件、启停控制和点击计数。"),
    SourceFile("lib/pages/form_input_page.dart", "表单输入模块", "演示 TextField、下拉框、校验规则与表单提交。"),
    SourceFile("lib/pages/feedback_page.dart", "反馈提示模块", "演示 SnackBar、Dialog 与 BottomSheet 反馈场景。"),
    SourceFile("lib/pages/navigation_page.dart", "页面导航模块", "演示 Navigator.push、pushNamed 与结果回传。"),
    SourceFile("lib/pages/navigation/route_detail_page.dart", "路由详情模块", "接收页面参数并将处理结果返回上级页面。"),
    SourceFile("lib/pages/navigation/navigation_result.dart", "导航结果模型", "定义导航返回数据结构。"),
    SourceFile("lib/pages/state_lifting_page.dart", "状态提升模块", "演示父子组件状态同步、步长切换与回调传值。"),
    SourceFile("lib/pages/theme_page.dart", "主题样式模块", "演示浅色与深色主题切换及统一样式预览。"),
    SourceFile("lib/pages/async_list_page.dart", "异步加载模块", "演示 FutureBuilder、异常状态和异步列表刷新。"),
    SourceFile("lib/pages/hardware_hub_page.dart", "硬件入口模块", "汇聚定位、传感器、相机、文件与蓝牙能力子页面。"),
    SourceFile("lib/pages/hardware/gps_demo_page.dart", "定位能力模块", "封装定位服务检查、权限申请与经纬度读取逻辑。"),
    SourceFile("lib/pages/hardware/sensor_demo_page.dart", "传感器能力模块", "订阅陀螺仪和加速度计数据流并实时更新界面。"),
    SourceFile("lib/pages/hardware/camera_demo_page.dart", "相机能力模块", "通过 image_picker 调起相机并回显拍照结果。"),
    SourceFile("lib/pages/hardware/file_read_demo_page.dart", "文件读取模块", "通过 file_picker 选择本地文件并预览文本内容。"),
    SourceFile("lib/pages/hardware/bluetooth_demo_page.dart", "蓝牙能力模块", "控制蓝牙扫描并展示附近设备列表。"),
    SourceFile("lib/widgets/demo_page_template.dart", "页面模板组件", "统一演示页面的场景说明、提示、代码区和效果区布局。"),
    SourceFile("lib/widgets/section_card.dart", "通用卡片组件", "统一承载模块页面中的分区说明内容。"),
    SourceFile("lib/widgets/code_block.dart", "代码展示组件", "负责高可读性展示示例代码片段。"),
    SourceFile("lib/widgets/network_image_with_fallback.dart", "图片兜底组件", "加载网络图片并在异常时提供本地图标兜底。"),
]


NAME_CANDIDATES = [
    "基于Flutter的安卓开发学习移动应用软件",
    "Flutter组件实验学习手册软件",
    "安卓开发基础组件学习平台软件",
    "移动端Flutter组件教学演示系统",
    "Flutter硬件能力实验教学软件",
]

MODULE_DETAILS = [
    {
        "name": "首页模块",
        "purpose": "统一汇总全部学习专题，作为系统导航总入口。",
        "controls": "卡片式列表项、图标头像、标题、副标题、右箭头跳转提示。",
        "state": "不保存复杂业务状态，主要依赖当前主题模式和页面跳转上下文。",
        "flow": "应用启动后默认进入首页，用户点击任一列表项后进入对应专题页面。",
        "output": "输出模块入口列表，帮助学习者快速切换到目标知识点页面。",
    },
    {
        "name": "文本显示模块",
        "purpose": "演示文本、富文本、图标、头像和网络图片的组合用法。",
        "controls": "字体大小滑块、单行省略开关、网络图片展示区。",
        "state": "保存字体大小数值和是否启用省略号两项状态。",
        "flow": "用户拖动滑块或切换开关后，页面立即重建并更新文本显示效果。",
        "output": "输出可视化文本排版结果和图片加载兜底效果。",
    },
    {
        "name": "布局模块",
        "purpose": "演示 Flutter 常见布局方式及其空间分配机制。",
        "controls": "间距滑块、Row 示例区、Wrap 标签区、Stack 层叠区。",
        "state": "保存间距参数，用于联动多个布局展示区域。",
        "flow": "用户调整间距后，Row、Wrap 与 Stack 中的间距和定位同步变化。",
        "output": "输出布局结构变化结果，帮助理解横向、换行和层叠布局特性。",
    },
    {
        "name": "按钮交互模块",
        "purpose": "演示多种按钮组件及启用、禁用和点击反馈逻辑。",
        "controls": "多种按钮、启用开关、浮动操作按钮。",
        "state": "保存按钮启停状态和点击次数统计值。",
        "flow": "用户点击按钮后累计计数，关闭开关后所有按钮统一变为禁用。",
        "output": "输出按钮状态变化和点击统计结果。",
    },
    {
        "name": "表单输入模块",
        "purpose": "演示输入、选择、勾选、校验和提交流程。",
        "controls": "姓名输入框、城市下拉框、协议勾选框、提交按钮。",
        "state": "保存表单输入值、城市选项、勾选状态和提交结果文本。",
        "flow": "用户填写信息并提交后，系统执行校验、协议判断和结果提示。",
        "output": "输出表单校验结论、提交结果文字和 SnackBar 消息。",
    },
    {
        "name": "反馈提示模块",
        "purpose": "演示移动端常见的即时反馈和二次确认交互。",
        "controls": "SnackBar 按钮、Dialog 按钮、BottomSheet 按钮。",
        "state": "以一次性弹层结果为主，不长期保存复杂状态。",
        "flow": "用户点击不同按钮后，系统展示不同层级的反馈组件。",
        "output": "输出消息提示、确认对话框或底部操作面板。",
    },
    {
        "name": "导航模块",
        "purpose": "演示命名路由和匿名路由两种页面跳转方案。",
        "controls": "push 跳转按钮、pushNamed 跳转按钮、返回结果显示区。",
        "state": "保存导航结果文本，记录返回来源和时间。",
        "flow": "进入详情页后接收参数，点击返回按钮时将结果对象回传上级页面。",
        "output": "输出页面跳转效果和路由回传结果。",
    },
    {
        "name": "状态提升模块",
        "purpose": "演示父组件持有状态、子组件通过回调发起变更的模式。",
        "controls": "步长下拉框、增加按钮、减少按钮。",
        "state": "保存当前数值和步长，二者均由父组件统一管理。",
        "flow": "子组件触发 onAdd 或 onMinus 回调，由父组件更新值后重绘页面。",
        "output": "输出数值变化结果，帮助理解单向数据流。",
    },
    {
        "name": "主题模块",
        "purpose": "演示全局主题配置和浅色、深色模式切换。",
        "controls": "SegmentedButton 主题切换控件、主题预览卡片、主题按钮。",
        "state": "由根组件保存当前 ThemeMode，专题页负责发起切换动作。",
        "flow": "切换模式后，根组件刷新 MaterialApp 主题并联动所有子页面视觉风格。",
        "output": "输出浅色/深色主题切换后的界面预览效果。",
    },
    {
        "name": "异步列表模块",
        "purpose": "演示 FutureBuilder 的等待态、错误态和结果态。",
        "controls": "错误模拟开关、重新加载按钮、列表结果区。",
        "state": "保存 Future 对象和错误模拟标记。",
        "flow": "重新加载后等待异步结果返回，根据状态展示加载圈、错误文本或列表。",
        "output": "输出异步请求过程及最终列表数据。",
    },
    {
        "name": "硬件入口模块",
        "purpose": "统一组织定位、传感器、相机、文件与蓝牙五类示例。",
        "controls": "五个硬件示例卡片入口。",
        "state": "不保存复杂硬件状态，主要承担页面分发职责。",
        "flow": "用户按需进入具体硬件示例页面。",
        "output": "输出硬件学习目录，形成二级功能导航。",
    },
    {
        "name": "GPS 定位模块",
        "purpose": "演示系统定位服务检查、权限申请和定位结果读取。",
        "controls": "获取当前位置按钮、状态文本区。",
        "state": "保存定位结果文本，包括服务状态、权限状态和定位信息。",
        "flow": "点击按钮后依次检查定位服务、权限并尝试获取当前位置。",
        "output": "输出经纬度、精度或错误提示信息。",
    },
    {
        "name": "传感器模块",
        "purpose": "演示陀螺仪与加速度计事件流监听。",
        "controls": "开始监听按钮、停止监听按钮、实时数值显示区。",
        "state": "保存监听开关状态、陀螺仪数据和加速度计数据。",
        "flow": "开始监听后创建订阅，停止监听后释放订阅并保留最近一次结果。",
        "output": "输出实时变化的姿态与加速度数值。",
    },
    {
        "name": "相机模块",
        "purpose": "演示调起系统相机、获取照片路径和页面预览。",
        "controls": "打开相机拍照按钮、状态文本区、图片预览区。",
        "state": "保存拍照文件对象和状态文字。",
        "flow": "拍照成功后回传文件路径并在页面中预览；取消或失败则写入状态提示。",
        "output": "输出拍照结果和图像预览画面。",
    },
    {
        "name": "文件读取模块",
        "purpose": "演示选择本地文件并读取文本内容。",
        "controls": "选择并读取文件按钮、状态文本区、文本预览区。",
        "state": "保存当前状态文本和预览内容。",
        "flow": "选择文件后读取文本，成功则显示内容摘要，失败则显示异常。",
        "output": "输出文件路径和文本预览结果。",
    },
    {
        "name": "蓝牙模块",
        "purpose": "演示蓝牙开启、定时扫描和设备列表更新。",
        "controls": "蓝牙扫描按钮、状态文本、扫描结果列表。",
        "state": "保存扫描进行中标记、状态文本和 `ScanResult` 集合。",
        "flow": "启动扫描后订阅结果流，超时后自动结束并统计设备数量。",
        "output": "输出附近蓝牙设备名称、标识和 RSSI 强度。",
    },
]


def ensure_dirs() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    DIAGRAM_DIR.mkdir(parents=True, exist_ok=True)


def copy_screenshots() -> list[dict[str, str]]:
    copied: list[dict[str, str]] = []
    for item in SCREENSHOTS:
        src = TMP_SCREENSHOT_DIR / item["src"]
        dst = SCREENSHOT_DIR / item["dst"]
        if not src.exists():
            raise FileNotFoundError(f"未找到截图文件: {src}")
        shutil.copy2(src, dst)
        copied.append({**item, "path": str(dst.relative_to(ROOT)).replace("\\", "/")})
    return copied


def count_lines(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def build_source_stats() -> dict[str, int]:
    dart_lines = sum(count_lines(path) for path in ROOT.glob("lib/**/*.dart"))
    kotlin_lines = sum(count_lines(path) for path in ROOT.glob("android/app/src/main/kotlin/**/*.kt"))
    manifest_lines = count_lines(ROOT / "android" / "app" / "src" / "main" / "AndroidManifest.xml")
    gradle_lines = count_lines(ROOT / "android" / "app" / "build.gradle.kts")
    total = dart_lines + kotlin_lines + manifest_lines + gradle_lines
    return {
        "dart_lines": dart_lines,
        "kotlin_lines": kotlin_lines,
        "manifest_lines": manifest_lines,
        "gradle_lines": gradle_lines,
        "total_lines": total,
        "source_files": len(SOURCE_FILES),
    }


def build_tree(paths: list[str]) -> str:
    tree: dict[str, dict] = {}
    for raw_path in paths:
        parts = raw_path.replace("\\", "/").split("/")
        limited = parts[:3]
        current = tree
        for part in limited:
            current = current.setdefault(part, {})

    lines: list[str] = []

    def walk(node: dict[str, dict], prefix: str = "") -> None:
        items = list(node.items())
        for index, (name, child) in enumerate(items):
            connector = "└── " if index == len(items) - 1 else "├── "
            lines.append(f"{prefix}{connector}{name}")
            next_prefix = prefix + ("    " if index == len(items) - 1 else "│   ")
            walk(child, next_prefix)

    walk(tree)
    return "\n".join(lines)


def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def build_information_txt(stats: dict[str, int]) -> str:
    return dedent(
        f"""
        软件名称：{SOFTWARE_NAME}
        版本号：{SOFTWARE_VERSION}
        开发的硬件环境：Windows 开发工作站，操作系统为 {DEV_OS}，处理器为 {DEV_CPU}，物理内存约 {DEV_MEMORY}，配套安装 Android SDK、USB 调试环境与 Flutter 工具链，用于 Flutter 跨平台应用编码、调试、打包和真机联调。
        运行的硬件环境：Android 智能手机，真机截图采集设备为 {DEVICE_MODEL}，屏幕分辨率为 {DEVICE_RESOLUTION}，具备定位、加速度计、陀螺仪、蓝牙、相机和本地文件访问能力，可满足本软件演示移动端组件与硬件接口调用的运行要求。
        开发该软件的操作系统：{DEV_OS} 64 位。
        软件开发环境/开发工具：{FLUTTER_VERSION}、{DART_VERSION}、Android SDK、Gradle Kotlin DSL、ADB 真机调试工具、Kotlin 17 运行配置以及 Flutter 默认 Material 组件体系。
        该软件的运行平台/操作系统：Android 7.0 及以上版本移动终端，当前交付版本在 {DEVICE_OS} 真机环境完成运行验证；Android 安装包包名为 {PACKAGE_NAME}。
        软件运行支撑环境/支持软件：Flutter Framework、Dart Runtime、Android Framework、定位服务、蓝牙服务、相机服务、媒体文件访问能力以及各硬件插件对应的系统权限支持。
        编程语言：Dart、Kotlin、Gradle Kotlin DSL。
        源程序量：核心自研代码约 {stats["total_lines"]} 行，其中 Dart 代码约 {stats["dart_lines"]} 行、Kotlin 代码约 {stats["kotlin_lines"]} 行、Android Manifest 与构建配置约 {stats["manifest_lines"] + stats["gradle_lines"]} 行；以上统计不包含 Flutter SDK、第三方插件源码和构建产物。
        开发目的：本软件面向 Flutter 安卓移动应用开发学习场景，旨在通过一个可直接运行的移动端应用，将常见组件、页面组织方式、表单交互、异步数据处理、主题切换以及移动设备硬件能力接入等知识点集成到统一的教学型应用中，帮助学习者在真实 Android 终端上观察界面效果、理解页面状态变化并掌握常见插件的使用方法。
        面向行业/领域：移动应用开发教育、软件工程实践教学、Flutter 技术培训、移动端基础实验教学。
        软件的主要功能：本软件围绕“Flutter 安卓开发学习”这一主题构建完整的移动端演示流程。应用启动后首先进入首页模块列表，集中展示文本与显示组件学习、常见布局组件学习、按钮与点击交互学习、输入组件与表单学习、弹窗与提示反馈学习、导航与页面切换学习、状态更新与父子传值学习、主题样式学习、异步加载与列表展示学习以及硬件设备示例学习等多个功能入口。文本与显示模块用于演示普通文本、富文本、图标、头像、网络图片与失败兜底展示；布局模块用于演示 Row、Column、Expanded、Wrap、Stack 等布局方式；按钮交互模块展示不同按钮形态、启用/禁用切换和点击次数统计；表单模块提供姓名输入、城市选择、协议勾选和表单校验提交流程；反馈模块通过 SnackBar、对话框和底部弹层展示移动端常见交互反馈。导航模块实现 push、pushNamed、参数传递和页面结果回传；状态提升模块展示父组件保存状态、子组件回调更新的经典 Flutter 数据流模式；主题样式模块演示浅色与深色主题切换以及统一视觉样式管理；异步列表模块通过 FutureBuilder 模拟接口延迟、错误状态与刷新流程。硬件入口模块进一步整合 GPS 定位、陀螺仪与加速度计、相机拍照、本地文件读取和蓝牙扫描等示例页面，使学习者可以在一套应用中同时掌握界面组件与设备能力接入方式，形成较为完整的安卓移动应用开发学习闭环。
        软件的技术特点：本软件采用 Flutter 作为前端跨平台开发框架，整体结构以 MaterialApp 为根容器，通过首页列表对多个学习模块进行统一编排。页面层面大量使用 StatelessWidget、StatefulWidget、setState、WidgetBuilder、MaterialPageRoute 与命名路由等 Flutter 基础能力，形成清晰的页面导航和状态控制机制。应用内部通过统一的 DemoPageTemplate、SectionCard、CodeBlock 和 NetworkImageWithFallback 等组件实现页面模板复用，降低重复代码并提高展示一致性。异步模块采用 FutureBuilder 组织等待态、异常态和结果态；表单模块结合 GlobalKey<FormState>、TextEditingController 与 validator 机制完成表单验证；导航模块通过自定义 NavigationResult 对象回传结果；状态提升模块使用父子组件回调传值体现单向数据流思想。硬件能力方面，应用接入 geolocator、sensors_plus、image_picker、file_picker、flutter_blue_plus 等插件，分别完成定位、传感器、相机、文件读取与蓝牙扫描能力封装，并在 AndroidManifest 中声明定位、相机、蓝牙和媒体读取权限。Android 构建侧采用 Kotlin DSL 管理应用包名、版本号、最小支持版本和发布构建配置，当前版本号为 1.0.0，minSdk 为 24，targetSdk 为 36。整体技术路线突出“组件演示 + 页面交互 + 插件接入 + 真机验证”的特点，适合移动应用开发教学与实验演示使用。
        """
    )


def build_facts_md(stats: dict[str, int]) -> str:
    return dedent(
        f"""
        # 软著事实摘要

        ## 软件名称候选
        - {NAME_CANDIDATES[0]}（推荐）
        - {NAME_CANDIDATES[1]}
        - {NAME_CANDIDATES[2]}
        - {NAME_CANDIDATES[3]}
        - {NAME_CANDIDATES[4]}

        推荐名称说明：当前应用既覆盖 Flutter 基础组件教学，又明确以 Android 真机运行和移动端学习为交付形态，因此“{NAME_CANDIDATES[0]}”最能准确反映软件用途、实现技术和运行平台。

        ## 已核验事实
        - 项目类型：Flutter Android 移动应用，仓库目录同时包含 `android/`、`ios/`、`lib/` 等 Flutter 标准结构。
        - 应用标题：`{APP_TITLE}`。
        - Android 包名：`{PACKAGE_NAME}`。
        - 当前版本：`1.0.0`。
        - 运行真机：`{DEVICE_MODEL}`，系统 `{DEVICE_OS}`，分辨率 `{DEVICE_RESOLUTION}`。
        - 核心代码规模：约 {stats["total_lines"]} 行自研代码。
        - 页面模块：文本显示、布局、按钮交互、表单、反馈、导航、状态提升、主题、异步列表、硬件入口、GPS、传感器、相机、文件读取、蓝牙扫描。
        - 使用插件：`geolocator`、`sensors_plus`、`image_picker`、`file_picker`、`flutter_blue_plus`。
        - Android 权限：粗略定位、精确定位、相机、媒体图片读取、蓝牙、蓝牙管理、蓝牙扫描、蓝牙连接。
        - 构建方式：Flutter + Android Gradle Kotlin DSL + Kotlin Android 插件。

        ## 冲突与缺失
        - 仓库 README 仍为 Flutter 默认模板，未描述真实业务背景，本次软著说明以代码和真机截图事实为准。
        - Android `applicationId` 仍使用示例包名 `com.example.flutter_dudo`，可用于当前材料，但如后续正式发布建议替换为稳定产品包名。
        - 开发机 CPU、内存和操作系统已从当前环境提取；若登记主体要求填写更细的开发工具版本清单，可继续补充 IDE 版本信息。
        - GPS 页面截图已完成入口页采集，当前截图体现“定位按钮与结果区域”结构；若需要展示实时经纬度数值，可在后续人工触发定位后补采一张结果页。
        """
    )


def build_screenshot_md(copied: list[dict[str, str]]) -> str:
    lines = ["# 截图记录", "", f"采集日期：{BUILD_DATE}", f"采集设备：{DEVICE_MODEL} / {DEVICE_OS} / {DEVICE_RESOLUTION}", ""]
    for idx, item in enumerate(copied, start=1):
        lines.extend(
            [
                f"## {idx}. {item['title']}",
                f"- 文件：`{item['path']}`",
                f"- 进入路径：{item['entry']}",
                f"- 页面状态：{item['state']}",
                "",
            ]
        )
    return "\n".join(lines)


def build_design_md(stats: dict[str, int], copied: list[dict[str, str]]) -> str:
    shot = {item["dst"]: item for item in copied}
    lines = [
        f"# {SOFTWARE_NAME}{DESIGN_DOC_NAME}",
        "",
        "## 1 引言",
        "",
        "### 1.1 编写目的",
        f"本说明书用于描述 {SOFTWARE_NAME} 的整体结构、功能组成、页面设计、数据组织、接口接入方式以及运行部署方案，为软件著作权登记、后续版本维护与教学演示提供完整的技术文档依据。",
        "",
        "### 1.2 软件范围",
        "本软件是一套面向 Android 终端运行的 Flutter 学习型移动应用，通过统一首页组织多个实验模块，覆盖基础组件展示、交互处理、页面导航、状态管理、异步加载和硬件能力接入等内容。系统不依赖远程业务后端，重点体现移动端页面实现与设备能力调用。",
        "",
        "### 1.3 参考环境",
        f"- 开发环境：{DEV_OS}，{DEV_CPU}，内存约 {DEV_MEMORY}",
        f"- 开发工具：{FLUTTER_VERSION}，{DART_VERSION}，Android SDK，ADB",
        f"- 运行平台：{DEVICE_OS}，Android 7.0 及以上版本",
        f"- 应用包名：`{PACKAGE_NAME}`",
        f"- 版本号：`{SOFTWARE_VERSION}`",
        "",
        "## 2 需求分析",
        "",
        "### 2.1 建设目标",
        "系统建设目标是提供一套可直接安装到安卓真机中的 Flutter 学习应用，使学习者能够通过点击式交互观察各类组件的实际效果，并结合内置代码片段快速建立“知识点 - 页面结构 - 状态变化 - 设备能力”之间的映射关系。与单纯文档型教程相比，本软件更强调真机操作和可视化反馈。",
        "",
        "### 2.2 目标用户",
        "- Flutter 初学者：需要快速理解常见组件、页面跳转和状态管理方式。",
        "- 移动应用教学人员：需要一套可展示、可安装、可演示的课堂案例。",
        "- Android 实验学习人员：需要观察定位、传感器、相机、文件与蓝牙等接口的调用方式。",
        "",
        "### 2.3 功能需求",
        "软件应满足以下需求：一是提供统一首页作为模块导航入口；二是每个模块需要同时给出场景说明、可调参数提示、关键代码片段和运行效果区；三是支持文本显示、布局排版、按钮交互、表单输入、消息反馈、页面导航、状态提升、主题切换和异步列表等基础实验；四是支持 GPS、传感器、相机、文件读取与蓝牙扫描等硬件能力演示；五是支持 Android 真机安装运行，并在真实设备上完成页面展示与功能触发。",
        "",
        "### 2.4 非功能需求",
        "系统需要保证界面结构清晰、操作路径简单、真机运行稳定、权限申请符合 Android 平台规范、页面切换响应及时、代码结构易于阅读与二次扩展。同时，文档和演示内容要保持一致，便于教学与软著材料复用。",
        "",
        "## 3 系统概述",
        "",
        "### 3.1 系统定位",
        "本系统属于移动端教学演示软件，采用“首页导航 + 专题模块 + 硬件子模块”的结构组织学习内容。所有功能均以内置页面形式运行，适合作为 Flutter 基础到进阶能力的串联式学习工具。",
        "",
        "### 3.2 首页结构",
        "首页展示全部模块入口，用户可通过列表卡片进入任意学习专题。首页同时承担模块总览、知识点分发和统一跳转控制作用。",
        "",
        f"![{shot['4-2-home.png']['title']}](../assets/screenshots/4-2-home.png)",
        "",
        "图 4-2 页面展示了首页模块列表，卡片式入口使文本显示、布局、按钮、表单、导航、主题、异步加载和硬件学习等内容集中呈现，便于学习者按主题逐项操作。",
        "",
        "## 4 总体设计",
        "",
        "### 4.1 用例设计",
        "从使用过程看，用户首先打开应用并进入首页，然后根据学习目标选择具体模块，查看场景说明、阅读关键代码、观察运行效果，并可在部分模块中调整参数、触发跳转或调用硬件能力。",
        "",
        "![图4-1 系统功能用例图](../assets/diagrams/4-1-usecase.png)",
        "",
        "### 4.2 架构设计",
        "系统整体采用 Flutter 单端架构。应用启动后由 `main.dart` 进入根组件 `FlutterWidgetLabApp`，根组件负责初始化主题模式、MaterialApp 和命名路由。页面层通过 `HomePage` 统一组织模块入口，各学习页面复用 `DemoPageTemplate` 形成一致的说明区、代码区和运行区布局。硬件模块通过插件桥接 Android 原生能力，实现定位、传感器、相机、文件和蓝牙能力调用。",
        "",
        "![图5-1 系统架构图](../assets/diagrams/5-1-architecture.png)",
        "",
        "### 4.3 部署设计",
        "应用以 Android 安装包形式部署到移动终端。开发阶段在 Windows 主机上完成 Flutter 编译与 ADB 真机调试，运行阶段依赖 Android 系统服务和对应硬件权限。",
        "",
        "![图5-2 系统部署图](../assets/diagrams/5-2-deployment.png)",
        "",
        "### 4.4 模块划分",
        "系统功能按照教学内容划分为基础组件模块、交互模块、数据与状态模块、主题模块、异步模块和硬件模块六大类。其中：",
        "- 基础组件模块包括文本显示、布局演示和按钮交互。",
        "- 交互模块包括表单输入、消息反馈和导航跳转。",
        "- 数据与状态模块包括状态提升和异步列表。",
        "- 主题模块负责样式切换与统一视觉展示。",
        "- 硬件模块包括 GPS、传感器、相机、文件读取和蓝牙扫描五类示例。",
        "",
        "## 5 详细设计",
        "",
        "### 5.1 通用页面模板设计",
        "所有学习页面均基于 `DemoPageTemplate` 构建，模板分为四个层次：使用场景说明区、参数调整建议区、关键代码展示区和运行效果区。该设计使各模块拥有一致的信息组织方式，学习者可快速定位“为什么使用”“如何调整”“关键实现”和“实际效果”四类核心信息。",
        "",
        "### 5.2 表单输入模块设计",
        "表单输入页面使用 `Form`、`TextFormField`、`DropdownButtonFormField`、`CheckboxListTile` 和 `FilledButton` 组合构建。页面内部通过 `GlobalKey<FormState>` 管理校验状态，通过 `TextEditingController` 保存姓名字段值，并在提交按钮触发时完成校验、协议勾选判断、结果更新和 SnackBar 提示。",
        "",
        f"![{shot['6-2-form.png']['title']}](../assets/screenshots/6-2-form.png)",
        "",
        "该模块体现了 Flutter 表单类组件的常见使用模式，适用于登录、注册、资料录入和筛选条件填写等业务场景。",
        "",
        "### 5.3 导航模块设计",
        "导航模块通过两个按钮分别演示 `Navigator.push` 与 `Navigator.pushNamed`。页面状态中保存返回结果文本，子页面返回后立即更新展示结果。该设计直观体现了页面间的参数传递与结果回传机制。",
        "",
        f"![{shot['6-3-navigation.png']['title']}](../assets/screenshots/6-3-navigation.png)",
        "",
        "路由详情页面负责接收来自上级页面的字符串参数，并通过自定义结果对象将来源信息和时间戳返回给导航页面。",
        "",
        f"![{shot['6-4-route-detail.png']['title']}](../assets/screenshots/6-4-route-detail.png)",
        "",
        "页面跳转主流程如下图所示。",
        "",
        "![图6-1 页面跳转流程图](../assets/diagrams/6-1-flow.png)",
        "",
        "### 5.4 主题模块设计",
        "主题模块通过 `ThemeMode` 控制浅色和深色两套主题配置，由根组件统一持有当前模式。学习页面通过 `SegmentedButton` 发出模式切换动作，再由根组件更新 `MaterialApp` 的 `themeMode`，从而使整个应用在无需重建路由的情况下完成统一样式切换。",
        "",
        f"![{shot['6-5-theme.png']['title']}](../assets/screenshots/6-5-theme.png)",
        "",
        "该模块适合演示全局色彩、组件视觉一致性和亮暗模式适配策略。",
        "",
        "### 5.5 硬件能力入口设计",
        "硬件入口页面作为二级目录，集中列出 GPS、传感器、相机、文件和蓝牙五类能力模块。该页面自身不处理复杂业务逻辑，主要承担硬件示例分发、页面跳转和学习路径组织的职责。",
        "",
        f"![{shot['6-6-hardware-hub.png']['title']}](../assets/screenshots/6-6-hardware-hub.png)",
        "",
        "### 5.6 GPS 定位模块设计",
        "GPS 模块首先检查系统定位服务是否开启，然后校验并申请定位权限，最后调用 `Geolocator.getCurrentPosition` 读取位置信息。若系统定位未开启或权限被拒绝，则页面会通过状态文本提示用户进行处理。该设计覆盖了移动端定位调用中“服务可用性检查、权限检查、位置读取、异常提示”四个关键环节。",
        "",
        f"![{shot['6-7-gps.png']['title']}](../assets/screenshots/6-7-gps.png)",
        "",
        "### 5.7 传感器模块设计",
        "传感器模块分别订阅陀螺仪和加速度计事件流，并将最新值实时渲染到界面中。页面提供“开始监听”和“停止监听”两个按钮，对应启动和取消 `StreamSubscription`。这一设计体现了 Flutter 中基于流的异步硬件数据监听模式。",
        "",
        f"![{shot['6-8-sensor.png']['title']}](../assets/screenshots/6-8-sensor.png)",
        "",
        "运行结果页面在监听开始后持续刷新角速度与加速度数值，便于学习者观察真实设备姿态变化。",
        "",
        "### 5.8 相机模块设计",
        "相机模块通过 `image_picker` 调起系统相机，完成拍照后回传图片路径，并在页面中使用 `Image.file` 预览拍摄结果。若用户取消拍照或调用失败，页面会使用状态字符串给出结果反馈。这一模块适合扩展为头像上传、现场取证、工单拍照等移动端业务。",
        "",
        "### 5.9 文件读取模块设计",
        "文件模块通过 `file_picker` 选择本地 `txt`、`json`、`md` 文件，再通过 Dart 文件 API 读取文本内容，并在页面中展示截断后的预览结果。模块逻辑覆盖“文件选择、路径校验、文本读取、结果展示和异常处理”完整流程。",
        "",
        "### 5.10 蓝牙模块设计",
        "蓝牙模块调用 `flutter_blue_plus` 开启蓝牙并执行定时扫描，将扫描得到的 `ScanResult` 集合实时更新到页面列表中。模块输出包含设备名称、设备标识和 RSSI 信号强度，可作为连接外设、设备发现和近场通信实验的基础。",
        "",
        "### 5.11 其他基础模块设计",
        "文本显示模块主要演示 `Text`、`RichText`、图标、头像和网络图片异常兜底；布局模块重点展示 `Row`、`Expanded`、`Wrap`、`Stack` 的组合用法；按钮模块演示 `ElevatedButton`、`OutlinedButton`、`TextButton`、`IconButton` 与 `FilledButton` 的差异化交互；反馈模块用于演示 `SnackBar`、`AlertDialog` 和 `BottomSheet` 三类反馈组件；状态提升模块通过父子组件回调传值演示单向数据流；异步列表模块通过 `FutureBuilder` 演示等待态、错误态和结果态切换。上述模块共同构成从组件基础到页面交互的完整学习链路。",
        "",
        "## 6 数据设计",
        "",
        "### 6.1 状态数据设计",
        "本系统不依赖外部数据库，数据设计以页面内状态对象和插件返回数据为主。核心状态包括：",
        "- 主题状态：`ThemeMode`，用于控制浅色与深色主题。",
        "- 表单状态：姓名字符串、城市选项、协议勾选值、提交结果文本。",
        "- 导航状态：路由参数字符串与 `NavigationResult` 返回对象。",
        "- 异步状态：Future 列表对象、错误模拟开关。",
        "- 硬件状态：定位结果文本、传感器当前值、照片文件路径、文件预览文本、蓝牙扫描结果集合。",
        "",
        "### 6.2 数据结构设计",
        "系统采用轻量级本地状态存储方式，通过 `StatefulWidget` 成员变量、控制器对象和事件回调保存运行态数据。导航模块引入 `NavigationResult` 作为返回数据模型，用于规范来源和时间信息的传递结构。",
        "",
        "### 6.3 类关系设计",
        "页面组件、模板组件和结果模型之间的关系如下图所示。",
        "",
        "![图7-1 核心类关系图](../assets/diagrams/7-1-classes.png)",
        "",
        "## 7 接口设计",
        "",
        "### 7.1 页面内部接口",
        "- `onThemeModeChanged(ThemeMode mode)`：主题页面通知根组件切换主题模式。",
        "- `onAdd()` / `onMinus()`：状态提升模块中子组件通知父组件变更数值。",
        "- `Navigator.push` / `Navigator.pushNamed`：负责页面间路由跳转。",
        "- `Navigator.pop(result)`：负责从详情页回传处理结果。",
        "",
        "### 7.2 插件接口",
        "- `Geolocator.isLocationServiceEnabled`、`Geolocator.checkPermission`、`Geolocator.getCurrentPosition`：定位能力接口。",
        "- `gyroscopeEvents.listen`、`accelerometerEvents.listen`：传感器流接口。",
        "- `ImagePicker().pickImage`：相机采集接口。",
        "- `FilePicker.platform.pickFiles`：本地文件选择接口。",
        "- `FlutterBluePlus.startScan`、`FlutterBluePlus.scanResults.listen`：蓝牙扫描接口。",
        "",
        "### 7.3 Android 权限接口",
        "系统在 Android Manifest 中声明了精确定位、粗略定位、相机、媒体图片读取、蓝牙扫描、蓝牙连接和蓝牙基础管理权限。运行时由对应插件根据需要触发权限检查和申请，确保功能调用符合 Android 权限模型。",
        "",
        "## 8 运行与部署设计",
        "",
        "### 8.1 构建方式",
        f"项目采用 Flutter 标准目录结构，Android 侧通过 `build.gradle.kts` 管理应用构建。应用包名为 `{PACKAGE_NAME}`，版本号为 `1.0.0`，最低支持版本 `minSdk=24`，目标版本 `targetSdk=36`。",
        "",
        "### 8.2 真机运行方式",
        f"开发阶段通过 ADB 连接 Android 真机，执行安装、启动和截图采集。当前软著截图于 {BUILD_DATE} 在 `{DEVICE_MODEL}` 真机上完成，验证了应用首页、表单、导航、主题、硬件入口、GPS 与传感器等关键页面。",
        "",
        "### 8.3 部署特点",
        "系统以单机应用方式部署，不依赖独立服务器、不依赖数据库服务，也不要求额外中间件。教学内容全部封装在移动端内部，便于离线展示和课堂安装演示。",
        "",
        "## 9 安全与权限设计",
        "",
        "系统的安全设计重点在于运行时权限控制和异常提示。定位、蓝牙、相机和媒体访问均依赖 Android 权限声明；若用户拒绝授权或系统服务未开启，页面通过状态文本进行提示，避免无反馈失败。由于本系统未内置账号体系、远程登录和网络数据上传逻辑，因此不存在账户口令、数据库连接和外部接口凭据等高风险数据暴露问题。系统对外部资源访问主要限于网络图片示例和本机硬件能力调用，整体风险面较小。",
        "",
        "## 10 测试与验证",
        "",
        "### 10.1 功能验证方式",
        "软件采用“代码检查 + 真机运行 + 页面截图留档”的方式验证。当前已核验的页面包括首页、表单、导航、路由详情、主题、硬件入口、GPS 页面和传感器页面，其中传感器页面已采集到实时变化数据。",
        "",
        "### 10.2 关键验证结论",
        "- 应用可在 Android 真机成功安装并启动。",
        "- 首页可进入各学习模块。",
        "- 表单页面可展示输入组件和提交流程。",
        "- 导航页面与详情页可完成参数传递和结果回传。",
        "- 主题页面可展示主题切换控件和预览卡片。",
        "- 硬件入口页可进入 GPS 与传感器示例页面。",
        "- GPS 页面已验证权限与入口结构，适合作为定位能力教学界面。",
        "- 传感器页面已验证监听启动和实时数据显示能力。",
        "",
        "### 10.3 截图设备信息",
        f"- 设备型号：{DEVICE_MODEL}",
        f"- 系统版本：{DEVICE_OS}",
        f"- 屏幕分辨率：{DEVICE_RESOLUTION}",
        f"- 截图日期：{BUILD_DATE}",
        "",
        "## 11 结论",
        "",
        f"{SOFTWARE_NAME} 以 Flutter 为核心开发框架，将移动端基础组件、典型交互模式和常见硬件能力接入集中整合为一套可运行、可演示、可教学的安卓学习应用。系统结构清晰、模块边界明确、页面逻辑完整，既适合作为 Flutter 初学者实验手册，也适合作为移动应用教学和演示型软件进行交付。",
        "",
        "## 12 附录",
        "",
        "### 12.1 目录结构摘要",
        "",
        "```text",
        build_tree([file.path for file in SOURCE_FILES]),
        "```",
        "",
        "### 12.2 截图索引",
        "- 图4-2：首页模块列表",
        "- 图6-2：表单输入与校验页面",
        "- 图6-3：页面导航与返回结果页面",
        "- 图6-4：路由详情结果页面",
        "- 图6-5：主题样式切换页面",
        "- 图6-6：硬件能力学习入口页面",
        "- 图6-7：GPS 定位示例页面",
        "- 图6-8：传感器监听示例页面",
        "",
        "### 12.3 代码规模说明",
        f"当前纳入软著整理的核心自研代码共 {stats['source_files']} 个主要文件，累计约 {stats['total_lines']} 行，能够完整覆盖应用结构、页面逻辑、交互流程和 Android 运行配置。",
        "",
        "### 12.4 页面级详细设计附录",
        "",
    ]

    for index, item in enumerate(MODULE_DETAILS, start=1):
        lines.extend(
            [
                f"#### 12.4.{index} {item['name']}",
                "",
                f"{item['name']}的设计目的在于{item['purpose']} 页面主要控件包括{item['controls']}。运行过程中主要状态为{item['state']}。典型业务流程为：{item['flow']}。模块最终向学习者{item['output']}。",
                "",
            ]
        )

    lines.extend(
        [
            "### 12.5 权限与插件映射附录",
            "",
            "- 定位权限：`ACCESS_FINE_LOCATION` 与 `ACCESS_COARSE_LOCATION`，对应 `geolocator` 插件，用于检查服务状态、申请权限并获取经纬度信息。",
            "- 蓝牙权限：`BLUETOOTH`、`BLUETOOTH_ADMIN`、`BLUETOOTH_SCAN`、`BLUETOOTH_CONNECT`，对应 `flutter_blue_plus` 插件，用于蓝牙开启、扫描和设备信息展示。",
            "- 相机权限：`CAMERA`，对应 `image_picker` 插件，用于调起系统相机拍照。",
            "- 媒体读取权限：`READ_MEDIA_IMAGES`，用于 Android 端图片资源读取和相机结果回传场景。",
            "- 传感器能力：由 `sensors_plus` 通过系统传感器服务提供支持，不额外声明危险权限，但依赖终端硬件存在陀螺仪和加速度计。",
            "- 文件读取能力：由 `file_picker` 调用系统文件选择器实现，主要依赖系统文档访问能力。",
            "",
        ]
    )

    return "\n".join(lines)


def build_source_md(stats: dict[str, int]) -> str:
    lines = [
        f"# {SOURCE_DOC_NAME}",
        "",
        "## 1 封面信息",
        "",
        f"- 软件名称：{SOFTWARE_NAME}",
        f"- 版本号：{SOFTWARE_VERSION}",
        f"- 应用标题：{APP_TITLE}",
        f"- Android 包名：`{PACKAGE_NAME}`",
        f"- 代码规模：约 {stats['total_lines']} 行自研代码",
        "",
        "## 2 源代码属性结构说明",
        "",
        f"- 技术栈：Flutter、Dart、Kotlin、Android Gradle Kotlin DSL",
        f"- 源码根目录：`{ROOT}`",
        "- 一级目录划分：`android/` 用于 Android 构建与权限声明，`lib/` 用于 Flutter 页面与组件实现，`docs/` 用于软著材料输出。",
        "- 二级目录划分：`lib/pages/` 承载页面模块，`lib/widgets/` 承载通用组件，`lib/pages/hardware/` 承载设备能力示例。",
        "- 三级目录划分：`lib/pages/navigation/` 存放导航结果模型与详情页，`android/app/src/main/` 存放 Android 主配置。",
        "- 选入范围说明：纳入应用配置、Flutter 页面、通用组件、Android 权限清单和启动入口，不纳入第三方依赖、构建缓存和生成产物。",
        "",
        "## 3 三级目录结构树",
        "",
        "```text",
        build_tree([file.path for file in SOURCE_FILES]),
        "```",
        "",
        "## 4 按目录顺序整理的源代码",
        "",
    ]

    for index, source in enumerate(SOURCE_FILES, start=1):
        path = ROOT / source.path
        content = path.read_text(encoding="utf-8").rstrip()
        ext = path.suffix.lstrip(".") or "text"
        rel_path = source.path.replace("\\", "/")
        lines.extend(
            [
                f"### 4.{index} {rel_path}",
                "",
                f"文件路径：`{rel_path}`",
                "",
                f"文件作用：{source.purpose}",
                "",
                f"所属模块：{source.module}",
                "",
                f"```{ext}",
                content,
                "```",
                "",
            ]
        )

    return "\n".join(lines)


def register_fonts() -> tuple[str, str]:
    regular = "SCRegular"
    bold = "SCBold"
    try:
        pdfmetrics.registerFont(TTFont(regular, r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
        pdfmetrics.registerFont(TTFont(bold, r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))
        return regular, bold
    except Exception:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        return "STSong-Light", "STSong-Light"


def build_styles(body_font: str, bold_font: str, compact: bool) -> dict[str, ParagraphStyle]:
    styles = getSampleStyleSheet()
    body_size = 10 if compact else 11.2
    body_leading = 15 if compact else 18
    code_size = 7.5 if compact else 8.5
    code_leading = 9.2 if compact else 10.5
    return {
        "title": ParagraphStyle(
            "title",
            parent=styles["Heading1"],
            fontName=bold_font,
            fontSize=18,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "h1": ParagraphStyle(
            "h1",
            parent=styles["Heading1"],
            fontName=bold_font,
            fontSize=16,
            leading=22,
            spaceBefore=8,
            spaceAfter=6,
            wordWrap="CJK",
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=styles["Heading2"],
            fontName=bold_font,
            fontSize=13,
            leading=18,
            spaceBefore=6,
            spaceAfter=4,
            wordWrap="CJK",
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=styles["Heading3"],
            fontName=bold_font,
            fontSize=11.5,
            leading=16,
            spaceBefore=4,
            spaceAfter=3,
            wordWrap="CJK",
        ),
        "body": ParagraphStyle(
            "body",
            parent=styles["BodyText"],
            fontName=body_font,
            fontSize=body_size,
            leading=body_leading,
            alignment=TA_LEFT,
            spaceAfter=3,
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "bullet",
            parent=styles["BodyText"],
            fontName=body_font,
            fontSize=body_size,
            leading=body_leading,
            leftIndent=14,
            firstLineIndent=-8,
            spaceAfter=2,
            wordWrap="CJK",
        ),
        "caption": ParagraphStyle(
            "caption",
            parent=styles["BodyText"],
            fontName=body_font,
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=8,
            wordWrap="CJK",
        ),
        "code": ParagraphStyle(
            "code",
            parent=styles["Code"],
            fontName=body_font,
            fontSize=code_size,
            leading=code_leading,
            leftIndent=4,
            rightIndent=4,
            borderPadding=6,
            backColor=colors.HexColor("#F3F5F7"),
        ),
    }


def markdown_to_story(md_path: Path, styles: dict[str, ParagraphStyle], compact: bool) -> list:
    story: list = []
    lines = md_path.read_text(encoding="utf-8").splitlines()
    buffer: list[str] = []
    code_buffer: list[str] = []
    in_code = False
    title_used = False

    def flush_paragraph() -> None:
        nonlocal buffer
        if not buffer:
            return
        text = escape(" ".join(line.strip() for line in buffer).strip())
        if text:
            story.append(Paragraph(text, styles["body"]))
        buffer = []

    for line in lines:
        stripped = line.rstrip()
        normalized = stripped.lstrip()
        if stripped.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Preformatted("\n".join(code_buffer), styles["code"]))
                story.append(Spacer(1, 4))
                code_buffer = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_buffer.append(stripped)
            continue

        if not stripped:
            flush_paragraph()
            story.append(Spacer(1, 4))
            continue

        image_match = re.match(r"!\[(.*?)\]\((.*?)\)", normalized)
        if image_match:
            flush_paragraph()
            caption, raw_path = image_match.groups()
            image_path = (md_path.parent / raw_path).resolve()
            img = RLImage(str(image_path))
            max_width = 170 * mm if compact else 180 * mm
            max_height = 190 * mm if compact else 205 * mm
            scale = min(max_width / img.imageWidth, max_height / img.imageHeight, 1)
            img.drawWidth = img.imageWidth * scale
            img.drawHeight = img.imageHeight * scale
            story.append(img)
            story.append(Paragraph(escape(caption), styles["caption"]))
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)", normalized)
        if heading_match:
            flush_paragraph()
            level = len(heading_match.group(1))
            text = escape(heading_match.group(2).strip())
            if level == 1 and not title_used:
                story.append(Paragraph(text, styles["title"]))
                title_used = True
            elif level == 1:
                story.append(Paragraph(text, styles["h1"]))
            elif level == 2:
                story.append(Paragraph(text, styles["h2"]))
            else:
                story.append(Paragraph(text, styles["h3"]))
            continue

        if normalized.startswith("- "):
            flush_paragraph()
            story.append(Paragraph(escape("• " + normalized[2:].strip()), styles["bullet"]))
            continue

        buffer.append(normalized)

    flush_paragraph()
    if code_buffer:
        story.append(Preformatted("\n".join(code_buffer), styles["code"]))
    return story


def render_pdf(md_path: Path, pdf_path: Path, compact: bool) -> int:
    body_font, bold_font = register_fonts()
    styles = build_styles(body_font, bold_font, compact)
    story = markdown_to_story(md_path, styles, compact)

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=14 * mm,
        title=md_path.stem,
        author="Codex",
    )

    def add_header_footer(canvas, _doc) -> None:
        canvas.saveState()
        canvas.setFont(body_font, 9)
        canvas.drawString(doc.leftMargin, A4[1] - 10 * mm, f"{SOFTWARE_NAME} {SOFTWARE_VERSION}")
        canvas.drawRightString(A4[0] - doc.rightMargin, 8 * mm, f"第 {canvas.getPageNumber()} 页")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    return len(PdfReader(str(pdf_path)).pages)


def crop_pdf_if_needed(pdf_path: Path) -> tuple[int, Path | None]:
    reader = PdfReader(str(pdf_path))
    page_count = len(reader.pages)
    if page_count <= 60:
        return page_count, None

    full_backup = pdf_path.with_name(pdf_path.stem + ".full.pdf")
    shutil.copy2(pdf_path, full_backup)

    writer = PdfWriter()
    for page in reader.pages[:30]:
        writer.add_page(page)
    for page in reader.pages[-30:]:
        writer.add_page(page)
    with pdf_path.open("wb") as handle:
        writer.write(handle)
    return len(writer.pages), full_backup


def archive_outputs(pdf_paths: list[Path], copied: list[dict[str, str]], info_path: Path) -> None:
    target_root = ARCHIVE_ROOT / SOFTWARE_NAME
    pdf_dir = target_root / "pdf"
    text_dir = target_root / "text"
    diagram_dir = target_root / "images" / "diagrams"
    shot_dir = target_root / "images" / "screenshots"
    for directory in (pdf_dir, text_dir, diagram_dir, shot_dir):
        directory.mkdir(parents=True, exist_ok=True)

    for pdf_path in pdf_paths:
        shutil.copy2(pdf_path, pdf_dir / pdf_path.name)
        full_backup = pdf_path.with_name(pdf_path.stem + ".full.pdf")
        if full_backup.exists():
            shutil.copy2(full_backup, pdf_dir / full_backup.name)

    shutil.copy2(info_path, text_dir / info_path.name)

    for item in copied:
        shutil.copy2(ROOT / item["path"], shot_dir / Path(item["path"]).name)

    for image in DIAGRAM_DIR.glob("*.*"):
        shutil.copy2(image, diagram_dir / image.name)


def main() -> None:
    ensure_dirs()
    copied = copy_screenshots()
    stats = build_source_stats()

    info_path = DOCS_DIR / "information.txt"
    facts_path = DOCS_DIR / "facts.md"
    shot_path = DOCS_DIR / "截图记录.md"
    design_md_path = DOCS_DIR / f"{SOFTWARE_NAME}{DESIGN_DOC_NAME}.md"
    source_md_path = DOCS_DIR / f"{SOURCE_DOC_NAME}.md"

    write_text(info_path, build_information_txt(stats))
    write_text(facts_path, build_facts_md(stats))
    write_text(shot_path, build_screenshot_md(copied))
    write_text(design_md_path, build_design_md(stats, copied))
    write_text(source_md_path, build_source_md(stats))

    design_pdf_path = DOCS_DIR / f"{SOFTWARE_NAME}{DESIGN_DOC_NAME}.pdf"
    source_pdf_path = DOCS_DIR / f"{SOURCE_DOC_NAME}.pdf"

    design_pages = render_pdf(design_md_path, design_pdf_path, compact=False)
    source_pages = render_pdf(source_md_path, source_pdf_path, compact=True)
    design_pages, _ = crop_pdf_if_needed(design_pdf_path)
    source_pages, _ = crop_pdf_if_needed(source_pdf_path)

    archive_outputs([design_pdf_path, source_pdf_path], copied, info_path)

    print(f"software_name={SOFTWARE_NAME}")
    print(f"design_pdf={design_pdf_path}")
    print(f"design_pages={design_pages}")
    print(f"source_pdf={source_pdf_path}")
    print(f"source_pages={source_pages}")
    print(f"archive_root={ARCHIVE_ROOT / SOFTWARE_NAME}")


if __name__ == "__main__":
    main()
