# Sh_Sci_Fig 使用指南

## 简介

Sh_Sci_Fig 是一个用于从学术 PDF 论文中精准提取图表和子图的工具。它能够自动识别图号、分割组合图中的各个子图，并以高质量 PNG 格式输出。

## 功能特性

- **自动图表检测** — 定位 Figure N / 图 N 等图号标题，自动确定图表边界
- **子图分割** — 将组合图分割成单个面板 (a), (b), (c)... 使用白空间分析 + OCR
- **高质量输出** — 可配置分辨率渲染（默认 600 DPI），适合论文发表
- **智能降级** — OCR 失败时自动降级到基于标题的网格分割

## 安装

### 前置要求

- Python 3.9+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
  - Windows: winget install UB-Mannheim.TesseractOCR
  - Linux: pt install tesseract-ocr
  - macOS: rew install tesseract

### 安装步骤

`ash
git clone https://github.com/xssjqx/Sh_Sci_Fig.git
cd Sh_Sci_Fig
pip install -r requirements.txt
`

## 快速开始

### 提取指定图表

`ash
python scripts/extract_figure.py paper.pdf -f 3
`

输出: igure_3.png

### 提取子图

`ash
python scripts/extract_figure.py paper.pdf -f 2 -s c
`

输出: igure_2c.png（只提取图 2 的 c 部分）

### 列出所有可用图表

`ash
python scripts/extract_figure.py paper.pdf --list
`

输出:
`
Available figures: 1, 2a, 2b, 2c, 3, 4a, 4b, 5
`

### 提取所有图表

`ash
python scripts/extract_figure.py paper.pdf --all -o ./output/
`

输出: igure_1.png, igure_2a.png, igure_2b.png, ...

### 自定义分辨率和格式

`ash
python scripts/extract_figure.py paper.pdf -f 2 -s c -o ./output/ -d 300 --format jpg
`

## 命令行选项

| 选项 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| <input> | | PDF 文件路径 | 必需 |
| --figure | -f | 要提取的图号（1, 2, 3...） | 必需* |
| --subfigure | -s | 子图标签（a, b, c...） | 无 |
| --output | -o | 输出目录 | 当前目录 |
| --dpi | -d | 输出分辨率 | 600 |
| --list | -l | 列出所有可用图表 | |
| --all | | 提取所有图表 | |
| --format | | 输出格式（png 或 jpg） | png |
| --quiet | -q | 抑制信息输出 | |

*除非使用 --list 或 --all

## 输出文件命名

| 模式 | 文件名 |
|------|--------|
| 完整图表 | igure_3.png |
| 子图 | igure_3c.png |

## 工作原理

1. **文本提取** — 使用 pdfplumber 从每一页提取所有文本及其坐标
2. **图号检测** — 正则表达式匹配 Fig. N / Figure N 等模式定位图号
3. **边界计算** — 分析文本间隙确定图表区域
4. **页面渲染** — PyMuPDF 以高 DPI 渲染页面，然后裁剪图表区域
5. **子图分割** — 白空间投影分析找到网格结构；OCR + 标签识别分配面板标识符

## 常见问题

### Q: 为什么提取的图表质量不好？

**A:** 尝试调整 DPI：
`ash
python scripts/extract_figure.py paper.pdf -f 2 -d 1200
`

DPI 越高质量越好，但文件也会更大。推荐值：
- 屏幕查看: 300 DPI
- 论文发表: 600-1200 DPI

### Q: 子图分割失败怎么办？

**A:** 如果 OCR 识别失败，工具会自动返回整个图表区域。可以：
1. 检查 Tesseract 是否正确安装
2. 尝试手动指定子图（如果支持）
3. 使用 --quiet 查看详细错误日志

### Q: 支持扫描版 PDF 吗？

**A:** 目前优先支持矢量版 PDF。扫描版 PDF 可能因为 OCR 准确率问题导致识别失败。

### Q: 如何批量处理多个 PDF？

**A:** 使用 shell 脚本：
`ash
for pdf in *.pdf; do
    python scripts/extract_figure.py   --all -o ./output/
done
`

## 错误处理

| 场景 | 行为 |
|------|------|
| PDF 不存在 | 清晰的错误提示和文件路径 |
| PDF 加密 | 错误提示建议使用解密版本 |
| 图号不存在 | 错误提示并列出所有可用图号 |
| OCR 失败 | 自动降级到网格分割 |
| 子图分割失败 | 返回整个图表区域并显示警告 |

## 依赖库

| 库 | 用途 |
|----|------|
| [pdfplumber](https://github.com/jsvine/pdfplumber) | 文本 + 坐标提取 |
| [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) | PDF → 高质量图像渲染 |
| [opencv-python](https://opencv.org/) | 边界检测、轮廓分析 |
| [Pillow](https://pillow.readthedocs.io/) | 图像格式转换 |
| [pytesseract](https://github.com/madmaze/pytesseract) | OCR 子图标签识别 |
| [NumPy](https://numpy.org/) | 数组操作 |

## 许可证

AGPL-3.0-or-later — 详见 [LICENSE](LICENSE)

**注意**: 本项目使用 PyMuPDF (fitz)，其许可证为 AGPL v3。因此整个项目也必须采用 AGPL v3 或更高版本。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请在 [GitHub Issues](https://github.com/xssjqx/Sh_Sci_Fig/issues) 中提出。
