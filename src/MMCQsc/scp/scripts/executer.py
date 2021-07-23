# -*- coding=utf-8

# SCSD-PY001

# hi-windom/ColorThemeAnalyse

# https://gitee.com/hi-windom/color-theme-analyse

'''
# ---------------------------------
# 创建于    2021-5-18
# 更新于    2021-7-20 02:10:10
# ---------------------------------
# Need help ?  => 694357845@qq.com
# ---------------------------------
# 处理流程：
# 1.传入路径
# 2.复制路径文件夹的图片 => 粘贴至当前PY文件目录下的prepare文件夹（没有会自动创建）
# 3.压缩prepare文件夹的图片 => 另存至当前PY文件目录下的compress文件夹（没有会自动创建） //这里使用率多进程+多线程，并绑定回调函数testMMCQ执行4.
# 4.分析compress文件夹的图片色彩主题 => 重命名对应的prepare图片文件
# 5.对prepare文件夹的图片生成对应的JSON文件
# 6.[Optional]生成报告
# ---------------------------------
'''
import os,sys
import json
from importlib import import_module
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if root_path not in sys.path:
    sys.path.append(root_path)
from MMCQsc.scp.lib import logger
logger = logger.myLogging("gitee.com/soltus")
# 全局变量
try:
    profile = json.load(open(f'{root_path}\\scp\\scripts\\profile.json', 'r+'))
    themes = profile['themes']
    size_rate = profile['size_rate']
    ignore_size = profile['ignore_size']
except:
    logger.error('./profile.json 配置文件加载失败')

'''
# themes 是分析色彩的结果颜色数量，默认为5
# size_rate 是图片尺寸缩放倍率，默认为10
# ignore_size 是图片压缩忽略阈值（宽/高中的最大值），默认为300
# 推荐在profile.json中修改配置，如有需要也可以修改成传参
'''

from concurrent import futures  # 多进程+多线程，实测速度提升明显，缺点是无法实现rich进度条展示
from multiprocessing import shared_memory
from posixpath import pathsep
import shutil
import datetime
import time  # 导入EasyGui模块，主要用于选择目标文件夹，不需要可以去掉
import urllib.parse as parse
import binascii
import re
from hashlib import md5
# try:
#     import easygui as g
#     import cv2 as cv
#     import numpy as np
#     from PIL import Image
#     from rich import print  # rich用于进度条展示和美化终端输出，不需要可以去掉
#     from rich.console import Console
#     from rich.progress import (
#     BarColumn,
#     Progress,
# )
# except ImportError:
#     raise
class Pgd:
    def __init__(self):
        self.url = 'https://pypi.douban.com/simple/'

    def task(self,im,re):
        self.im = im
        self.re = re
        import os
        repo = input('\n\n Unable to import package [{}] , \n\n Do you want to download ? \n\n\t\tProccess ? [Y/n]\t'.format(self.im))
        if repo in ['Y','y']:
            os.system('cls')
            os.system("pip install {} -i {}".format(self.re, self.url))
            return 1
        return 0

dddd = 0
pgd = Pgd()
try:
    import easygui as g
except ImportError:
    repo = pgd.task(im="easygui",re="easygui")
    dddd += repo

try:
    import cv2 as cv
except ImportError:
    repo = pgd.task(im="cv2",re="opencv-python")
    dddd += repo

try:
    import numpy as np
except ImportError:
    repo = pgd.task(im="numpy",re="numpy")
    dddd += repo

try:
    from PIL import Image
except ImportError:
    repo = pgd.task(im="PIL",re="pillow")
    dddd += repo

try:
    from rich import print
    from rich.console import Console
    from rich.progress import (
    BarColumn,
    Progress,
)
except ImportError:
    repo = pgd.task(im="rich",re="rich")
    dddd += repo


if dddd:
    os.system("cls")
    print(f'\n\t\t{dddd} new packages already installed .\n\n\t\ttry to launch again .\n\n')
    exit()


from MMCQsc.scp.lib.MMCQ import MMCQ # 第一个MMCQ是文件名，第二个是类名

    # from ..lib.logger import *
    # logger = myLogging("gitee.com/soltus")
    # from ..lib.MMCQ import MMCQ  # 第一个MMCQ是文件名，第二个是类名


# 实例化进度条，由于采用多进程+多线程，只能当分隔符使用
progress = Progress(
    BarColumn(bar_width=None)
)

console = Console(color_system='auto', style=None)


def procompress(files, root):
    testshm = shared_memory.SharedMemory(name='main_run_share')
    buf = testshm.buf
    buf[3] += 1
    console.rule(title=' 多进程 ProcessPoolExecutor {:<3}'.format(
                 str(buf[3])), align='center')

    ss = []
    ipl = 0
    for f in files:
        if os.path.splitext(f)[1].lower() in ['.jpg', 'jpeg', '.png']:
            ipl = ipl + 1
            new_file_path = r'%s\%s_%s_%s%s' % (
                os.path.join(BASE_DIR, "src\\prepare"), 'img', ipl, str(int(time.time()*10000)), os.path.splitext(f)[1])
            shutil.copy2(os.path.join(root, f), new_file_path)
            ss.append(new_file_path)

    with futures.ThreadPoolExecutor(max_workers=None) as pool:  # 多线程
        for si in ss:
            results = pool.submit(compressImage, si)
            results.add_done_callback(testMMCQ)  # 回调函数


def compressImage(srcPath):
    # 如果是文件就处理
    if os.path.isfile(srcPath):
        try:
            # 打开原图片缩小后保存，可以用if srcFile.endswith(".jpg")或者split，splitext等函数等针对特定文件压缩
            filename = os.path.basename(srcPath)
            srcFile = srcPath
            dstFile = os.path.join(os.path.join(
                BASE_DIR, "src\\compress"), filename)
            sImg = Image.open(srcFile)
            dImg = sImg.convert('RGB')
            w, h = sImg.size
            MIN_SIZE = 40*40
            # 设置压缩尺寸和选项，注意尺寸要用括号
            if max(w, h) > ignore_size:
                dImg = dImg.resize(
                    (int(w/size_rate), int(h/size_rate)), Image.NEAREST)
            # 尺寸过小需要放大
            elif max(w, h) < MIN_SIZE:
                dImg = dImg.resize(
                    (int(w*2), int(h/size_rate*2)), Image.NEAREST)
            dImg.save(dstFile.replace(filename.split('.')[1], 'jpg'))
            dImg.close()
            sImg.close()
            os.rename(srcFile, srcFile.replace(
                filename.split('.')[1], 'jpg'))  # 不改找不到文件
            return dstFile.replace(filename.split('.')[1], 'jpg')

        except Exception:
            sImg.close()
            sImg = cv.imread(srcFile, 1)
            if max(w, h) > ignore_size:
                dImg = cv.resize(sImg, None, size_rate, size_rate)
            cv.imwrite(dstFile.replace(filename.split('.')[1], 'jpg'), dImg)
            sImg.close
            os.rename(srcFile, srcFile.replace(
                filename.split('.')[1], 'jpg'))  # 不改找不到文件
            return dstFile.replace(filename.split('.')[1], 'jpg')

    # 如果是文件夹就递归
    # if os.path.isdir(srcPath):
    #     for file in srcPath:
    #         compressImage(file)
    # 多进程已做好文件夹递归，传参必是文件


def testMMCQ(future):
    testshm = shared_memory.SharedMemory(name='main_run_share')
    buf = testshm.buf
    if buf[4] < 255:
        buf[4] += 1
    elif buf[5] < 255:
        buf[5] += 1
    elif buf[6] < 255:
        buf[6] += 1
    elif buf[7] < 255:
        buf[7] += 1  # 处理不超过255*4=1020张图片
    thisbuf = str(buf[4] + buf[5] + buf[6] + buf[7])

    imgfile = future.result()
    rgb = list(map(lambda d: MMCQ(d, themes, file=imgfile).quantize(), [cv.imdecode(np.fromfile(
        imgfile, dtype=np.uint8), cv.COLOR_BGR2RGB)]))
    for i in range(len(rgb)):
        strjoin = ''
        for j in range(len(rgb[i])):
            strs = '#'
            for k in rgb[i][j]:
                strs += str(hex(k))[-2:].replace('x', '0').upper()
            strjoin += strs
        console.rule(title='多线程 ThreadPoolExecutor {:<9}  结果 {}\n'.format(
            thisbuf, strjoin.replace('#', ' ')), align='left')
        strjoin += '__{}__'.format(thisbuf + str(int(time.time())))
        filename = os.path.basename(imgfile)
        extname = os.path.splitext(imgfile)[1]
        newname = imgfile.replace(
            'compress', 'prepare').replace(filename, strjoin)
        os.rename(imgfile.replace(
            'compress', 'prepare'), newname + extname)


def domain(img):
    testshm = shared_memory.SharedMemory(name='main_run_share')
    buf = testshm.buf
    with progress:
        task_id = progress.add_task(
            "process", filename="正在多线程分析 ", start=False)

        totaltime = time.time()  # 获取当前文件目录

        # 遍历删除图片
        path = os.path.join(BASE_DIR, "src\\finish")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        path = os.path.join(BASE_DIR, "src\\compress")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        if os.path.exists(os.path.join(BASE_DIR, "src\\reports")) == False:
            os.makedirs(os.path.join(BASE_DIR, "src\\reports"))
        path = os.path.join(BASE_DIR, "src\\prepare\\temp")
        temp = os.path.join(BASE_DIR, "src\\prepare\\temp")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        path = os.walk(os.path.join(BASE_DIR, "src\\prepare"))
        rerule = re.compile(r'\#.{6}\#.{6}\#.{6}\#.{6}\#.{6}\__')
        rerule2 = re.compile(
            r'SCMD-P.*')  # 和定义的命名规则有关
        redoma = 0
        for root, dirs, files in path:
            for f in files:
                if rerule.search(f) or rerule2.search(f):
                    os.remove(os.path.join(root, f))
                else:
                    if root != temp:
                        redoma += 1
                        shutil.move(os.path.join(root, f), temp)
        if redoma > 1:
            progress.update(task_id, visible=False, refresh=False)
            progress.stop()
            os.system('cls')
            redo = input(
                '\n\n\n注意：检测到遗留的 {} 个任务未处理，是否先继续未完成的任务？\n\n  __ 输入 y 继续遗留任务，输入 n 放弃遗留任务，任意其他键退出 __\n'.format(redoma))
            if redo in ['y', 'Y']:
                procompress(os.listdir(temp), temp)
                shutil.rmtree(temp)
            elif redo in ['n', 'N']:
                shutil.rmtree(temp)
                progress.update(task_id, visible=True, refresh=True)
                progress.start_task(task_id)
            else:
                exit()

        if img != None:  # 有传入才处理

            ptv = 0
            origin_list = []
            path = os.walk(os.path.dirname(img))
            for root, dirs, files in path:
                for f in files:
                    if os.path.splitext(f)[1].lower() in ['.jpg', '.jpeg', '.png']:
                        ptv += 1
                        origin_list.append(os.path.join(root, f))
            progress.update(task_id, total=ptv)
            progress.start_task(task_id)
            progress.update(task_id, advance=ptv)
            if ptv > 1019:
                console.rule(title='demo限制单次最多处理 1020 张图片（ {} 张已选择）'.format(
                    ptv), align='center')
                exit()

            # 开始处理

            with futures.ProcessPoolExecutor(max_workers=None) as prolist:
                ffs = []
                roots = []
                path = os.walk(os.path.dirname(img))
                for root, dirs, files in path:
                    ffs.append(files)
                    roots.append(root)

                prolist.map(procompress, ffs, roots)

            while True:  # 定时检测文件夹文件数量
                nowlist = len(os.listdir(
                    os.path.join(BASE_DIR, "src\\finish")))
                time.sleep(2)
                while nowlist != len(os.listdir(
                        os.path.join(BASE_DIR, "src\\finish"))):
                    continue
                buf[1] = 0
                break

            path = os.walk(os.path.join(BASE_DIR, "src\\compress"))
            for root, dirs, files in path:
                for f in files:
                    shutil.move(os.path.join(root, f), os.path.join(
                        BASE_DIR, "src\\finish", f))

            path = os.walk(os.path.join(BASE_DIR, "src\\prepare"))
            for root, dirs, files in path:
                for f in files:
                    fname = os.path.splitext(os.path.basename(f))[0]
                    fnames = fname.split('\\')
                    lastname = fnames[len(fnames) - 1]
                    fname = fname.replace(
                        lastname, re.sub(r'\__.*\__', '', lastname))  # 正则替换

                    curr_time = datetime.datetime.now()
                    with open(os.path.join(root, f), mode="rb") as bf:
                        crc32v = hex(binascii.crc32(bf.read()))[2:].upper()
                        bf.seek(0)
                        md5v = md5(bf.read()).hexdigest()
                    licenseid = "SCMD-P_L1F_" + curr_time.strftime("%Y%m") + \
                        fname.replace("#", "-")
                    jsonstr = {'license': licenseid, 'color': fname, 'theme': fname.split("#")[1:], 'CRC32': crc32v, 'size': os.path.getsize(
                        os.path.join(root, f)), 'date': curr_time.strftime("%Y-%m-%d"), 'time': curr_time.strftime("%H:%M:%S"), 'md5': md5v}
                    dstname = os.path.join(
                        root, licenseid) + os.path.splitext(f)[1]
                    if os.path.exists(dstname):
                        sames = [dstname, os.path.join(root, f), os.path.getsize(
                            dstname), os.path.getsize(os.path.join(root, f))]  # 第二个是当前处理对象
                        issanme = g.buttonbox(msg=f'\n 【疑似重复提醒】 检测到两张图片的色彩主题相同，你有理由怀疑它们是重复的，请检查！\n{sames[0]} \
                            为已存在图片（图片大小{sames[2]}）\n{sames[1]} 为当前待保存图片（图片大小{sames[3]}）\n',
                                              title=' 操作确认 ', choices=(
                                                  ' 保留已存在的 ', ' 我全都要 ', ' 删除已存在的 '), default_choice=None, cancel_choice=' 我全都要 ', images=None)
                        if issanme != ' 我全都要 ':
                            if issanme == ' 保留已存在的 ':
                                os.remove(dstname)
                                with open(os.path.join(root, licenseid) + '.json', 'w') as js:
                                    json.dump(jsonstr, js)
                                os.rename(os.path.join(root, f), dstname)
                            else:
                                os.remove(os.path.join(root, f))
                        else:
                            # 本demo参考SCMD标准，因此不允许重复存在，如有需求可自行修改
                            os.remove(os.path.join(root, f))
                    else:
                        with open(os.path.join(root, licenseid) + '.json', 'w') as js:
                            json.dump(jsonstr, js)
                        os.rename(os.path.join(root, f), dstname)

            progress.stop_task(task_id)

            cost_times = str(round(time.time()-totaltime, 4))
            cc = g.ccbox(msg="\n\n\n" + BASE_DIR + "\n\n\n 总耗时：" +
                         cost_times, title="处理完成", choices=(" 生成报告 ", " 完成 "))

            # 点击生成报告触发事件
            if cc == 1:
                cc1 = shared_memory.SharedMemory(name='main_run_share')
                buf = cc1.buf
                buf[2] = 1
                print('\n\n\n')
                curr_time = datetime.datetime.now()
                # 将路径转为URL格式，不转则json.dump以ASCII格式写到JSON文件里
                in_path_url = parse.quote(
                    os.path.dirname(img), safe=";/?:@&=+$,")
                reportjson = {'date': curr_time.strftime(
                    "%Y-%m-%d"), 'time': curr_time.strftime("%H:%M:%S"), 'in_path_url': in_path_url, 'in_files': ptv, 'cost_times': cost_times}
                reportfile = os.path.join(
                    BASE_DIR, 'src\\reports\\' + curr_time.strftime("%Y%m%d-%H%M%S_")) + 'report.json'
                with open(reportfile, 'w') as js:
                    file_list = []
                    for dir in os.listdir(BASE_DIR + '\\src\\prepare'):
                        child = os.path.join(BASE_DIR + '\\src\\prepare', dir)
                        if os.path.isdir(child):
                            for file in os.listdir(child):
                                if os.path.splitext(file)[1].lower() in ['.jpg', '.jpeg', '.png']:
                                    file = os.path.join(child, file)
                                    if os.path.basename(child) != 'temp':
                                        file_list.append(
                                            file.replace('\\', '/'))
                        elif os.path.isfile(child):
                            if os.path.splitext(child)[1].lower() in ['.jpg', '.jpeg', '.png']:
                                file_list.append(child.replace('\\', '/'))
                    reportjson['origin_list'] = origin_list
                    json.dump(reportjson, js)
                    console.print(reportjson, justify='full',
                                  highlight=True)
                    for i in range(len(file_list)):
                        file_list[i] = str(file_list[i]).replace(
                            BASE_DIR.replace('\\', '/') + '/src/', '')
                    with open(os.path.join(BASE_DIR, 'src/index.js'), 'w', encoding='utf-8') as mainjs:
                        mainjs.write(
                            'class ImgShow extends React.Component {\n render() {\n return (<div id="imgbox"><div className="imgshow1" >\n')
                    with open(os.path.join(BASE_DIR, 'src/index.js'), 'a', encoding='utf-8') as mainjs:
                        img1 = len(file_list) // 2
                        img2_w = False
                        i = 0
                        shutil.copy2(os.path.join(
                            BASE_DIR, 'src/_css/base.css'), os.path.join(BASE_DIR, 'src/index.css'))
                        for name in file_list:
                            i += 1
                            if rerule2.search(os.path.splitext(name)[0]):
                                colors = rerule2.search(os.path.splitext(name)[
                                    0]).group().split('-')
                            else:
                                colors = ['', '', 'FFFFFF', 'FFFFFF',
                                          'FFFFFF', 'FFFFFF', 'FFFFFF']  # 意外处理
                            if len(colors) != 7:
                                print(colors)
                                print('格式有误')
                            else:
                                if i <= img1 and img2_w == False:
                                    mainjs.writelines(
                                        r'<div className="colorbox wow fadeIn" data-wow-delay="0.2s" data-wow-duration="0.5s" data-wow-offset="20">')
                                    with open(os.path.join(BASE_DIR, 'src/index.css'), 'a', encoding='utf-8') as maincss:
                                        maincss.writelines('\n')
                                        for c in range(1, 6):
                                            mainjs.writelines(
                                                r'<div id = "t{}c{}"></div>'.format(i, c))
                                            maincss.writelines(
                                                '#t{}c{} {{\nmax-width: 20%; min-width: 20%; width: 20%; height: 40px; background-color: #{}; display: inline-block; z-index: 99;\n}}\n'.format(i, c, colors[c+1]))
                                    mainjs.writelines('</div>\n')
                                    mainjs.writelines(
                                        r'<img className="img wow fadeIn" data-wow-delay="0.2s" data-wow-duration="0.5s" data-wow-offset="20" src={"' + name + r'"} />' + '\n')
                                else:
                                    if img2_w == False:
                                        mainjs.writelines(
                                            '</div>\n<div className='"'imgshow2'"'>\n')
                                        img2_w = True
                                    mainjs.writelines(
                                        r'<div className="colorbox wow fadeIn" data-wow-delay="0.2s" data-wow-duration="0.5s" data-wow-offset="20">')
                                    with open(os.path.join(BASE_DIR, 'src/index.css'), 'a', encoding='utf-8') as maincss:
                                        maincss.writelines('\n')
                                        for c in range(1, 6):
                                            mainjs.writelines(
                                                r'<div id = "t{}c{}"></div>'.format(i, c))
                                            maincss.writelines(
                                                '#t{}c{} {{\nmax-width: 20%; min-width: 20%; width: 20%; height: 40px; background-color: #{}; display: inline-block; z-index: 99;\n}}\n'.format(i, c, colors[c+1]))
                                    mainjs.writelines('</div>\n')
                                if img2_w == True:
                                    mainjs.writelines(
                                        r'<img className="img wow fadeIn" data-wow-delay="0.2s" data-wow-duration="0.5s" data-wow-offset="20" src={"' + name + r'"} />' + '\n')
                        mainjs.writelines(
                            '</div>\n</div> ); \n}}\n\nReactDOM.render(<ImgShow / >,document.getElementById('"'imgs'"')); ')
                        with open(os.path.join(BASE_DIR, 'src/_js/base.js'), 'r+', encoding='utf-8') as index:
                            index.seek(0)
                            index_text = index.read()
                            rf = re.sub(r'^.*\\src', './',
                                        reportfile).replace('\\', '/')
                            index_text = index_text.replace(
                                '[[reportpath]]', rf)
                            mainjs.writelines(index_text)


# if __name__ == '__main__':
#     # fileopenbox()函数的返回值是你选择的那个文件的具体路径
#     if 'img' in dir():
#         pass
#     else:
#         img = g.fileopenbox('open file' + '会导入当前文件夹的全部图片')
#         domain(img)
