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
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".."))
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc','src'))
DPKG_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc_dpkg'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
if DPKG_DIR not in sys.path:
    sys.path.append(DPKG_DIR)
from MMCQsc.scp.lib import logger
logger = logger.myLogging("gitee.com/soltus")
# 全局变量
try:
    profile = json.load(open(os.path.abspath(os.path.join(BASE_DIR,'MMCQsc','scp','scripts','profile.json')), 'r+'))
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
import shutil
import datetime
import time
import urllib.parse as parse
import binascii
import re
from hashlib import md5

if os.name == 'posix':
    CLS = 'clear'
    DIR_SPLIT = '/'
else:
    CLS = 'cls'
    DIR_SPLIT = '\\'
class Pgd:
    def __init__(self):
        self.url = 'https://pypi.douban.com/simple/'

    def task(self,im,re):
        self.im = im
        self.re = re
        import os
        repo = input('\n\n Unable to import package [{}] from \n\t{} , \n\n Do you want to download ? \n\n\t\tProccess ? [Y/n]\t'.format(self.im, sys.path))
        if repo in ['Y','y']:
            os.system('cls')
            os.system("pip install {} -i {}".format(self.re, self.url))
            return 1
        return 0

dddd = 0
pgd = Pgd()



try:
    np = __import__('numpy', globals(), locals(), [], 0)
except ImportError:
    try:
        from MMCQsc_dpkg import numpy as np
    except:
        repo = pgd.task(im="numpy",re="numpy")
        dddd += repo
try:
    from MMCQsc_dpkg.PIL import Image as PImage
except ImportError:
    try:
        PIL = __import__('PIL', globals(), locals(), [], 0)
        from PIL import Image as PImage
    except:
        repo = pgd.task(im="PIL",re="Pillow")
        dddd += repo
try:
    # logger.debug("from rich import print")
    from rich import print
    # logger.debug("from rich.console import Console")
    from rich.console import Console
    from rich.progress import (BarColumn,Progress,) # 实例化进度条，由于采用多进程+多线程，只能当分隔符使用
except ImportError:
    try:
        # logger.debug("from MMCQsc_dpkg.rich import print")
        from MMCQsc_dpkg.rich import print
        # logger.debug("from MMCQsc_dpkg.rich.console import Console")
        from MMCQsc_dpkg.rich.console import Console
        from MMCQsc_dpkg.rich.progress import (BarColumn,Progress,) # 实例化进度条，由于采用多进程+多线程，只能当分隔符使用
    except Exception as e:
        logger.error(e)
        repo = pgd.task(im="rich",re="rich")
        dddd += repo
'''
embed 版本：Pillow 更换为嵌入版本，Numpy, rich 改为动态引用，弃用 OpenCV-Python
'''


if dddd:
    os.system(CLS)
    logger.info(f'\n\t\t{dddd} new packages already installed .\n\n\t\ttry to launch again .\n\n')
    sys.exit()

from MMCQsc.scp.lib.MMCQ import MMCQ # 第一个MMCQ是文件名，第二个是类名


progress = Progress(
        BarColumn(bar_width=None)
    )

console = Console(color_system='auto', style=None)



def procompress(files, root):
    testshm = shared_memory.SharedMemory(name='main_run_share')
    buf = testshm.buf
    buf[3] += 1
    console.rule(title=' 多进程 ProcessPoolExecutor {:<3} \t "./profile.json 配置文件加载成功"'.format(
                 str(buf[3])), align='center')

    ss = []
    ipl = 0
    for f in files:
        if os.path.splitext(f)[1].lower() in ['.jpg', 'jpeg', '.png']:
            ipl = ipl + 1
            new_file_path = r'%s\%s_%s_%s%s' % (
                os.path.join(SRC_DIR, "prepare"), 'img', ipl, str(int(time.time()*10000)), os.path.splitext(f)[1])
            shutil.copy2(os.path.join(root, f), new_file_path)
            ss.append(new_file_path)

    with futures.ThreadPoolExecutor(max_workers=None) as pool:  # 多线程
        for si in ss:
            results = pool.submit(compressImage, si)
            results.add_done_callback(testMMCQ)  # 回调函数
    testshm.close()


def compressImage(srcPath):
    # 如果是文件就处理
    if os.path.isfile(srcPath):
        try:
            # 打开原图片缩小后保存，可以用if srcFile.endswith(".jpg")或者split，splitext等函数等针对特定文件压缩
            filename = os.path.basename(srcPath)
            dstFile = os.path.join(os.path.join(
                SRC_DIR, "compress"), filename)
            sImg = PImage.open(srcPath)
            dImg = sImg.convert('RGB')
            w, h = sImg.size
            MIN_SIZE = 40*40
            # 设置压缩尺寸和选项，注意尺寸要用括号
            if max(w, h) > ignore_size:
                dImg = dImg.resize(
                    (int(w/size_rate), int(h/size_rate)), PImage.NEAREST)
            # 尺寸过小需要放大
            elif max(w, h) < MIN_SIZE:
                dImg = dImg.resize(
                    (int(w*2), int(h/size_rate*2)), PImage.NEAREST)
            dImg.save(dstFile.replace(filename.split('.')[1], 'jpg'))
            dImg.close()
            sImg.close()
            os.rename(srcPath, srcPath.replace(
                filename.split('.')[1], 'jpg'))  # 不改找不到文件
            return dstFile.replace(filename.split('.')[1], 'jpg')

        except Exception as e:
            print(e)


    # 如果是文件夹就递归
    # if os.path.isdir(srcPath):
    #     for file in srcPath:
    #         compressImage(file)
    # 多进程已做好文件夹递归，srcPath传参必是文件


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

    imgfile = os.path.abspath(future.result())
    # rgb = list(map(lambda d: MMCQ(d, themes, file=imgfile, use='cv2').quantize(), [cv.imdecode(np.fromfile(
    #     imgfile, dtype=np.uint8), cv.COLOR_BGR2RGB)]))
    rgb = list(map(lambda d: MMCQ(d, themes, file=imgfile, use='PIL').quantize(), [PImage.open(imgfile).convert('RGB')]))
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
    testshm.close()


def domain(img):
    testshm = shared_memory.SharedMemory(name='main_run_share')
    buf = testshm.buf
    with progress:
        task_id = progress.add_task(
            "process", filename="正在多线程分析 ", start=False)

        totaltime = time.time()

        # 遍历删除图片
        path = os.path.join(SRC_DIR, "finish")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        path = os.path.join(SRC_DIR, "compress")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        if os.path.exists(os.path.join(SRC_DIR, "reports")) == False:
            os.makedirs(os.path.join(SRC_DIR, "reports"))
        path = os.path.join(SRC_DIR, "prepare", "temp")
        temp = os.path.join(SRC_DIR, "prepare", "temp")
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
        path = os.walk(os.path.join(SRC_DIR, "prepare"))
        if os.name == 'posix':
            rerule = re.compile(r'/#.{6}/#.{6}/#.{6}/#.{6}/#.{6}/__')
        else:
            rerule = re.compile(r'\#.{6}\#.{6}\#.{6}\#.{6}\#.{6}\__')
        rerule2 = re.compile(r'SCMD-P.*')  # 和定义的命名规则有关
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
            path = os.walk(img)
            print(img)
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
                path = os.walk(img)
                for root, dirs, files in path:
                    ffs.append(files)
                    roots.append(root)

                prolist.map(procompress, ffs, roots)

            while True:  # 定时检测文件夹文件数量
                nowlist = len(os.listdir(
                    os.path.join(SRC_DIR, "finish")))
                time.sleep(2)
                while nowlist != len(os.listdir(os.path.join(SRC_DIR, "finish"))):
                    continue
                buf[1] = 0
                break

            path = os.walk(os.path.join(SRC_DIR, "compress"))
            for root, dirs, files in path:
                for f in files:
                    shutil.move(os.path.join(root, f), os.path.join(SRC_DIR, "finish", f))

            path = os.walk(os.path.join(SRC_DIR, "prepare"))
            for root, dirs, files in path:
                for f in files:
                    fname = os.path.splitext(os.path.basename(f))[0]
                    fnames = fname.split(DIR_SPLIT)
                    lastname = fnames[len(fnames) - 1]
                    if os.name == 'posix':
                        fname = fname.replace(lastname, re.sub(r'/__.*/__', '', lastname))  # 正则替换
                    else:
                        fname = fname.replace(lastname, re.sub(r'\__.*\__', '', lastname))  # 正则替换

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
                        # issanme = g.buttonbox(msg=f'\n 【疑似重复提醒】 检测到两张图片的色彩主题相同，你有理由怀疑它们是重复的，请检查！\n{sames[0]} \
                        #     为已存在图片（图片大小{sames[2]}）\n{sames[1]} 为当前待保存图片（图片大小{sames[3]}）\n',
                        #                       title=' 操作确认 ', choices=(
                        #                           ' 保留已存在的 ', ' 我全都要 ', ' 删除已存在的 '), default_choice=None, cancel_choice=' 我全都要 ', images=None)
                        # if issanme != ' 我全都要 ':
                        #     if issanme == ' 保留已存在的 ':
                        #         os.remove(dstname)
                        #         with open(os.path.join(root, licenseid) + '.json', 'w') as js:
                        #             json.dump(jsonstr, js)
                        #         os.rename(os.path.join(root, f), dstname)
                        #     else:
                        #         os.remove(os.path.join(root, f))
                        # else:
                        #     # 本demo参考SCMD标准，因此不允许重复存在，如有需求可自行修改
                        #     os.remove(os.path.join(root, f))
                    else:
                        with open(os.path.join(root, licenseid) + '.json', 'w') as js:
                            json.dump(jsonstr, js)
                        os.rename(os.path.join(root, f), dstname)

            progress.stop_task(task_id)

            cost_times = str(round(time.time()-totaltime, 4))
            cc = 1
            # cc = g.ccbox(msg="\n\n\n" + SRC_DIR + "\n\n\n 总耗时：" +
            #              cost_times, title="处理完成", choices=(" 生成报告 ", " 完成 "))

            # 点击生成报告触发事件
            if cc == 1:
                print('\n\n\n')
                curr_time = datetime.datetime.now()
                # 将路径转为URL格式，不转则json.dump以ASCII格式写到JSON文件里
                in_path_url = parse.quote(img, safe=";/?:@&=+$,")
                reportjson = {'date': curr_time.strftime(
                    "%Y-%m-%d"), 'time': curr_time.strftime("%H:%M:%S"), 'in_path_url': in_path_url, 'in_files': ptv, 'cost_times': cost_times}
                reportfile = os.path.join(
                    SRC_DIR, 'reports', curr_time.strftime("%Y%m%d-%H%M%S_")) + 'report.json'
                with open(reportfile, 'w') as js:
                    file_list = []
                    for dir in os.listdir(os.path.join(SRC_DIR, 'prepare')):
                        child = os.path.join(SRC_DIR, 'prepare', dir)
                        if os.path.isdir(child):
                            for file in os.listdir(child):
                                if os.path.splitext(file)[1].lower() in ['.jpg', '.jpeg', '.png']:
                                    file = os.path.join(child, file)
                                    if os.path.basename(child) != 'temp':
                                        file_list.append(file.replace('\\', '/'))
                        elif os.path.isfile(child):
                            if os.path.splitext(child)[1].lower() in ['.jpg', '.jpeg', '.png']:
                                file_list.append(child.replace('\\', '/'))
                    reportjson['origin_list'] = origin_list
                    json.dump(reportjson, js)
                    console.print(reportjson, justify='full', highlight=True)
                    for i in range(len(file_list)):
                        file_list[i] = str(file_list[i]).replace(SRC_DIR, '')
                    print('写入index.js')
                    with open(os.path.join(SRC_DIR, 'index.js'), 'w', encoding='utf-8') as mainjs:
                        mainjs.write(
                            'class ImgShow extends React.Component {\n render() {\n return (<div id="imgbox"><div className="imgshow1" >\n')
                    print('注入index.js')
                    with open(os.path.join(SRC_DIR, 'index.js'), 'a', encoding='utf-8') as mainjs:
                        img1 = len(file_list) // 2
                        img2_w = False
                        i = 0
                        shutil.copy2(os.path.join(
                            SRC_DIR, '_css', 'base.css'), os.path.join(SRC_DIR, 'index.css'))
                        for name in file_list:
                            i += 1
                            if rerule2.search(os.path.splitext(name)[0]):
                                colors = rerule2.search(os.path.splitext(name)[0]).group().split('-')
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
                                    with open(os.path.join(SRC_DIR, 'index.css'), 'a', encoding='utf-8') as maincss:
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
                                        mainjs.writelines('</div>\n<div className='"'imgshow2'"'>\n')
                                        img2_w = True
                                    mainjs.writelines(
                                        r'<div className="colorbox wow fadeIn" data-wow-delay="0.2s" data-wow-duration="0.5s" data-wow-offset="20">')
                                    with open(os.path.join(SRC_DIR, 'index.css'), 'a', encoding='utf-8') as maincss:
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
                        with open(os.path.join(SRC_DIR, '_js', 'base.js'), 'r+', encoding='utf-8') as index:
                            index.seek(0)
                            index_text = index.read()
                            if os.name == 'posix':
                                rf = re.sub(r'^.*/src', './', reportfile)
                            else:
                                rf = re.sub(r'^.*\\src', './', reportfile).replace('\\', '/')
                            index_text = index_text.replace(
                                '[[reportpath]]', rf)
                            mainjs.writelines(index_text)
                testshm.close()
                cc1 = shared_memory.SharedMemory(name='main_run_share')
                buf = cc1.buf
                buf[2] = 1
                cc1.close()
                return 6

