# Claude Code Skill: Bug Bounty 全流程工作流

面向补天/SRC 等**授权范围内**漏洞挖掘的 Claude Code 技能包:侦察 → 挖掘 → 验证 → 报告 全流程自动化。

## 功能

- 5 阶段工作流:授权确认 → 侦察 → 挖掘 → 验证 → 报告,每阶段产出工件并与用户确认
- 自动化侦察脚本:子域收集(subfinder + crt.sh)、历史 URL(gau)、存活探测与指纹(httpx)、端口扫描(nmap)、Nuclei 模板扫描
- 10 类 Web 漏洞实战测试清单:认证绕过、越权、业务逻辑、SQLi、XSS、SSRF、文件上传、信息泄露等
- 补天格式报告模板 + 提交前自检清单
- 内置合规红线:只测授权资产、数据最小化、不做破坏性测试

## 安装

克隆到 Claude Code 的 skills 目录:

```bash
# Windows (Git Bash) / macOS / Linux 通用
git clone https://github.com/<你的用户名>/bugbounty-workflow.git ~/.claude/skills/bugbounty-workflow
```

重启 Claude Code 会话后生效。

## 使用

- 输入 `/bugbounty-workflow`,或直接说"帮我挖 XX 的漏洞(补天授权范围内)"
- 流程强制从授权确认开始,每个阶段结束会与你确认后再进入下一阶段

## 依赖工具(可选,缺失会自动跳过)

| 用途 | 工具 |
|---|---|
| 侦察 | subfinder、httpx、nuclei、gau、nmap |
| 挖掘 | dirsearch、ffuf、sqlmap、Burp Suite |
| 带外交互 | dnslog.cn 或 interactsh-client |

## 目录结构

```
├── SKILL.md                          # 主工作流(5 阶段 + 合规铁律)
├── scripts/
│   └── recon.sh                      # 自动化侦察脚本
├── checklists/
│   └── web-vuln-checklist.md         # 10 类漏洞实战测试清单
└── templates/
    └── report-template.md            # 补天格式报告模板
```

## ⚠️ 免责声明

本工具**仅限合法授权的安全测试**使用(如补天、企业 SRC 等平台授权范围内)。
使用者须自行确保测试行为符合平台规则与所在地法律法规。
未经授权对他人系统进行测试属于违法行为,后果由使用者自行承担。
