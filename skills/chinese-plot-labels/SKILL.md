---
name: chinese-plot-labels
description: Use when Codex writes or modifies Python, Java, or C++ code that generates charts, plots, figures, or saved image outputs. If the user has not explicitly specified another language, require Chinese titles, axis labels, and legends in generated result images.
---

# Chinese Plot Labels

## Overview

When producing Python, Java, or C++ code that renders charts or exports image results, default all human-facing chart text to Chinese unless the user explicitly asks for another language.

## Requirements

- Use Chinese for chart titles, subtitles, x/y/z axis labels, colorbar labels, legend entries, annotations that explain plotted series, and saved figure captions rendered inside the image.
- Apply this rule to common plotting libraries, including Python Matplotlib/Seaborn/Pandas/Plotly, Java JFreeChart/JavaFX/processing-style chart output, and C++ matplotlib-cpp/gnuplot/OpenCV/Qt Charts.
- Preserve domain terms, variable names, units, and symbols when translating them would reduce clarity. Prefer Chinese labels with units in parentheses, such as `时间 (s)` or `温度 (deg C)`.
- If the data series names are already meaningful and user-provided, keep their meaning but localize generic names such as `Series 1` to `系列 1`, `Train` to `训练集`, and `Validation` to `验证集`.
- Include font configuration when needed so Chinese text renders correctly in exported images.

## Respect Explicit Instructions

Do not force Chinese labels when the user explicitly requests English, bilingual labels, original-language labels, publication-specific wording, or a required UI/localization convention. In those cases, follow the user's stated language requirement.

## Implementation Notes

- In Python Matplotlib, set an available Chinese font and disable broken minus signs when appropriate, for example `plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]` and `plt.rcParams["axes.unicode_minus"] = False`.
- In Java and C++, set a font family that supports Chinese where the charting library requires explicit font objects.
- Verify examples and tests check the rendered text values, not only that a file was saved.
