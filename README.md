<p align="center">
    <a href="https://pypi.org/project/color-theme-analyse/"><img src="https://img.shields.io/pypi/v/color-theme-analyse.svg" alt="PyPI Version"></a>
    <a href="https://pypi.org/project/color-theme-analyse/"><img src="https://img.shields.io/pypi/pyversions/color-theme-analyse.svg" alt="PyPI Supported Versions"></a>
    <a href="https://pypi.org/project/color-theme-analyse/"><img src="https://img.shields.io/pypi/l/color-theme-analyse.svg" alt="License"></a>
    <a href="https://pypi.org/project/color-theme-analyse/"><img src="https://img.shields.io/badge/Internal%20code-SCSD--PY001-ff69b4"></a>
    <a href="https://pypi.org/project/color-theme-analyse/"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/color-theme-analyse?label=pypi%20downloads"></a>
    <a href="https://pepy.tech/project/color-theme-analyse"><img src="https://static.pepy.tech/badge/color-theme-analyse" alt="Downloads"></a>
    <a href="https://pepy.tech/project/color-theme-analyse"><img src="https://static.pepy.tech/badge/color-theme-analyse/month" alt="Downloads Per Month"></a>
    <a href="https://pyinstaller.readthedocs.io/en/stable/requirements.html"><img src="https://img.shields.io/badge/platform-windows%20%7C%20linux-lightgrey" alt="Supported Platforms"></a>
    <a href="https://pypi.org/project/color-theme-analyse/"><img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/color-theme-analyse"></a>
    <a href="https://pypi.org/project/color-theme-analyse/"><img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/color-theme-analyse"></a>
    <a href="https://bitbucket.org/hi-windom/colorthemeanalyse/addon/pipelines/home#!/results/page/1"><img alt="Bitbucket Pipelines" src="https://img.shields.io/bitbucket/pipelines/hi-windom/colorthemeanalyse/dev2022"></a>
    <a href="https://github.com/Soltus/color-theme-analyse"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/soltus/color-theme-analyse?label=GitHub%20last%20commit"></a>
    <a href="https://github.com/Soltus/color-theme-analyse"><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/y/soltus/color-theme-analyse?label=GitHub%20commit%20activity"></a>
    <a href="https://github.com/Soltus/color-theme-analyse"><img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/soltus/color-theme-analyse?label=GitHub%20code%20size"></a>
    <a href="https://github.com/Soltus/color-theme-analyse"><img alt="GitHub language count" src="https://img.shields.io/github/languages/count/soltus/color-theme-analyse"></a>
    <a href="tencent://AddContact/?fromId=45&fromSubId=1&subcmd=all&uin=694357845&website=www.oicqzone.com"><img src="https://img.shields.io/badge/QQ-694357845-orange"></a>
</p>

项目依赖比较简单，可以使用无依赖安装：

`pip install color-theme-analyse --no-deps`

如果你设置的全局镜像未收录本项目，请使用以下的命令从官方仓库安装或者手动指定镜像：

`pip install color-theme-analyse --no-deps -i https://pypi.org/simple`

以下镜像收录了本项目：

* [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)
* [http://pypi.douban.com/simple](http://pypi.douban.com/simple)
* [https://mirrors.tencent.com/pypi/simple](https://mirrors.tencent.com/pypi/simple)
* [http://mirrors.aliyun.com/pypi/simple/](http://mirrors.aliyun.com/pypi/simple/)

如果你使用的是校园网，可以使用腾讯镜像下载本项目

`pip install color-theme-analyse[base] -i https://mirrors.tencent.com/pypi/simple`

---

**如果出于pypi学习目的首次下载，建议使用下面的下载命令：（推荐）**

`pip install color-theme-analyse[base,dev] -i https://mirrors.tencent.com/pypi/simple`

等效于 `pip install color-theme-analyse[merge] -i https://mirrors.tencent.com/pypi/simple`

**安装后使用终端命令 `MMCQsc`运行**

支持以下终端命令（Linux平台需要注意大小写）：

```bash
MMCQsc
RunMMCQsc
DoMMCQsc
MMCQscPure
MMCQscR
MMCQscR1
MMCQscR2
```

---

### 项目地址

[Gitee](https://gitee.com/hi-windom/color-theme-analyse "主要同步仓库") 

[Github](https://github.com/Soltus/color-theme-analyse)（偶尔同步）

[GitLab](https://gitlab.com/liaoshanyi/ColorThemeAnalyse)（偶尔同步）

[GitCode](https://gitcode.net/Soltus/color-theme-analyse)

[Pypi](https://pypi.org/project/color-theme-analyse/ "https://pypi.org/project/color-theme-analyse/")（官方仓库）

[libraries.io](https://libraries.io/pypi/color-theme-analyse)（同步官方仓库）

下载所有源文件 -> [Links for color-theme-analyse (tencent.com)](https://mirrors.tencent.com/pypi/simple/color-theme-analyse/)

当前默认分支为 `dev2022`

`master，pypi` 分支已停止维护

源仓库在 Bitbucket，因此会首先得到同步

Bug 反馈和 Issues 提交在Gitee或Github，**在 Gitee 会得到最快反馈**

请勿在 Github 或 GitLab 提交 Issues ，它们只是同步仓库，不会处理任何提交的 Issues

### 简介

基于MMCQ对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。

`master` 分支是功能实现的 Simple Demo

`pypi` 分支是 基于master分支重构的 Python Package 打包发布的 Simple Demo

`embed` 分支是 基于 pypi分支重构的 嵌入式版本 Simple Demo

本项目是ImageColorTheme的（MMCQ）具体实现，ImageColorTheme的GitHub（国内镜像）地址：

[GitHub - rainyear/ImageColorTheme: Extract Color Themes from Images (fastgit.org)](https://hub.fastgit.org/rainyear/ImageColorTheme)

本项目同时也是SCMD开源计划的一部分

### Requires

**要求的版本 3.10.0 > Python >= 3.9.0**

建议的版本 Python == 3.9.5

> from multiprocessing import shared_memory required for Python >= 3.8

要求的操作系统 Windows >= 1909  ( Win 10 / 11 )

建议的操作系统 Windows>=22000.100（ Win 11 Dev ）

必要的 Python 第三方库依赖：numpy, opencv-python, pillow, ~~easygui~~, rich

本项目使用了 `React` 框架（非项目构建，只是运行时 `Babel`）

---

# 教程

### Build

`python setup.py bdist_wheel`

调试请运行 color_theme_analyse.py

这是为 Windows 平台专门开发的，无法在 Linux 中获得完美体验，同时可能存在部分兼容问题

### Feature

### Customize

`str(hex(k))[-2:].replace('x', '0').upper()`

本demo处理结果由RGB转为16进制，可根据需要不转换或者转为其他颜色表达形式。

`MMCQ(d, 5)`

本demo默认颜色主题为5个颜色，可根据需要减少或者增加（注意：主题色越多，分析速度越慢）。

本demo限制一次最多处理1020图片，不建议修改，更多图片分批次处理即可

### Scheme

* [X] embed 版本：Pillow 更换为嵌入版本，Numpy, rich 改为动态引用，弃用 OpenCV-Python
