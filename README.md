# 说明

已修改默认分支为 `pypi`


## 项目地址

[Bitbucket（最快更新）](https://bitbucket.org/hi-windom/colorthemeanalyse/src/master/ "默认仓库")

[Gitee（最快下载）](https://gitee.com/hi-windom/color-theme-analyse "主要同步仓库")

[Github（计划中）]()

[Pypi](https://pypi.org/project/color-theme-analyse/ "https://pypi.org/project/color-theme-analyse/")

[libraries.io](https://libraries.io/pypi/color-theme-analyse)


## 简介

基于MMCQ对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。

`master` 分支是功能实现的 Simple Demo

`pypi` 分支是 基于master分支重构的 Python Package 打包发布的 Simple Demo

本项目是ImageColorTheme的（MMCQ）具体实现，ImageColorTheme的GitHub（国内镜像）地址：

[GitHub - rainyear/ImageColorTheme: Extract Color Themes from Images (fastgit.org)](https://hub.fastgit.org/rainyear/ImageColorTheme)

本项目同时也是SCMD开源计划的一部分


## 依赖

要求的版本Python>=3.8.0，建议的版本Python==3.9.5

`from multiprocessing import shared_memory required for Python >= 3.8`

要求的操作系统为Windows >= 1909  ( Win 10 / 11 )，建议的版本Windows==22000.71

必要的 Python 第三方库依赖：numpy, opencv-python, pillow, easygui, rich

* [ ] 计划将 `rich` 移植为扩展依赖
* [ ] 计划移除 `opency-python` 依赖

本项目使用了 `React` 框架（非项目构建，只是运行时 `Babel`）

---

# 教程

## 个性化实现

`str(hex(k))[-2:].replace('x', '0').upper()`

本demo处理结果由RGB转为16进制，可根据需要不转换或者转为其他颜色表达形式。

`MMCQ(d, 5)`

本demo默认颜色主题为5个颜色，可根据需要减少或者增加（注意：主题色越多，分析速度越慢）。

本demo限制一次最多处理1020图片，不建议修改，更多图片分批次处理即可
