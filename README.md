# 说明

源码地址

[bitbucket（最快更新）](https://bitbucket.org/hi-windom/colorthemeanalyse/src/master/)

[gitee](https://gitee.com/hi-windom/color-theme-analyse)

## 简介

基于MMCQ对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。

> 多进程下难以实现进度条，因此可去掉

本项目是ImageColorTheme的（MMCQ）具体实现，ImageColorTheme的GitHub（国内镜像）地址：

[GitHub - rainyear/ImageColorTheme: Extract Color Themes from Images (fastgit.org)](https://hub.fastgit.org/rainyear/ImageColorTheme)

## 库依赖（不包括PY3自带）

要求Python版本高于3.9.0

必要：

`pip install numpy -i https://pypi.douban.com/simple`

> `import numpy as np`

`pip install opencv-python -i https://pypi.douban.com/simple`

> `import cv2 as cv`
>
> `from cv2 import data`

`pip install Pillow -i https://pypi.douban.com/simple` ~~(PIL)~~

> `from PIL import Image`

可选：

`pip install easygui -i https://pypi.douban.com/simple`

`pip install rich -i https://pypi.douban.com/simple`

---

## 个性化实现

`str(hex(k))[-2:].replace('x', '0').upper()`

本demo处理结果由RGB转为16进制，可根据需要不转换或者转为其他颜色表达形式。

`MMCQ(d, 5)`

本demo默认颜色主题为5个颜色，可根据需要减少或者增加（注意：主题色越多，分析速度越慢）。

本demo建议一次处理30~1000图片，图片数量过少本demo无速度优化，图片过多尚未测试。
