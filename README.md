项目依赖比较简单，推荐使用无依赖安装：

`pip install color-theme-analyse --no-deps`

如果你设置了全局镜像，请使用以下的命令安装：

`pip install color-theme-analyse --no-deps -i https://pypi.org.simple`

### 项目地址

[Bitbucket（最快更新）](https://bitbucket.org/hi-windom/colorthemeanalyse/src/master/ "默认仓库")

[Gitee（最快下载）](https://gitee.com/hi-windom/color-theme-analyse "主要同步仓库")

[Github（仅同步PyPi分支）](https://github.com/Soltus/color-theme-analyse)

[GitLab](https://gitlab.com/liaoshanyi/ColorThemeAnalyse)

[Pypi](https://pypi.org/project/color-theme-analyse/ "https://pypi.org/project/color-theme-analyse/")

[libraries.io](https://libraries.io/pypi/color-theme-analyse)

已修改默认分支为 `pypi`

`master` 分支已停止维护

源仓库在 Bitbucket，因此会首先得到同步

Bug 反馈和 Issues 提交可以在 Bitbucket 或者 Gitee，**在 Gitee 会得到最快反馈**

请勿在 Github 或 GitLab 提交 Issues ，它们只是同步仓库，不会处理任何提交的 Issues

### 简介

基于MMCQ对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。

`master` 分支是功能实现的 Simple Demo

`pypi` 分支是 基于master分支重构的 Python Package 打包发布的 Simple Demo

本项目是ImageColorTheme的（MMCQ）具体实现，ImageColorTheme的GitHub（国内镜像）地址：

[GitHub - rainyear/ImageColorTheme: Extract Color Themes from Images (fastgit.org)](https://hub.fastgit.org/rainyear/ImageColorTheme)

本项目同时也是SCMD开源计划的一部分

### Requires

要求的版本 3.10.0 > Python >= 3.8.0

建议的版本 Python == 3.9.5

`from multiprocessing import shared_memory required for Python >= 3.8`

要求的操作系统 Windows >= 1909  ( Win 10 / 11 )

建议的操作系统 Windows>=22000.100（ Win 11 Dev ）

必要的 Python 第三方库依赖：numpy, opencv-python, pillow, easygui, rich

本项目使用了 `React` 框架（非项目构建，只是运行时 `Babel`）

---

# 教程

### Build

### Feature

### Customize

`str(hex(k))[-2:].replace('x', '0').upper()`

本demo处理结果由RGB转为16进制，可根据需要不转换或者转为其他颜色表达形式。

`MMCQ(d, 5)`

本demo默认颜色主题为5个颜色，可根据需要减少或者增加（注意：主题色越多，分析速度越慢）。

本demo限制一次最多处理1020图片，不建议修改，更多图片分批次处理即可

### Scheme

计划将 `rich` 移植为扩展依赖

计划移除 `opency-python` 依赖

# 目录树

src
├─ MMCQsc
│  ├─ scp
│  │  ├─ lib
│  │  │  ├─ error_sc.py
│  │  │  ├─ logger.py
│  │  │  ├─ MMCQ.py
│  │  │  └─ __init__.py
│  │  ├─ scripts
│  │  │  ├─ executer.py
│  │  │  ├─ profile.json
│  │  │  └─ __init__.py
│  │  ├─ executable_check.py
│  │  ├─ main.py
│  │  └─ __init__.py
│  ├─ src
│  │  ├─ _css
│  │  │  ├─ animate.css
│  │  │  ├─ base.css
│  │  │  └─ sweet-alert.css
│  │  ├─ _js
│  │  │  ├─ babel.min_5.8.23.js
│  │  │  ├─ base.js
│  │  │  ├─ react-dom.development.js
│  │  │  ├─ react.development.js
│  │  │  ├─ sweet-alert.js
│  │  │  ├─ wow.min.js
│  │  │  └─ wow.min2.js
│  │  ├─ gitee.svg
│  │  ├─ index.css
│  │  ├─ index.html
│  │  └─ index.js
│  ├─ color_theme_analyse.py
│  ├─ version.py
│  └─ __init__.py
└─ MMCQsc.cmd
