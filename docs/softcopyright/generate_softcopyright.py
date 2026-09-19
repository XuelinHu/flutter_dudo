from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
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
from reportlab.platypus import Image as RLImage
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / "docs" / "softcopyright"
ASSET_DIR = ROOT / "docs" / "assets"
DIAGRAM_DIR = ASSET_DIR / "diagrams"
SCREENSHOT_DIR = ASSET_DIR / "screenshots"
ARCHIVE_ROOT = Path(r"D:\软著")

SOFTWARE_NAME = "基于Flutter的安卓开发学习移动应用软件"
SOFTWARE_VERSION = "V1.0.0"
APP_TITLE = "Flutter组件实验手册"
PACKAGE_NAME = "com.example.flutter_dudo"
BUILD_DATE = "2026-05-13"
DEVICE_MODEL = "OPPO PKS110"
DEVICE_OS = "Android 16"
DEVICE_RESOLUTION = "1080x2412"
FLUTTER_VERSION = "Flutter 3.41.6"
DART_VERSION = "Dart 3.11.4"
DEV_OS = "Microsoft Windows 10 家庭版"
DEV_CPU = "Intel(R) Core(TM) Ultra 9 285H"
DEV_MEMORY = "31.5GB"

SOURCE_DOC_NAME = f"{SOFTWARE_NAME}源代码"
DESIGN_DOC_NAME = f"{SOFTWARE_NAME}软件设计说明书"


@dataclass(frozen=True)
class SourceFile:
    path: str
    module: str
    purpose: str


@dataclass(frozen=True)
class AssetItem:
    file: str
    title: str
    description: str


SOURCE_FILES = [
    SourceFile("pubspec.yaml", "项目配置", "定义应用名称、版本、Flutter SDK 约束和硬件能力相关插件依赖。"),
    SourceFile("android/app/build.gradle.kts", "Android 构建配置", "配置 Android 命名空间、包名、版本、Java/Kotlin 编译目标和构建类型。"),
    SourceFile("android/app/src/main/AndroidManifest.xml", "Android 权限配置", "声明定位、相机、媒体读取、蓝牙扫描与连接权限，并配置主入口 Activity。"),
    SourceFile("android/app/src/main/kotlin/com/example/flutter_dudo/MainActivity.kt", "Android 启动入口", "提供 FlutterActivity 宿主入口。"),
    SourceFile("lib/main.dart", "应用入口", "初始化 Flutter 绑定并启动根组件。"),
    SourceFile("lib/app.dart", "根应用", "配置 MaterialApp、主题模式、命名路由和首页挂载。"),
    SourceFile("lib/pages/home_page.dart", "首页模块", "展示学习模块列表并进入各功能页面。"),
    SourceFile("lib/pages/text_display_page.dart", "基础展示模块", "演示文本、富文本、图标、图片和参数联动显示。"),
    SourceFile("lib/pages/layout_widgets_page.dart", "布局模块", "演示 Row、Expanded、Wrap、Stack 等常见布局组件。"),
    SourceFile("lib/pages/button_interaction_page.dart", "按钮交互模块", "演示按钮状态、禁用控制和点击计数。"),
    SourceFile("lib/pages/form_input_page.dart", "表单输入模块", "演示 TextField、下拉选择、协议勾选、校验和提交反馈。"),
    SourceFile("lib/pages/feedback_page.dart", "反馈提示模块", "演示 SnackBar、Dialog 和 BottomSheet 反馈场景。"),
    SourceFile("lib/pages/navigation_page.dart", "页面导航模块", "演示 Navigator.push、pushNamed 与结果回传。"),
    SourceFile("lib/pages/navigation/route_detail_page.dart", "路由详情模块", "接收页面参数并向上级页面返回处理结果。"),
    SourceFile("lib/pages/navigation/navigation_result.dart", "导航结果模型", "定义导航返回数据结构。"),
    SourceFile("lib/pages/state_lifting_page.dart", "状态提升模块", "演示父组件统一管理状态、子组件通过回调触发变更。"),
    SourceFile("lib/pages/theme_page.dart", "主题样式模块", "演示浅色、深色和系统主题模式切换。"),
    SourceFile("lib/pages/async_list_page.dart", "异步列表模块", "演示 FutureBuilder 的等待、错误和结果状态。"),
    SourceFile("lib/pages/hardware_hub_page.dart", "硬件入口模块", "集中组织定位、传感器、相机、文件读取和蓝牙能力入口。"),
    SourceFile("lib/pages/hardware/gps_demo_page.dart", "定位能力模块", "封装定位服务检查、权限申请和经纬度读取逻辑。"),
    SourceFile("lib/pages/hardware/sensor_demo_page.dart", "传感器能力模块", "订阅陀螺仪和加速度计数据流并实时刷新界面。"),
    SourceFile("lib/pages/hardware/camera_demo_page.dart", "相机能力模块", "调用系统相机并回显拍照结果。"),
    SourceFile("lib/pages/hardware/file_read_demo_page.dart", "文件读取模块", "选择本地文件并预览文本内容。"),
    SourceFile("lib/pages/hardware/bluetooth_demo_page.dart", "蓝牙能力模块", "控制蓝牙扫描并展示附近设备列表。"),
    SourceFile("lib/widgets/demo_page_template.dart", "页面模板组件", "统一演示页面的场景说明、代码区和效果区布局。"),
    SourceFile("lib/widgets/section_card.dart", "通用分区组件", "承载模块页面中的分区内容。"),
    SourceFile("lib/widgets/code_block.dart", "代码展示组件", "展示示例代码片段。"),
    SourceFile("lib/widgets/network_image_with_fallback.dart", "图片兜底组件", "加载网络图片并在异常时提供本地图标兜底。"),
]

SCREENSHOTS = [
    AssetItem("4-2-home.png", "图4-2 系统首页模块列表", "应用启动后进入首页，展示基础展示、布局、按钮、表单、反馈、导航、状态、主题、异步列表和硬件能力等学习模块入口。"),
    AssetItem("6-2-form.png", "图6-2 表单输入与校验页面", "表单页面展示姓名输入、城市选择、协议勾选和提交校验区域，用于说明移动端表单采集与即时反馈流程。"),
    AssetItem("6-3-navigation.png", "图6-3 页面导航与返回结果页面", "导航页面展示普通路由和命名路由两种跳转入口，并保留返回结果显示区域。"),
    AssetItem("6-4-route-detail.png", "图6-4 路由详情结果页面", "路由详情页面接收上级页面传入的参数，并通过返回按钮向上级页面回传处理结果。"),
    AssetItem("6-5-theme.png", "图6-5 主题样式切换页面", "主题页面提供浅色、深色和跟随系统的主题切换控件，并展示主题预览卡片。"),
    AssetItem("6-6-hardware-hub.png", "图6-6 硬件能力学习入口页面", "硬件入口页面集中展示 GPS、传感器、相机、文件读取和蓝牙扫描五类能力的学习入口。"),
    AssetItem("6-7-gps.png", "图6-7 GPS 定位示例页面", "定位页面展示权限检查、定位按钮、示例代码和定位结果区域，用于说明位置能力的调用流程。"),
    AssetItem("6-8-sensor.png", "图6-8 传感器监听示例页面", "传感器页面展示监听开关、陀螺仪数据、加速度数据和实时刷新区域，用于说明设备传感器数据流。"),
]

DIAGRAMS = [
    AssetItem("4-1-usecase.png", "图4-1 系统用例图", "用例图展示学习者与页面学习、组件交互、硬件能力演示和主题切换等核心用例之间的关系。"),
    AssetItem("5-1-architecture.png", "图5-1 系统架构图", "架构图展示 Flutter 表现层、页面模块层、通用组件层、插件能力层和 Android 运行环境之间的层次关系。"),
    AssetItem("5-2-deployment.png", "图5-2 部署结构图", "部署图展示开发机、Flutter 构建工具、Android 安装包和 Android 真机运行环境之间的交付关系。"),
    AssetItem("6-1-flow.png", "图6-1 功能流程图", "流程图展示用户从首页进入具体学习模块、执行交互操作、查看反馈和返回首页的主流程。"),
    AssetItem("7-1-classes.png", "图7-1 主要类关系图", "类关系图展示根应用、首页、演示页面、路由详情页、硬件子页面和通用组件之间的依赖关系。"),
]

MODULE_DETAILS = [
    ("首页模块", "提供学习模块导航入口", "模块列表、图标、标题、副标题、进入按钮", "点击条目后进入对应专题页面", "页面不保存复杂业务状态，仅承担路由分发职责"),
    ("文本显示模块", "展示文本、富文本、图标和网络图片", "字体大小滑块、省略开关、图片区域", "调整参数后实时刷新显示效果", "保存字体大小和是否省略两类界面状态"),
    ("布局模块", "展示常见布局和空间分配方式", "Row、Expanded、Wrap、Stack、间距滑块", "调整间距后联动多个布局区域", "保存布局间距参数"),
    ("按钮交互模块", "展示按钮启停和点击反馈", "多类按钮、启用开关、计数器", "点击按钮后更新计数，关闭开关后按钮禁用", "保存按钮启停状态和点击次数"),
    ("表单输入模块", "展示移动端表单采集和校验", "输入框、下拉框、复选框、提交按钮", "提交时校验输入、协议和选项并展示结果", "保存输入值、城市、协议状态和提交提示"),
    ("反馈提示模块", "展示轻量提示和确认交互", "SnackBar、Dialog、BottomSheet", "点击不同按钮弹出不同层级的反馈组件", "反馈组件为一次性状态"),
    ("导航模块", "展示匿名路由和命名路由跳转", "push 按钮、pushNamed 按钮、返回结果区", "详情页接收参数并返回结果对象", "保存最近一次导航结果"),
    ("状态提升模块", "展示父子组件状态协同", "步长选择、增加按钮、减少按钮", "子组件触发回调，父组件更新值并重建页面", "由父组件保存数值和步长"),
    ("主题样式模块", "展示全局主题模式切换", "分段控件、主题预览卡片", "切换后根组件刷新 MaterialApp 主题", "根组件保存 ThemeMode"),
    ("异步列表模块", "展示 FutureBuilder 异步加载过程", "错误模拟开关、重新加载按钮、结果列表", "重新加载后按等待、错误或成功状态展示内容", "保存 Future 对象和错误模拟标记"),
    ("硬件入口模块", "集中组织设备能力示例入口", "GPS、传感器、相机、文件读取、蓝牙卡片", "点击进入具体硬件能力页面", "不保存硬件状态"),
    ("GPS 定位模块", "展示定位服务和权限调用", "获取位置按钮、状态文本、结果区域", "检查服务、申请权限、读取坐标并展示结果", "保存定位状态、权限结论和位置信息"),
    ("传感器模块", "展示陀螺仪和加速度计数据流", "开始监听、停止监听、实时数据区", "订阅传感器流并在停止时释放订阅", "保存监听状态和最近一次传感器数据"),
    ("相机模块", "展示系统相机调用和结果预览", "拍照按钮、状态文本、图片预览", "调用系统相机，成功后回显照片结果", "保存拍照文件和状态文本"),
    ("文件读取模块", "展示本地文件选择和文本预览", "选择文件按钮、状态文本、文本预览区", "读取文本文件并展示内容摘要", "保存当前文件路径和预览内容"),
    ("蓝牙模块", "展示蓝牙扫描和设备列表", "扫描按钮、状态文本、结果列表", "启动扫描并在超时后汇总设备", "保存扫描状态、状态文本和设备集合"),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_stats() -> dict[str, int]:
    total = 0
    existing = 0
    for item in SOURCE_FILES:
        path = ROOT / item.path
        if path.exists():
            existing += 1
            total += len(read_text(path).splitlines())
    return {"source_files": existing, "total_lines": total}


def build_tree(paths: list[str]) -> str:
    tree: dict[str, dict] = {}
    for raw in paths:
        node = tree
        for part in raw.replace("\\", "/").split("/"):
            node = node.setdefault(part, {})

    lines: list[str] = []

    def walk(node: dict[str, dict], prefix: str = "") -> None:
        names = sorted(node)
        for index, name in enumerate(names):
            branch = "└── " if index == len(names) - 1 else "├── "
            lines.append(prefix + branch + name)
            child_prefix = prefix + ("    " if index == len(names) - 1 else "│   ")
            if node[name]:
                walk(node[name], child_prefix)

    walk(tree)
    return "\n".join(lines)


def markdown_image_path(item: AssetItem, base_dir: Path) -> str:
    return Path("..").joinpath("assets", base_dir.name, item.file).as_posix()


def build_information_txt(stats: dict[str, int]) -> str:
    main_features = (
        "本软件是一套面向 Flutter 与 Android 移动应用开发学习的教学演示型应用，围绕常见组件、页面交互、状态管理、"
        "主题样式、异步加载和移动端硬件能力组织功能。用户进入应用后可以在首页选择不同学习模块，查看每个模块的场景说明、"
        "示例代码和实际运行效果；文本展示模块用于理解基础文本、富文本、图标和网络图片的呈现方式；布局模块用于理解横向排列、"
        "弹性布局、自动换行和层叠布局等空间组织方式；按钮模块用于学习按钮启停、点击计数和交互反馈；表单模块用于演示输入、"
        "选择、协议勾选、校验和提交提示；反馈模块用于演示轻提示、对话框和底部操作面板；导航模块用于演示页面参数传递和结果回传；"
        "状态提升模块用于说明父子组件之间的数据流和回调机制；主题模块用于演示浅色、深色及系统主题切换；异步列表模块用于展示"
        "加载中、异常和成功三类状态；硬件入口模块进一步提供 GPS 定位、传感器监听、相机拍照、文件读取和蓝牙扫描等移动设备能力示例。"
        "软件不依赖独立服务器或数据库，主要通过本机 Flutter 运行时、Android 权限体系和第三方插件完成教学演示，适合课堂讲解、"
        "自学练习、移动端实验和组件行为对照验证。"
    )
    return f"""软件名称：{SOFTWARE_NAME}
版本号：{SOFTWARE_VERSION}

开发的硬件环境：{DEV_CPU}，内存 {DEV_MEMORY}，本地固态硬盘，Android 真机 {DEVICE_MODEL}
运行的硬件环境：Android 移动终端，已验证设备为 {DEVICE_MODEL}，屏幕分辨率 {DEVICE_RESOLUTION}
开发该软件的操作系统：{DEV_OS}
软件开发环境 / 开发工具：{FLUTTER_VERSION}，{DART_VERSION}，Android Gradle Kotlin DSL，Android SDK，Flutter CLI，ADB
该软件的运行平台 / 操作系统：Android 移动操作系统，已验证系统版本为 {DEVICE_OS}
软件运行支撑环境 / 支持软件：Flutter Engine、Android Runtime、Material 组件库、geolocator、sensors_plus、image_picker、file_picker、flutter_blue_plus
编程语言：Dart、Kotlin、Gradle Kotlin DSL、XML
源程序量：约 {stats['total_lines']} 行核心自研代码，纳入 {stats['source_files']} 个主要源码与配置文件
开发目的：为 Flutter 初学者和移动应用课程提供一套可直接运行的安卓学习应用，通过真实页面、示例代码和设备能力演示帮助学习者理解常见组件、交互模式和移动端权限调用方式。
面向行业 / 领域：移动应用开发教学、软件工程实践、Flutter 组件学习、Android 硬件能力实验
软件的主要功能：{main_features}
软件的技术特点：本软件采用 Flutter 跨平台框架和 Dart 语言实现页面层与交互逻辑，Android 端使用 Kotlin Android 插件和 Gradle Kotlin DSL 进行构建配置。系统以 Material Design 组件体系为基础，采用首页导航、专题页面、通用演示模板和硬件能力子页面的分层结构。页面状态主要通过 StatefulWidget 管理，路由跳转通过 Flutter Navigator 完成，主题模式由根组件统一维护。硬件能力通过 Android 权限声明和 Flutter 插件接入，包括定位服务、传感器事件流、相机调用、文件选择和蓝牙扫描。软件以单机应用方式运行，不内置账号体系、数据库连接或独立后端服务，适合离线安装、课堂演示和真机实验。"""


def build_facts_md(stats: dict[str, int]) -> str:
    names = [
        SOFTWARE_NAME,
        "Flutter组件实验学习手册软件",
        "安卓开发基础组件学习平台软件",
        "移动端Flutter组件教学演示系统",
        "Flutter硬件能力实验教学软件",
    ]
    lines = [
        "# 软著事实摘要",
        "",
        "## 软件名称候选",
        "",
    ]
    for index, name in enumerate(names, start=1):
        suffix = "（推荐）" if index == 1 else ""
        lines.append(f"- {name}{suffix}")
    lines.extend(
        [
            "",
            "推荐名称说明：当前应用既覆盖 Flutter 基础组件教学，又明确以 Android 真机运行和移动端学习为交付形态，因此推荐名称能够同时反映用途、技术和运行平台。",
            "",
            "## 已核验事实",
            "",
            "- 项目类型：Flutter Android 移动应用，仓库包含 android、ios、lib、web、windows、linux、macos 等 Flutter 标准目录。",
            f"- 应用标题：{APP_TITLE}。",
            f"- Android 包名：`{PACKAGE_NAME}`。",
            "- 当前版本：`1.0.0+1`。",
            f"- 运行真机：`{DEVICE_MODEL}`，系统 `{DEVICE_OS}`，分辨率 `{DEVICE_RESOLUTION}`。",
            f"- 核心代码规模：约 {stats['total_lines']} 行自研代码。",
            "- 页面模块：文本显示、布局、按钮交互、表单、反馈、导航、状态提升、主题、异步列表、硬件入口、GPS、传感器、相机、文件读取、蓝牙扫描。",
            "- 使用插件：`geolocator`、`sensors_plus`、`image_picker`、`file_picker`、`flutter_blue_plus`。",
            "- Android 权限：粗略定位、精确定位、相机、媒体图片读取、蓝牙、蓝牙管理、蓝牙扫描、蓝牙连接。",
            "",
            "## 缺口与说明",
            "",
            "- 仓库 README 仍为 Flutter 默认模板，软著资料以真实代码、配置和已留档截图为依据。",
            "- Android `applicationId` 当前为示例包名 `com.example.flutter_dudo`，本次登记材料按当前代码事实记录。",
            "- GPS 截图主要体现定位入口和结果区域结构，如需展示实时经纬度，可后续在真机授权后补采结果页。",
        ]
    )
    return "\n".join(lines)


def build_asset_records() -> str:
    lines = ["# 截图与图示记录", ""]
    lines.append("## 运行截图")
    for item in SCREENSHOTS:
        lines.extend(["", f"### {item.title}", "", item.description, "", f"![{item.title}]({markdown_image_path(item, SCREENSHOT_DIR)})"])
    lines.extend(["", "## 设计图示"])
    for item in DIAGRAMS:
        lines.extend(["", f"### {item.title}", "", item.description, "", f"![{item.title}]({markdown_image_path(item, DIAGRAM_DIR)})"])
    return "\n".join(lines)


def build_design_md(stats: dict[str, int]) -> str:
    lines = [
        f"# {DESIGN_DOC_NAME}",
        "",
        "## 目录",
        "",
        "1. 引言",
        "2. 需求概要分析",
        "3. 总体设计",
        "4. 用例设计",
        "5. 架构与部署设计",
        "6. 功能流程设计",
        "7. 详细设计",
        "8. 数据与权限设计",
        "9. 运行与部署设计",
        "10. 测试与验证",
        "11. 结论",
        "12. 附录",
        "",
        "## 1 引言",
        "",
        f"{SOFTWARE_NAME} 是一套面向 Flutter 与 Android 移动应用开发学习的教学演示型软件。系统通过可运行页面展示常用组件、页面导航、主题切换、异步加载和硬件能力调用方式，帮助学习者在真实移动端界面中理解组件行为和开发流程。",
        "",
        "### 1.1 编写目的",
        "本文档用于说明软件的需求背景、总体结构、模块划分、运行环境、权限设计、页面流程和详细设计，为软件著作权登记材料提供设计依据。",
        "",
        "### 1.2 软件范围",
        "软件范围包括 Flutter 应用页面、通用组件、Android 构建配置、权限声明和硬件能力演示页面。软件不包含独立后端服务、账号体系、远程数据库或服务器运维模块。",
        "",
        "### 1.3 术语说明",
        "- Flutter：用于构建多平台应用的 UI 框架。",
        "- Widget：Flutter 中描述界面结构和交互状态的基础单元。",
        "- Navigator：Flutter 页面跳转和结果回传机制。",
        "- ADB：Android 调试桥，用于安装、启动和调试 Android 应用。",
        "",
        "## 2 需求概要分析",
        "",
        "### 2.1 需求背景",
        "移动应用开发学习通常需要同时理解组件外观、交互行为、状态变化、页面跳转和设备权限调用。仅阅读代码难以直观看到组件运行效果，仅查看静态截图又难以理解参数变化和状态管理过程。因此，本软件将常见 Flutter 组件与 Android 设备能力集中组织为可运行的学习手册，让学习者能够通过页面操作观察代码逻辑和界面反馈之间的对应关系。",
        "",
        "### 2.2 用户角色",
        "- 学习者：浏览不同专题页面，查看示例代码并执行交互操作。",
        "- 教学人员：在课堂或实验环境中演示组件行为、导航流程和硬件能力接入方式。",
        "- 开发维护人员：根据课程需要扩展示例页面、更新插件版本或补充新的硬件能力。",
        "",
        "### 2.3 功能需求",
    ]
    for name, purpose, controls, flow, state in MODULE_DETAILS:
        lines.append(f"- {name}：{purpose}，主要控件包括{controls}，典型流程为{flow}，状态设计为{state}。")

    lines.extend(
        [
            "",
            "### 2.4 非功能需求",
            "- 可运行性：应用应能在 Android 真机上安装、启动和进入主要页面。",
            "- 可读性：页面应同时提供运行效果和示例代码，便于学习者对照理解。",
            "- 可维护性：页面模块保持相对独立，通用布局由组件复用。",
            "- 权限可控性：定位、相机、蓝牙和文件能力通过 Android 权限体系和插件能力调用。",
            "- 离线可用性：核心教学页面不依赖独立服务器或数据库。",
            "",
            "## 3 总体设计",
            "",
            "系统采用 Flutter 标准工程结构，`lib/` 目录承载页面和通用组件，`android/` 目录承载 Android 构建与权限配置。整体结构分为应用入口层、页面导航层、专题演示层、通用组件层和平台能力层。",
            "",
            "### 3.1 设计原则",
            "系统以模块清晰、示例可见、交互可验证为主要原则。每个专题页面围绕单一学习目标组织控件、代码片段和运行效果，避免把多个知识点混杂在同一页面中。硬件能力页面采用入口页加子页面的方式组织，降低首页信息密度。",
            "",
            "### 3.2 目录结构",
            "",
            "```text",
            build_tree([item.path for item in SOURCE_FILES]),
            "```",
            "",
            "## 4 用例设计",
            "",
            "### 4.1 用例图",
            "",
            f"![{DIAGRAMS[0].title}]({markdown_image_path(DIAGRAMS[0], DIAGRAM_DIR)})",
            "",
            "### 4.2 用例说明",
            "学习者启动应用后进入首页，选择目标专题页面。对于普通组件专题，学习者可以调整控件、查看界面变化和代码示例；对于硬件能力专题，学习者进入硬件入口后选择 GPS、传感器、相机、文件读取或蓝牙页面，并根据设备权限完成相应操作。",
            "",
            "### 4.3 首页截图",
            "",
            f"![{SCREENSHOTS[0].title}]({markdown_image_path(SCREENSHOTS[0], SCREENSHOT_DIR)})",
            "",
            "## 5 架构与部署设计",
            "",
            "### 5.1 架构图",
            "",
            f"![{DIAGRAMS[1].title}]({markdown_image_path(DIAGRAMS[1], DIAGRAM_DIR)})",
            "",
            "### 5.2 架构说明",
            "表现层由 MaterialApp、主题配置和各页面 Widget 构成；页面模块层承载文本、布局、按钮、表单、反馈、导航、状态、主题、异步列表和硬件入口；通用组件层复用演示页模板、分区卡片、代码展示和图片兜底组件；插件能力层通过 Flutter 插件访问 Android 定位、传感器、相机、文件和蓝牙能力；平台层由 Android Runtime 和设备硬件组成。",
            "",
            "### 5.3 部署图",
            "",
            f"![{DIAGRAMS[2].title}]({markdown_image_path(DIAGRAMS[2], DIAGRAM_DIR)})",
            "",
            "## 6 功能流程设计",
            "",
            "### 6.1 主流程图",
            "",
            f"![{DIAGRAMS[3].title}]({markdown_image_path(DIAGRAMS[3], DIAGRAM_DIR)})",
            "",
            "### 6.2 关键页面截图",
        ]
    )
    for item in SCREENSHOTS[1:]:
        lines.extend(["", f"#### {item.title}", "", item.description, "", f"![{item.title}]({markdown_image_path(item, SCREENSHOT_DIR)})"])

    lines.extend(
        [
            "",
            "## 7 详细设计",
            "",
            "### 7.1 主要类关系图",
            "",
            f"![{DIAGRAMS[4].title}]({markdown_image_path(DIAGRAMS[4], DIAGRAM_DIR)})",
            "",
            "### 7.2 模块详细设计",
        ]
    )
    for index, (name, purpose, controls, flow, state) in enumerate(MODULE_DETAILS, start=1):
        lines.extend(
            [
                "",
                f"#### 7.2.{index} {name}",
                "",
                f"{name}的设计目标是{purpose}。页面主要控件包括{controls}。典型业务流程为：{flow}。运行过程中，{state}。该模块与其他模块保持低耦合，通过 Flutter 路由或父组件回调完成页面切换和状态同步。",
                "",
                f"{name}的异常处理以页面内状态提示为主。当用户操作不满足条件、权限不可用或异步数据未返回时，页面通过文本、禁用状态、SnackBar 或结果区域展示当前状态，避免用户无法判断操作结果。该设计使教学演示过程保持连续，并能清楚展示正常路径和异常路径的差异。",
            ]
        )

    lines.extend(
        [
            "",
            "## 8 数据与权限设计",
            "",
            "### 8.1 数据设计",
            "系统不使用独立数据库。页面数据主要由组件内部状态、路由参数、插件返回值和示例列表组成。导航结果采用对象模型承载来源、消息和时间，硬件能力数据由插件实时返回并在页面中展示。",
            "",
            "### 8.2 权限设计",
            "- 定位权限：`ACCESS_FINE_LOCATION` 和 `ACCESS_COARSE_LOCATION`，用于 GPS 定位示例。",
            "- 相机权限：`CAMERA`，用于系统相机调用。",
            "- 媒体读取权限：`READ_MEDIA_IMAGES`，用于图片资源读取场景。",
            "- 蓝牙权限：`BLUETOOTH`、`BLUETOOTH_ADMIN`、`BLUETOOTH_SCAN`、`BLUETOOTH_CONNECT`，用于蓝牙扫描和连接能力展示。",
            "- 传感器能力：通过系统传感器服务读取陀螺仪和加速度计数据，不额外声明危险权限。",
            "",
            "### 8.3 数据安全",
            "软件未内置账号、口令、令牌、Cookie、数据库连接或服务器接口凭据。外部能力调用主要受 Android 权限控制，材料中涉及的设备信息仅保留型号、系统版本和分辨率等登记所需信息。",
            "",
            "## 9 运行与部署设计",
            "",
            "### 9.1 构建方式",
            "项目采用 Flutter 标准工程结构，Android 侧通过 Gradle Kotlin DSL 管理构建。应用包名为 `com.example.flutter_dudo`，版本为 `1.0.0+1`。",
            "",
            "### 9.2 真机运行方式",
            f"开发阶段通过 ADB 连接 Android 真机执行安装、启动和截图采集。当前截图于 {BUILD_DATE} 在 {DEVICE_MODEL} 真机中完成，验证了首页、表单、导航、主题、硬件入口、GPS 与传感器等关键页面。",
            "",
            "### 9.3 部署特点",
            "系统以单机应用方式部署，不依赖独立服务器、数据库服务或后台中间件。教学内容和示例逻辑封装在移动端内部，适合离线安装和课堂演示。",
            "",
            "## 10 测试与验证",
            "",
            "### 10.1 验证方式",
            "软件采用代码检查、真机运行和页面截图留档相结合的方式验证。当前已核验页面包括首页、表单、导航、路由详情、主题、硬件入口、GPS 页面和传感器页面。",
            "",
            "### 10.2 验证结论",
            "- 应用可在 Android 真机成功安装并启动。",
            "- 首页可进入各学习模块。",
            "- 表单页面可展示输入组件和提交流程。",
            "- 导航页面与详情页可完成参数传递和结果回传。",
            "- 主题页面可展示主题切换控件和预览卡片。",
            "- 硬件入口页可进入 GPS 与传感器示例页面。",
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
            f"{SOFTWARE_NAME} 以 Flutter 为核心开发框架，将移动端基础组件、典型交互模式和常见硬件能力接入集中整合为一套可运行、可演示、可教学的安卓学习应用。系统结构清晰、模块边界明确、页面逻辑完整，适合作为 Flutter 初学者实验手册和移动应用教学演示软件。",
            "",
            "## 12 附录",
            "",
            "### 12.1 源码规模说明",
            f"当前纳入软著整理的核心自研代码共 {stats['source_files']} 个主要文件，累计约 {stats['total_lines']} 行，覆盖应用结构、页面逻辑、交互流程、硬件能力和 Android 运行配置。",
            "",
            "### 12.2 截图索引",
        ]
    )
    for item in SCREENSHOTS:
        lines.append(f"- {item.title}：{item.description}")
    lines.extend(["", "### 12.3 图示索引"])
    for item in DIAGRAMS:
        lines.append(f"- {item.title}：{item.description}")
    lines.extend(
        [
            "",
            "### 12.4 页面级详细设计附录",
            "",
            "本附录按照已核验页面模块展开补充说明，用于记录各模块的输入、输出、状态、异常处理和与其他模块的关系。",
        ]
    )
    for index, (name, purpose, controls, flow, state) in enumerate(MODULE_DETAILS, start=1):
        lines.extend(
            [
                "",
                f"#### 12.4.{index} {name}补充设计",
                "",
                f"{name}的输入主要来自用户在页面上的点击、选择、文本输入或设备能力授权结果。模块围绕“{purpose}”组织页面结构，控件组合包括{controls}，这些控件在界面上形成可观察、可操作、可回退的学习闭环。",
                "",
                f"{name}的处理过程以 Flutter Widget 状态更新为核心。典型流程是{flow}。当状态发生变化时，页面通过 setState 或上级回调刷新局部展示，使学习者能够在同一页面中对照操作前后的差异。",
                "",
                f"{name}的输出包括界面显示结果、状态提示、路由返回值或插件调用结果。运行状态设计为{state}，不会把临时演示状态写入外部数据库，也不会向远程服务上传学习过程数据。",
                "",
                f"{name}的异常处理遵循移动端即时反馈原则。对于输入缺失、权限不可用、异步异常、取消操作或设备能力不可用等情况，页面通过提示文本、禁用状态、弹窗或结果区域说明当前状态，避免用户在教学演示中无法判断操作是否完成。",
                "",
                f"{name}与其他模块之间保持边界清晰。普通页面主要通过首页进入并通过系统返回键或 AppBar 返回；需要跨页面通信的导航模块使用 Flutter Navigator 参数和返回结果完成；硬件相关页面通过硬件入口模块集中分发，以减少首页与具体设备能力之间的耦合。",
                "",
                f"{name}的验收重点包括页面能否正常进入、核心控件是否可见、状态变化是否与用户操作一致、返回路径是否清晰以及异常场景是否给出明确反馈。对于教学类页面，还需要确认示例代码区域与页面效果区域能形成对应关系，便于学习者把代码片段和运行结果联系起来。",
                "",
                f"{name}的运行约束主要来自 Flutter 渲染机制、Android 设备权限和终端硬件能力。普通组件页面依赖 Flutter Material 组件库即可运行；涉及设备能力的页面需要在真机上验证权限授权、硬件可用性和插件回调结果，因此相关截图以真机运行为准。",
            ]
        )
    lines.extend(
        [
            "",
            "### 12.5 源码文件职责附录",
            "",
            "本附录按照纳入源码稿的文件清单补充职责说明，用于对应设计说明书中的模块实现依据。",
        ]
    )
    for index, item in enumerate(SOURCE_FILES, start=1):
        rel_path = item.path.replace("\\", "/")
        lines.extend(
            [
                "",
                f"#### 12.5.{index} {rel_path}",
                "",
                f"该文件所属模块为{item.module}，主要职责是{item.purpose}。在系统结构中，该文件与其上级目录共同构成软件的可运行基础，能够支撑设计说明书中对应的页面、构建、权限或通用组件说明。",
                "",
                f"从维护角度看，{rel_path} 的变更应保持与现有 Flutter 工程结构一致。涉及页面逻辑的文件应优先保持页面状态、控件结构和导航关系清晰；涉及 Android 配置的文件应优先保持包名、权限和构建参数与实际运行目标一致。",
                "",
                f"从登记材料角度看，该文件被纳入源码稿是因为它直接体现了软件的自研页面结构、交互流程、运行入口或平台能力接入方式。第三方依赖源码、构建缓存和自动生成产物未纳入本次源码正文。",
            ]
        )
    lines.extend(
        [
            "",
            "### 12.6 权限与插件映射附录",
            "",
            "定位功能由 `geolocator` 插件承载，配套使用精确定位和粗略定位权限。页面在用户点击定位按钮后检查系统服务和授权状态，并根据返回结果展示坐标或错误提示。",
            "",
            "传感器功能由 `sensors_plus` 插件承载，页面订阅陀螺仪和加速度计事件流。该类能力依赖终端硬件是否提供对应传感器，页面以实时数值区域展示最近一次事件结果。",
            "",
            "相机功能由 `image_picker` 插件承载，Android 清单中声明相机权限。页面调用系统相机后接收拍照文件并展示预览，取消拍照或调用失败时展示状态文本。",
            "",
            "文件读取功能由 `file_picker` 插件承载，页面调用系统文件选择器后读取文本内容并展示摘要。该功能不直接访问固定服务器路径，也不在材料中保留真实用户文件内容。",
            "",
            "蓝牙功能由 `flutter_blue_plus` 插件承载，Android 清单中声明蓝牙、蓝牙管理、扫描和连接权限。页面启动扫描后汇总附近设备名称、标识和信号强度，用于教学演示蓝牙扫描流程。",
            "",
            "### 12.7 运行截图验收记录附录",
            "",
            "本附录按照已经纳入材料的真机截图补充页面验收记录，用于说明截图对应的页面状态、可见内容和纳入依据。",
        ]
    )
    for index, item in enumerate(SCREENSHOTS, start=1):
        lines.extend(
            [
                "",
                f"#### 12.7.{index} {item.title}",
                "",
                f"{item.description}截图来源于 Android 真机运行界面，能够证明对应页面已经进入可显示状态，并且页面中的主要控件、标题、区域划分和交互入口处于可识别状态。",
                "",
                "从验收角度看，该截图的重点不是展示静态美术效果，而是确认页面结构、功能入口和交互反馈区域已经形成完整闭环。页面可见信息能够支撑设计说明书中对应模块的功能说明，并可作为后续人工复核的图像依据。",
                "",
                "从软著材料角度看，该截图被纳入最终材料，是因为它能代表一个独立功能场景或关键流程节点。截图未包含账号口令、真实个人信息、服务器地址、数据库连接或其他敏感凭据。",
                "",
                "该截图与源码文件之间存在明确对应关系。页面入口、控件布局、状态字段和路由关系均可在 `lib/pages/` 或 `lib/widgets/` 下的源码中找到实现依据，因此截图不是脱离代码的演示素材。",
            ]
        )
    lines.extend(
        [
            "",
            "### 12.8 组件交互矩阵附录",
            "",
            "本附录从输入、处理、输出和依赖四个角度记录各页面模块的交互关系，便于对照源码和运行界面进行复核。",
        ]
    )
    for index, (name, purpose, controls, flow, state) in enumerate(MODULE_DETAILS, start=1):
        lines.extend(
            [
                "",
                f"#### 12.8.{index} {name}交互矩阵",
                "",
                f"输入维度：{name}接收的输入主要来自用户触发的控件操作，相关控件包括{controls}。对于设备能力相关模块，输入还包括系统权限弹窗、设备服务状态和插件返回事件。",
                "",
                f"处理维度：模块围绕{purpose}执行页面逻辑。典型处理流程为{flow}。处理过程保持在 Flutter 页面状态或插件回调中完成，不依赖远程业务接口。",
                "",
                f"输出维度：模块输出为可见页面状态、提示信息、列表数据、路由返回结果或设备能力结果。状态设计为{state}，有助于学习者观察操作与结果之间的对应关系。",
                "",
                f"依赖维度：{name}依赖 Flutter Material 组件、项目内通用组件和必要的 Android 插件能力。模块之间通过首页导航、命名路由或回调函数连接，未形成跨模块共享的隐式全局业务状态。",
            ]
        )
    lines.extend(
        [
            "",
            "### 12.9 源码到功能追踪矩阵附录",
            "",
            "本附录用于说明源码文件与功能模块、设计章节之间的对应关系，便于从材料追溯到真实实现文件。",
        ]
    )
    for index, item in enumerate(SOURCE_FILES, start=1):
        rel_path = item.path.replace("\\", "/")
        lines.extend(
            [
                "",
                f"#### 12.9.{index} {rel_path}",
                "",
                f"追踪对象：`{rel_path}`。该文件归属{item.module}，在软件中承担“{item.purpose}”的职责。设计说明书中关于该模块的总体说明、详细设计、运行约束和验收重点，均可通过该文件或其相邻文件进行核对。",
                "",
                f"追踪关系：当该文件属于 `lib/` 目录时，它主要对应页面或组件层设计；当该文件属于 `android/` 目录时，它主要对应构建、权限或平台入口设计；当该文件属于项目配置时，它主要对应运行环境、依赖插件和版本信息。该追踪关系有助于确认软著材料没有脱离真实代码进行虚构描述。",
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
        f"- 代码规模：约 {stats['total_lines']} 行核心自研代码",
        "",
        "## 2 源代码属性结构说明",
        "",
        "- 技术栈：Flutter、Dart、Kotlin、Android Gradle Kotlin DSL、XML。",
        f"- 源码根目录：`{ROOT}`。",
        "- 一级目录划分：`android/` 用于 Android 构建与权限声明，`lib/` 用于 Flutter 页面与组件实现，`docs/` 用于软著材料输出。",
        "- 二级目录划分：`lib/pages/` 承载页面模块，`lib/widgets/` 承载通用组件，`lib/pages/hardware/` 承载设备能力示例。",
        "- 选入范围说明：纳入应用配置、Flutter 页面、通用组件、Android 权限清单和启动入口，不纳入第三方依赖、构建缓存和生成产物。",
        "",
        "## 3 三级目录结构表",
        "",
        "```text",
        build_tree([item.path for item in SOURCE_FILES]),
        "```",
        "",
        "## 4 按目录顺序整理的源代码",
        "",
    ]
    for index, item in enumerate(SOURCE_FILES, start=1):
        path = ROOT / item.path
        rel_path = item.path.replace("\\", "/")
        content = read_text(path).rstrip() if path.exists() else ""
        ext = path.suffix.lstrip(".") or "text"
        lines.extend(
            [
                f"### 4.{index} {rel_path}",
                "",
                f"文件路径：`{rel_path}`",
                "",
                f"文件作用：{item.purpose}",
                "",
                f"所属模块：{item.module}",
                "",
                f"```{ext}",
                content,
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def write_asset_txt_files() -> None:
    for directory, items in ((SCREENSHOT_DIR, SCREENSHOTS), (DIAGRAM_DIR, DIAGRAMS)):
        for item in items:
            image = directory / item.file
            if not image.exists():
                continue
            write_text(image.with_suffix(".txt"), f"{item.title}\n\n{item.description}该图片用于软著材料中证明对应页面、流程或结构已经完成梳理，能够支撑设计说明书中的功能描述和模块关系说明。")


def register_fonts() -> tuple[str, str]:
    try:
        regular = "MicrosoftYaHei"
        bold = "MicrosoftYaHeiBold"
        pdfmetrics.registerFont(TTFont(regular, r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
        pdfmetrics.registerFont(TTFont(bold, r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))
        return regular, bold
    except Exception:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        return "STSong-Light", "STSong-Light"


def build_styles(body_font: str, bold_font: str, compact: bool) -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    body_size = 11.2 if compact else 11.8
    body_leading = 16 if compact else 18
    code_size = 10.4 if compact else 8.5
    code_leading = 17.2 if compact else 10.5
    return {
        "title": ParagraphStyle("title", parent=sample["Heading1"], fontName=bold_font, fontSize=18, leading=24, alignment=TA_CENTER, spaceAfter=8, wordWrap="CJK"),
        "h1": ParagraphStyle("h1", parent=sample["Heading1"], fontName=bold_font, fontSize=15, leading=20, spaceBefore=8, spaceAfter=5, wordWrap="CJK"),
        "h2": ParagraphStyle("h2", parent=sample["Heading2"], fontName=bold_font, fontSize=12.5, leading=17, spaceBefore=6, spaceAfter=4, wordWrap="CJK"),
        "h3": ParagraphStyle("h3", parent=sample["Heading3"], fontName=bold_font, fontSize=11.2, leading=15, spaceBefore=4, spaceAfter=3, wordWrap="CJK"),
        "body": ParagraphStyle("body", parent=sample["BodyText"], fontName=body_font, fontSize=body_size, leading=body_leading, alignment=TA_LEFT, spaceAfter=2.5, wordWrap="CJK"),
        "bullet": ParagraphStyle("bullet", parent=sample["BodyText"], fontName=body_font, fontSize=body_size, leading=body_leading, leftIndent=13, firstLineIndent=-8, spaceAfter=2, wordWrap="CJK"),
        "caption": ParagraphStyle("caption", parent=sample["BodyText"], fontName=body_font, fontSize=8.5, leading=12, alignment=TA_CENTER, spaceBefore=2, spaceAfter=6, wordWrap="CJK"),
        "code": ParagraphStyle("code", parent=sample["Code"], fontName=body_font, fontSize=code_size, leading=code_leading, leftIndent=4, rightIndent=4, borderPadding=4, backColor=colors.HexColor("#F4F6F8")),
    }


def add_paragraph(story: list, text: str, style: ParagraphStyle) -> None:
    story.append(Paragraph(escape(text), style))


def markdown_to_story(md_path: Path, styles: dict[str, ParagraphStyle], compact: bool) -> list:
    story: list = []
    buffer: list[str] = []
    code_buffer: list[str] = []
    in_code = False
    title_used = False

    def flush_paragraph() -> None:
        nonlocal buffer
        text = " ".join(line.strip() for line in buffer).strip()
        if text:
            add_paragraph(story, text, styles["body"])
        buffer = []

    for raw_line in read_text(md_path).splitlines():
        line = raw_line.rstrip()
        stripped = line.lstrip()
        if stripped.startswith("```"):
            flush_paragraph()
            if in_code:
                story.append(Preformatted("\n".join(code_buffer), styles["code"], maxLineLength=112))
                story.append(Spacer(1, 3))
                code_buffer = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buffer.append(line[:160])
            continue
        if not stripped:
            flush_paragraph()
            story.append(Spacer(1, 3))
            continue
        image_match = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if image_match:
            flush_paragraph()
            caption, raw_path = image_match.groups()
            image_path = (md_path.parent / raw_path).resolve()
            if image_path.exists():
                img = RLImage(str(image_path))
                max_width = 170 * mm
                max_height = 150 * mm if compact else 185 * mm
                scale = min(max_width / img.imageWidth, max_height / img.imageHeight, 1)
                img.drawWidth = img.imageWidth * scale
                img.drawHeight = img.imageHeight * scale
                story.append(img)
                add_paragraph(story, caption, styles["caption"])
            continue
        heading = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level == 1 and not title_used:
                add_paragraph(story, text, styles["title"])
                title_used = True
            elif level == 1:
                add_paragraph(story, text, styles["h1"])
            elif level == 2:
                add_paragraph(story, text, styles["h2"])
            else:
                add_paragraph(story, text, styles["h3"])
            continue
        if stripped.startswith("- "):
            flush_paragraph()
            add_paragraph(story, "• " + stripped[2:].strip(), styles["bullet"])
            continue
        buffer.append(stripped)
    flush_paragraph()
    if code_buffer:
        story.append(Preformatted("\n".join(code_buffer), styles["code"], maxLineLength=112))
    return story


def render_pdf(md_path: Path, pdf_path: Path, compact: bool) -> int:
    body_font, bold_font = register_fonts()
    styles = build_styles(body_font, bold_font, compact)
    story = markdown_to_story(md_path, styles, compact)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    build_path = pdf_path.with_name(f"__build_{pdf_path.stem.encode('utf-8').hex()[:24]}.pdf")
    if build_path.exists():
        build_path.unlink()
    doc = SimpleDocTemplate(
        str(build_path),
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=17 * mm,
        bottomMargin=13 * mm,
        title=md_path.stem,
        author="Codex",
    )

    def header(canvas, _doc) -> None:
        canvas.saveState()
        canvas.setFont(body_font, 8.5)
        canvas.drawString(doc.leftMargin, A4[1] - 9 * mm, f"{SOFTWARE_NAME} {SOFTWARE_VERSION}")
        canvas.restoreState()

    doc.build(story, onFirstPage=header, onLaterPages=header)
    if pdf_path.exists():
        pdf_path.unlink()
    build_path.replace(pdf_path)
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


def archive_outputs(paths: list[Path]) -> Path:
    target_root = ARCHIVE_ROOT / SOFTWARE_NAME
    if target_root.exists():
        shutil.rmtree(target_root)
    pdf_dir = target_root / "pdf"
    text_dir = target_root / "text"
    diagram_dir = target_root / "images" / "diagrams"
    shot_dir = target_root / "images" / "screenshots"
    for directory in (pdf_dir, text_dir, diagram_dir, shot_dir, target_root / "apk"):
        directory.mkdir(parents=True, exist_ok=True)

    for path in paths:
        if path.suffix.lower() == ".pdf":
            shutil.copy2(path, pdf_dir / path.name)
            full = path.with_name(path.stem + ".full.pdf")
            if full.exists():
                shutil.copy2(full, pdf_dir / full.name)
        else:
            shutil.copy2(path, text_dir / path.name)

    for item in SCREENSHOTS:
        src = SCREENSHOT_DIR / item.file
        if src.exists():
            shutil.copy2(src, shot_dir / src.name)
            txt = src.with_suffix(".txt")
            if txt.exists():
                shutil.copy2(txt, shot_dir / txt.name)
    for item in DIAGRAMS:
        src = DIAGRAM_DIR / item.file
        if src.exists():
            shutil.copy2(src, diagram_dir / src.name)
            txt = src.with_suffix(".txt")
            if txt.exists():
                shutil.copy2(txt, diagram_dir / txt.name)
        svg = src.with_suffix(".svg")
        if svg.exists():
            shutil.copy2(svg, diagram_dir / svg.name)
    return target_root


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    write_asset_txt_files()
    stats = source_stats()

    info_path = DOCS_DIR / "information.txt"
    facts_path = DOCS_DIR / "facts.md"
    record_path = DOCS_DIR / "截图记录.md"
    design_md_path = DOCS_DIR / f"{DESIGN_DOC_NAME}.md"
    source_md_path = DOCS_DIR / f"{SOURCE_DOC_NAME}.md"

    write_text(info_path, build_information_txt(stats))
    write_text(facts_path, build_facts_md(stats))
    write_text(record_path, build_asset_records())
    write_text(design_md_path, build_design_md(stats))
    write_text(source_md_path, build_source_md(stats))

    design_pdf_path = DOCS_DIR / f"{DESIGN_DOC_NAME}.pdf"
    source_pdf_path = DOCS_DIR / f"{SOURCE_DOC_NAME}.pdf"
    design_pages = render_pdf(design_md_path, design_pdf_path, compact=False)
    source_pages = render_pdf(source_md_path, source_pdf_path, compact=True)
    design_pages, _ = crop_pdf_if_needed(design_pdf_path)
    source_pages, _ = crop_pdf_if_needed(source_pdf_path)
    target_root = archive_outputs([info_path, facts_path, record_path, design_md_path, source_md_path, design_pdf_path, source_pdf_path])

    print(f"software_name={SOFTWARE_NAME}")
    print(f"design_pdf={design_pdf_path}")
    print(f"design_pages={design_pages}")
    print(f"source_pdf={source_pdf_path}")
    print(f"source_pages={source_pages}")
    print(f"archive_root={target_root}")


if __name__ == "__main__":
    main()
