# -*- coding=utf-8
from hashlib import md5
import json
import binascii
from PIL import Image
import numpy as np
import cv2 as cv
from cv2 import data
from MMCQ import MMCQ  # 需要MMCQ.py文件在同一目录下
from rich.progress import (
    BarColumn,
    Progress,
)
from rich.console import Console
from rich import print  # rich用于进度条展示和美化终端输出，不需要可以去掉
import easygui as g  # 导入EasyGui模块，主要用于选择目标文件夹，不需要可以去掉
import time
import datetime
import os
import shutil
from concurrent import futures  # 多进程+多线程，实测速度提升明显，缺点是无法实现rich进度条展示
'''
---------------------------------
创建于2021/5/18
更新于2021/5/18 11:26
---------------------------------
Need help ?  => 694357845@qq.com
---------------------------------
处理流程：
1.传入路径
2.复制路径文件夹的图片 => 粘贴至当前PY文件目录下的prepare文件夹（没有会自动创建）
3.压缩prepare文件夹的图片 => 另存至当前PY文件目录下的compress文件夹（没有会自动创建） //这里使用率多进程+多线程，并绑定回调函数testMMCQ执行4.
4.分析compress文件夹的图片色彩主题 => 重命名对应的prepare图片文件
5.对prepare文件夹的图片生成对应的JSON文件
6.[Optional]生成报告
---------------------------------
'''

# 实例化进度条，由于采用多进程+多线程，只能当分隔符使用
progress = Progress(
    BarColumn(bar_width=None)
)

console = Console(color_system='auto', style=None)


def compressImage(srcPath):
    base_dir = os.path.dirname(__file__)   # 获取当前文件目录
    # 如果是文件就处理
    if os.path.isfile(srcPath):
        try:
            # 打开原图片缩小后保存，可以用if srcFile.endswith(".jpg")或者split，splitext等函数等针对特定文件压缩
            filename = os.path.basename(srcPath)
            srcFile = srcPath
            dstFile = os.path.join(os.path.join(
                base_dir, "compress"), filename)
            sImg = Image.open(srcFile)
            dImg = sImg.convert('RGB')
            w, h = sImg.size
            # 设置压缩尺寸和选项，注意尺寸要用括号
            if max(w, h) > 200:
                dImg = dImg.resize((int(w/10), int(h/10)), Image.BILINEAR)
            dImg.save(dstFile, quality=80)

            return dstFile

        except Exception:
            dImg = sImg.convert('RGBA')
            dImg = sImg.quantize(colors=256)
            if max(w, h) > 200:
                dImg = dImg.resize((int(w/10), int(h/10)), Image.BILINEAR)
            dImg.save(dstFile)
            return dstFile

            # 如果是文件夹就递归
    if os.path.isdir(srcPath):
        for file in srcPath:
            compressImage(file)


def testMMCQ(future):
    imgfile = future.result()
    start = time.process_time()
    rgb = list(map(lambda d: MMCQ(d, 5).quantize(), [cv.imdecode(np.fromfile(
        imgfile, dtype=np.uint8), cv.COLOR_BGR2RGB)]))

    for i in range(len(rgb)):
        strjoin = ''
        for j in range(len(rgb[i])):
            strs = '#'
            for k in rgb[i][j]:

                strs += str(hex(k))[-2:].replace('x', '0').upper()
            strjoin += strs
        console.print(strjoin.replace('#', ' '), justify='center')
        filename = os.path.basename(imgfile)
        extname = os.path.splitext(imgfile)[1]
        newname = imgfile.replace(
            'compress', 'prepare').replace(filename, strjoin)
        os.rename(imgfile.replace(
            'compress', 'prepare'), newname + extname)


def procompress(files, root):
    base_dir = os.path.dirname(__file__)   # 获取当前文件目录

    pool = futures.ThreadPoolExecutor(max_workers=None)
    ss = []
    ipl = 0
    for f in files:
        if os.path.splitext(f)[1] != '.gif':
            ipl = ipl + 1
            new_file_path = r'%s\%s_%s_%s%s' % (
                os.path.join(base_dir, "prepare"), 'img', ipl, str(int(time.time()*10000)), os.path.splitext(f)[1])
            shutil.copy2(os.path.join(root, f), new_file_path)
            ss.append(new_file_path)

    for si in ss:
        results = pool.submit(compressImage, si)
        results.add_done_callback(testMMCQ)

    pool.shutdown(wait=True)


with progress:
    if __name__ == '__main__':
        task_id = progress.add_task(
            "process", filename="正在多线程分析 ", start=False)
        # fileopenbox()函数的返回值是你选择的那个文件的具体路径
        img = g.fileopenbox('open file' + '会导入当前文件夹的全部图片')
        totaltime = time.time()
        base_dir = os.path.dirname(__file__)   # 获取当前文件目录

        # 遍历删除图片
        path = os.path.join(base_dir, "finish")
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        path = os.walk(path)
        for root, dirs, files in path:
            for f in files:
                os.remove(os.path.join(root, f))

        path = os.path.join(base_dir, "prepare")
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        path = os.walk(path)
        for root, dirs, files in path:
            for f in files:
                os.remove(os.path.join(root, f))

        path = os.path.join(base_dir, "compress")
        if os.path.exists(path):
            pass
        else:
            os.mkdir(path)
        path = os.walk(path)
        for root, dirs, files in path:
            for f in files:
                os.remove(os.path.join(root, f))

        if img != None:  # 有传入才处理

            ptv = 0
            path = os.walk(os.path.dirname(img))
            for root, dirs, files in path:
                for f in files:
                    ptv += 1
            progress.update(task_id, total=ptv)
            progress.start_task(task_id)
            progress.update(task_id, advance=ptv)

            # 开始处理

            prolist = futures.ProcessPoolExecutor(max_workers=None)
            ffs = []
            roots = []
            path = os.walk(os.path.dirname(img))
            for root, dirs, files in path:
                ffs.append(files)
                roots.append(root)

            prolist.map(procompress, ffs, roots)

            prolist.shutdown(wait=True)

            path = os.walk(os.path.join(base_dir, "compress"))
            for root, dirs, files in path:
                for f in files:
                    shutil.move(os.path.join(root, f), os.path.join(
                        base_dir, "finish", f))

            path = os.walk(os.path.join(base_dir, "prepare"))
            for root, dirs, files in path:
                for f in files:
                    fname = os.path.splitext(os.path.basename(f))[0]

                    curr_time = datetime.datetime.now()
                    with open(os.path.join(root, f), mode="rb") as bf:
                        crc32v = hex(binascii.crc32(bf.read()))[2:].upper()
                        bf.seek(0)
                        md5v = md5(bf.read()).hexdigest()
                        bf.close
                    licenseid = "SCMD-P_L1F_" + curr_time.strftime("%Y%m") + \
                        fname.replace("#", "-")
                    jsonstr = {'license': licenseid, 'color': fname, 'theme': fname.split("#")[1:], 'CRC32': crc32v, 'size': os.path.getsize(
                        os.path.join(root, f)), 'date': curr_time.strftime("%Y-%m-%d"), 'time': curr_time.strftime("%H:%M:%S"), 'md5': md5v}
                    with open(os.path.join(root, licenseid) + '.json', 'w') as js:
                        json.dump(jsonstr, js)
                        js.close
                    os.rename(os.path.join(root, f), os.path.join(
                        root, licenseid) + os.path.splitext(f)[1])
            progress.stop_task(task_id)
            cc = g.ccbox(msg="\n\n\n" + base_dir + "\n\n\n 总耗时：" +
                         str(time.time()-totaltime), title="处理完成", choices=("生成报告", "完成"))

            # 点击生成报告触发事件
            if cc == 1:
                import Upload_FileInPath
