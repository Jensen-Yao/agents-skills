---
name: windows-ios-cicd
description: >-
  在 Windows 上开发、构建并可视化验证 iOS/watchOS 应用的标准工作流（无本机 Mac/Xcode）：
  XcodeGen 工程定义 + Swift Package 本地包 + GitHub Actions macOS CI（构建/测试/签名）+
  XCUITest 模拟器截图回传 + SSH/gh API 网络传输 + 免费账号分发。
  含 20+ 个真实踩坑记录与修复（xcodegen 多平台依赖、watchOS WidgetKit 枚举、
  PowerShell 编码损坏、倒置区间崩溃、simctl 启动参数、App.init 写 SwiftData 崩溃等）。
  Use when: 在 Windows 上开发 iOS/watchOS 应用、无 Mac 构建 iOS、iOS CI/CD 配置、
  模拟器截图/预览、xcodegen watchOS 工程、GitHub Actions iOS runner、
  免费开发者账号分发、SSH 推送 GitHub 替代 HTTPS。
  Standard workflow for building and visually verifying iOS/watchOS apps on Windows
  without a local Mac/Xcode, with 20+ documented pitfalls and fixes.
---

# Windows → iOS/watchOS 构建与模拟器验证标准（Build & Verify iOS/watchOS from Windows）

> 核心结论：**Windows 上无法本地编译 iOS 代码，但可以完成 100% 的开发工作**
> ——代码在 Windows 编写，编译/测试/截图全部在 GitHub Actions 的 macOS runner 完成，
> 结果（构建状态、测试报告、模拟器截图）自动回传仓库。
> Key idea: all iOS development can happen on Windows; compilation & simulator runs happen on CI macOS runners, with artifacts pushed back into the repo.

---

## 1. 总原则 / Core Principles

| # | 原则 | 说明 |
|---|---|---|
| 1 | **代码在 Windows，构建在 CI** | Windows 只写代码与工程定义；`xcodebuild` 只存在于 CI macOS runner |
| 2 | **工程用 XcodeGen 定义，`.xcodeproj` 不入库** | `project.yml` 是唯一事实源；CI 上 `xcodegen generate` 再构建 |
| 3 | **纯逻辑抽成 Swift Package（SPM 本地包）** | 预测/算法等无 UI 代码放 SPM 包：iOS/watchOS 双平台可用、可独立单测、避免 xcodegen 多平台 target 坑 |
| 4 | **每个 push 必须 CI 绿灯** | 编译错误在 5 分钟内暴露，绝不攒到最后 |
| 5 | **模拟器截图走 XCUITest** | `simctl launch` 不稳定（参数/时序坑多）；`xcodebuild test` 是唯一稳定启动 App 的通道 |
| 6 | **一切自动回传仓库** | 截图/测试结果 commit 回 repo，Windows 端 pull 即可查看 |

---

## 2. 工程标准 / Project Standard

### 2.1 目录结构（推荐 monorepo）

```
Project/
├── project.yml                 # XcodeGen 定义（唯一工程事实源）
├── AppKit/                     # SPM 本地包（纯逻辑，iOS+watchOS 双平台）
│   └── Package.swift
├── App/                        # iOS App（SwiftUI）
├── Watch/                      # watchOS App
├── WatchWidget/                # watchOS complication（独立 widget extension）
├── Widget/                     # iOS 小组件 extension
├── Shared/                     # 跨 target 共享源文件（消息结构、FlowLevel 等）
├── Tests/
│   ├── UnitTests/              # 单元测试（SPM 包的测试 + App 测试）
│   └── UITests/                # 截图/UI 测试（关键！见 §4）
├── docs/screenshots/           # CI 自动提交的模拟器截图
└── .github/workflows/
    ├── ios.yml                 # 常规 CI：build + test
    └── simulator-shots.yml     # 手动触发：截图并 commit 回仓库
```

### 2.2 project.yml 要点 / XcodeGen Essentials

```yaml
name: MyApp
options:
  bundleIdPrefix: com.example
  deploymentTarget:
    iOS: "17.0"
    watchOS: "10.0"

packages:                        # ★ 本地 SPM 包（不要用 xcodegen 的 framework target！）
  MyKit:
    path: MyKit

targets:
  MyApp:
    type: application
    platform: iOS
    sources: [{path: App}, {path: Shared}]
    dependencies:
      - package: MyKit          # ★ 引用方式：package，不是 target
      - target: MyWatch
        embed: true
      - target: MyWidget
        embed: true
    info:
      path: App/Info.plist      # xcodegen 自动生成，含权限描述
      properties:
        UILaunchScreen: {}
        NSHealthShareUsageDescription: "…"
        NSHealthUpdateUsageDescription: "…"
        NSSpeechRecognitionUsageDescription: "…"
        NSMicrophoneUsageDescription: "…"
    entitlements:
      path: App/App.entitlements
      properties:
        com.apple.developer.healthkit: true
        com.apple.security.application-groups: [group.com.example.app]

  MyWatch:
    type: application            # ★ watchOS 用 application，不是 application.watchapp2！（坑 #4）
    platform: watchOS
    sources: [{path: Watch}, {path: Shared}]
    dependencies:
      - package: MyKit
      - target: MyWatchWidget
        embed: true

  MyWatchWidget:                 # watchOS complication 必须独立 extension（坑 #3）
    type: app-extension
    platform: watchOS
    info:
      path: WatchWidget/Info.plist
      properties:
        NSExtension:
          NSExtensionPointIdentifier: com.apple.widgetkit-extension

schemes:
  MyApp:
    build: {targets: {MyApp: all, MyWatch: all, MyWatchWidget: all, MyWidget: all}}
    test: {config: Debug, targets: [MyAppTests, MyKitTests]}
  MyAppUITests:                  # ★ 截图专用 scheme（与常规 CI 隔离）
    build: {targets: {MyApp: all, MyAppUITests: [test]}}
    test: {config: Debug, targets: [MyAppUITests]}
```

### 2.3 Swift 版本与并发
- `SWIFT_VERSION: "5.10"`（Xcode 16 默认；避免 Swift 6 严格并发误伤）
- **`@MainActor` 服务类（SwiftData store 等）被 View 的普通方法同步调用会编译失败** → 给相关 `View` 结构体整体标 `@MainActor`
- SwiftData `@Model` 类默认 `Identifiable`（`persistentModelID`），可直接用于 `sheet(item:)`

---

## 3. CI 标准 / CI Standard

### 3.1 常规 CI（`.github/workflows/ios.yml`）

```yaml
name: iOS CI
on: {push: {branches: [main]}, pull_request:}
jobs:
  build-and-test:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - run: brew install xcodegen
      - run: xcodegen generate
      # ★ build 用 generic 目的地（不依赖具体模拟器型号，永远可用）
      - name: Build
        run: |
          xcodebuild build -project MyApp.xcodeproj -scheme MyApp \
            -destination 'generic/platform=iOS Simulator' CODE_SIGNING_ALLOWED=NO
      # ★ test 必须具体设备：动态探测（runner 镜像的模拟器型号会变！）
      - name: Test
        run: |
          SIM_NAME=$(xcrun simctl list devices available -j | python3 -c "import json,sys;d=json.load(sys.stdin)['devices'];all_=[x for v in d.values() for x in v if x.get('isAvailable') and x['name'].startswith('iPhone')];print(sorted(all_,key=lambda x:x['name'])[-1]['name'] if all_ else '')")
          xcodebuild test -project MyApp.xcodeproj -scheme MyApp \
            -destination "platform=iOS Simulator,name=$SIM_NAME" CODE_SIGNING_ALLOWED=NO
```

要点：
- **build 用 `generic/platform=iOS Simulator`**；**test 用探测到的具体设备名**（硬编码 `iPhone 16` 会因 runner 镜像不同而 "Unable to find a device"）
- 免费/无证书环境 `CODE_SIGNING_ALLOWED=NO` 足够编译与单测
- **单测能启动 App**（host app 机制），所以单测通过 ≈ App 可启动

### 3.2 GitHub 计费 / Billing
- **Private 仓库免费额度 2000 分钟/月，macOS runner 按 10 倍计**（即约 200 分钟实际）
- 额度耗尽/欠费 → job 被拒：`The job was not started because recent account payments have failed...`
- **Public 仓库 Actions 免费无限** ← 常用解法：临时 `gh repo edit --visibility public --accept-visibility-change-consequences`，随时可切回 private

---

## 4. 模拟器截图标准（Windows 上看 App 效果的唯一通道）/ Simulator Screenshots via XCUITest

> ★ 结论：不要用 `simctl launch` + `simctl io screenshot`（参数与时序坑太多，见坑 #7~#9）。
> 用 **XCUITest 驱动截图**：`xcodebuild test` 是唯一稳定启动 App 的通道。

### 4.1 UI 测试模板（`Tests/UITests/ScreenshotTests.swift`）

```swift
import XCTest

final class ScreenshotTests: XCTestCase {
    func testCaptureAllTabs() throws {
        let app = XCUIApplication()
        let springboard = XCUIApplication(bundleIdentifier: "com.apple.springboard")

        for tab in ["home", "detail", "settings"] {
            // ★ 用 launchEnvironment 传截图参数（App 端读 ProcessInfo.environment）
            app.launchEnvironment["MY_SKIP_ONBOARDING"] = "1"
            app.launchEnvironment["MY_SEED_DEMO"] = "1"
            app.launchEnvironment["MY_OPEN_TAB"] = tab
            app.launch()

            // ★ 轮询处理系统弹窗（HealthKit 授权等），最长 12 秒
            for _ in 0..<6 {
                Thread.sleep(forTimeInterval: 2)
                let turnOnAll = springboard.buttons["Turn On All"]
                let allow = springboard.buttons["Allow"]
                if turnOnAll.exists { turnOnAll.tap(); break }
                if allow.exists { allow.tap(); break }
            }

            _ = app.buttons.firstMatch.waitForExistence(timeout: 15)
            Thread.sleep(forTimeInterval: 4)

            let screenshot = XCUIScreen.main.screenshot()
            // ★ 直接写 runner 沙盒 Documents（CI 用 simctl 拷贝，规范命名）
            if let docs = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first {
                try? screenshot.pngRepresentation.write(to: docs.appendingPathComponent("\(tab).png"))
            }
            app.terminate()
        }
    }
}
```

App 端读取参数（仅 DEBUG 生效）：

```swift
enum LaunchArguments {
    static var seedDemo: Bool {
        #if DEBUG
        return ProcessInfo.processInfo.environment["MY_SEED_DEMO"] == "1"
        #else
        return false
        #endif
    }
}
```

### 4.2 截图工作流（`.github/workflows/simulator-shots.yml`）

```yaml
name: Simulator Screenshots
on: workflow_dispatch
permissions: {contents: write}   # ★ 允许 CI 把截图 commit 回仓库
jobs:
  shots:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - run: brew install xcodegen
      - run: xcodegen generate
      - name: Boot simulator
        run: |
          SIM_UDID=$(xcrun simctl list devices available -j | python3 -c "…取最后一个 iPhone 的 udid…")
          echo "SIM_UDID=$SIM_UDID" >> "$GITHUB_ENV"
          xcrun simctl boot "$SIM_UDID" || true
          xcrun simctl bootstatus "$SIM_UDID" -b
      - name: Run UI tests & collect screenshots
        run: |
          SIM_NAME=$(…探测设备名…)
          xcodebuild test -project MyApp.xcodeproj -scheme MyAppUITests \
            -destination "platform=iOS Simulator,name=$SIM_NAME" \
            -resultBundlePath ui-tests.xcresult -only-testing:MyAppUITests
          mkdir -p docs/screenshots
          # ★ 从 UI test runner 沙盒直拷规范命名截图
          RUNNER=$(xcrun simctl get_app_container "$SIM_UDID" com.example.app.uitests.xctrunner data)
          cp "$RUNNER"/Documents/*.png docs/screenshots/ || true
      - name: Commit screenshots
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add docs/screenshots/
          git commit -m "docs: 模拟器截图（自动生成）" || echo "no changes"
          git push
```

要点：
- 截图写 **UI test runner 的沙盒 Documents**（`simctl get_app_container <udid> com.example.app.uitests.xctrunner data`），比 `xcresulttool export attachments`（UUID 命名、需二次映射）省事
- CI 直接 commit + push 回仓库 → Windows 端 `git pull` 即见截图
- 演示数据（seed）通过 launchEnvironment 注入，截图内容可控

---

## 5. 网络与二进制传输标准（中国大陆网络）/ Network & Binary Transfer

典型环境：`github.com:443` 被阻断，`github.com:22`（SSH）通，`api.github.com` 通，`raw.githubusercontent.com` 时通时断。

| 需求 | 标准做法 |
|---|---|
| git push/pull | **SSH 协议**：`git remote set-url origin git@github.com:<user>/<repo>.git`。若本地已有绑定其他账号的 key（`Permission denied` / `key is already in use`），生成新 key 并 `gh ssh-key add` 注册到目标账号 |
| 触发工作流/查状态/查日志 | `gh` CLI（走 api.github.com，通常可用） |
| 下载仓库二进制（截图等） | `curl.exe -H "Authorization: Bearer $(gh auth token)" -H "Accept: application/vnd.github.raw" -o out.png "https://api.github.com/repos/<user>/<repo>/contents/<path>?ref=main"` |
| ❌ 反例 | PowerShell 的 `>` 重定向与 `gh api raw` 输出会把二进制按 UTF-16 写盘导致文件损坏；用 `curl.exe -o`（注意是 `curl.exe` 不是 PS 别名）或 base64 解码 |

SSH 配置（`~/.ssh/config`）：

```
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/ylovel_github_ed25519
  IdentitiesOnly yes
```

---

## 6. 踩坑清单 / Pitfalls & Fixes（按踩坑顺序）

### 工程与编译 / Project & Compile

| # | 坑（症状） | 原因 | 修复 |
|---|---|---|---|
| 1 | xcodegen：`Target "X" has invalid dependency: "MyKit"`（多平台 framework target 依赖） | xcodegen 多平台 target 会生成 `MyKit_iOS`/`MyKit_watchOS` 后缀 target | **改用 SPM 本地包**：`packages: {MyKit: {path: MyKit}}` + `dependencies: [{package: MyKit}]` |
| 2 | `project.yml` 中文乱码导致 YAML 解析失败（`闇€瑕` 类乱码） | Windows PowerShell 5.1 `Get-Content` 按 GBK 读无 BOM UTF-8 文件，写回时损坏 | **永不用 PowerShell 处理含中文的工程文件**；用支持 UTF-8 的工具（编辑器/write API）编辑；加 `.gitattributes`：`*.swift text eol=lf`、`*.yml text eol=lf` |
| 3 | `WidgetFamily has no member 'circular'` | watchOS WidgetKit 的 family 枚举是 accessory 系列 | watchOS 用 `.accessoryCircular / .accessoryRectangular / .accessoryCorner`；iOS 才是 `.systemSmall` 等 |
| 4 | `Multiple commands produce ...YL0veLWatch.app/...`（CopyAndPreserveArchs 冲突） | xcodegen 的 `application.watchapp2` 类型生成的 watch target 缺 build rules | watchOS target 用 **`type: application`** + `platform: watchOS`（见 xcodegen#1257） |
| 5 | watchOS complication 与 watch App 双 `@main` 冲突 | complication 是 WidgetKit，必须独立 extension | 为 complication 建独立 `app-extension` target，`@main WidgetBundle` 放里面；watch App 自身 `@main` 保留 |
| 6 | SwiftUI `Section("标题") { } footer: { }` 编译错（missing argument label 'content:'） | Section 没有 (title, content, footer) 三参数 init | 改用 `Section { } header: { } footer: { }` |
| 7 | `ShareLink` 报 `UIImage does not conform to Transferable` | UIImage 不是 Transferable | 分享用 `pngData()` 的 `Data`（Transferable），预览用 `Image(uiImage:)` |
| 8 | 自定义 `Layout`：`for item in row` 报不满足 Sequence | 遍历了自定义 Row 结构而非 `row.items` | 遍历 `row.items`，布局用 `subviews[item.index].place(...)` |
| 9 | `value of optional type 'HKCategoryValueSleepAnalysis?' must be unwrapped` | 枚举 rawValue 初始化返回可选 | `guard let v = HKCategoryValueSleepAnalysis(rawValue: s.value) else { continue }` |
| 10 | `FetchDescriptor(fetchLimit:)` extra argument | fetchLimit 是属性不是 init 参数 | `var d = FetchDescriptor<T>(); d.fetchLimit = 1` |
| 11 | View 普通方法同步调用 `@MainActor` 服务类 → 编译错误 | 服务类（SwiftData store 等）标了 @MainActor，View 计算属性/方法非隔离 | 相关 View 结构体整体标 `@MainActor` |
| 12 | `call can throw, but it is not marked with 'try'` | async throws API 在 Task 中未 try | `Task { try? await … }` |

### 运行时崩溃 / Runtime Crashes（CI 模拟器才暴露，本地单测可能全绿）

| # | 坑（症状） | 原因 | 修复 |
|---|---|---|---|
| 13 | App 启动即退出、主屏截图、无崩溃报告（`simctl launch` 有 PID 但进程消失） | **倒置 `ClosedRange`**：`dateA...dateB` 当 `dateA > dateB` 时 Swift 运行时 fatalError。典型场景：报告生成循环把"进行中周期"当历史周期，`cycleEnd < cycleStart` | ①修循环索引（最新周期在数组首位时从 index 1 开始）；②区间函数入口 `guard start <= end else { return [] }` 防御 |
| 14 | **`App.init` 里写 SwiftData 导致启动失败（pid 0）** | App 初始化阶段 SwiftData 写入不可靠 | 一切 seed/写入移到 `RootView.onAppear`（主线程 + mainContext） |
| 15 | HealthKit 授权弹窗反复出现、挡住截图 | 多处重复调用 `requestAuthorization`（如 ContentView 与子页 onAppear 各一处） | **授权只保留一处统一入口**；截图场景加环境变量跳过标志 |
| 16 | 系统弹窗（Health 授权）无法用 interruption monitor 点掉 | monitor 触发时机在弹窗出现之前 | **springboard 轮询**：`XCUIApplication(bundleIdentifier: "com.apple.springboard").buttons["Turn On All"/"Allow"]`，循环 `Thread.sleep(2)` + exists 检查 |

### 模拟器启动与截图 / Simulator & Screenshots

| # | 坑 | 修复 |
|---|---|---|
| 17 | `simctl launch` 传 `-skipXxx` 等 `-` 开头参数不稳定（App 不启动） | 改传 **环境变量**：`SIMCTL_CHILD_MY_FLAG=1 xcrun simctl launch ...`（simctl 把 `SIMCTL_CHILD_` 前缀剥掉注入 App 环境）；App 端读 `ProcessInfo.processInfo.environment` |
| 18 | `simctl launch --console-pty` 无输出、看似挂起 | 别用它做诊断；App stdout 诊断用 XCUITest + 崩溃日志 |
| 19 | 主屏出现多个同名/异名图标残留 | install 前先 `xcrun simctl uninstall <udid> <bundle-id>` |
| 20 | 硬编码模拟器名（iPhone 16）→ "Unable to find a device matching the provided destination specifier" | 动态探测：`xcrun simctl list devices available -j` + python 取最后一个可用 iPhone |
| 21 | xcresult 附件导出文件名是 UUID、无法对应页面 | UI test 里把截图直接写 **runner 沙盒 Documents**，用页面名命名；CI `simctl get_app_container` 拷贝 |
| 22 | GitHub artifact 存储配额超限（`Artifact storage quota has been hit`） | 不要依赖 artifact 传递二进制；**截图 commit 回仓库** |
| 23 | `xcodebuild test` 需具体设备而 `build` 可用 generic | 两者 destination 分开写（见 §3.1） |

### 资产与分发 / Assets & Distribution

| # | 坑 | 修复 |
|---|---|---|
| 24 | AppIcon 带 alpha 通道（32bppArgb）不合规 | 转 **1024×1024、24bppRgb（无 alpha）PNG**；Windows 用 .NET System.Drawing 转换（`new Bitmap(w,h,PixelFormat.Format24bppRgb)` + DrawImage） |
| 25 | 免费账号分发：无 TestFlight、7 天签名过期、无 CloudKit | 路径：①Mac 直连 7 天重签 ②AltStore 侧载（Windows 可用，自动续签需同 Wi-Fi）③升级 $99/年解锁 TestFlight（代码零改动） |
| 26 | git 嵌套仓库（clone 参考源码进仓库）→ 外层丢失内容 | `Remove-Item references\<x>\.git -Recurse -Force; git rm -r --cached …` 后再 add |

---

## 7. 完整检查清单 / Final Checklist（新项目启动时逐项过）

- [ ] `project.yml`：SPM 本地包（非 framework target）、watchOS 用 `application`、complication 独立 extension、scheme 含 UI test scheme
- [ ] `.gitignore`：`*.xcodeproj/`、`xcuserdata/`、`DerivedData/`、`*.ipa`；`.gitattributes` 统一 LF
- [ ] Info.plist 权限描述齐全（Health/Speech/Microphone 按需）；AppIcon 1024 无 alpha
- [ ] iOS CI：build=generic、test=动态探测设备名；每次 push 全绿
- [ ] 截图工作流：`permissions: contents: write`；UI test 写 runner 沙盒；CI commit 回仓库
- [ ] 截图参数走 `SIMCTL_CHILD_`/launchEnvironment，且 seed 在 `onAppear` 而非 `App.init`
- [ ] 日期区间/集合构造有防御（`guard lower <= upper`）
- [ ] 授权请求只有一处统一入口
- [ ] git remote 用 SSH；下载二进制用 `curl.exe` + gh token
- [ ] 仓库 visibility 与 Actions 额度匹配（public=免费无限；private=2000 分钟/月）
- [ ] 真机分发路径明确（免费账号：Mac 直连/AltStore；付费：TestFlight）

---

## 8. 关键链接 / References

- XcodeGen：<https://github.com/yonaskolb/XcodeGen>（watchOS 坑：issue #1257）
- Swift Package Manager 本地包：`Package.swift` 放在子目录即可被 xcodegen `packages.path` 引用
- XCUITest 截图与 `XCUIScreen.main.screenshot()`
- `xcrun simctl`（`list devices -j` / `get_app_container` / `SIMCTL_CHILD_` 环境变量注入）
- GitHub CLI：`gh workflow run` / `gh run view --log` / `gh api`（raw 下载二进制）
