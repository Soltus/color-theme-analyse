
'''prog - 程序的名称（默认：sys.argv[0]）

usage - 描述程序用途的字符串（默认值：从添加到解析器的参数生成）

description - 在参数帮助文档之前显示的文本（默认值：无）

epilog - 在参数帮助文档之后显示的文本（默认值：无）

parents - 一个 ArgumentParser 对象的列表，它们的参数也应包含在内

formatter_class - 用于自定义帮助文档输出格式的类

prefix_chars - 可选参数的前缀字符集合（默认值：'-'）

fromfile_prefix_chars - 当需要从文件中读取其他参数时，用于标识文件名的前缀字符集合（默认值：None）

argument_default - 参数的全局默认值（默认值： None）

conflict_handler - 解决冲突选项的策略（通常是不必要的）

add_help - 为解析器添加一个 -h/--help 选项（默认值： True）

allow_abbrev - 如果缩写是无歧义的，则允许缩写长选项 （默认值：True）

在 3.5 版更改: 添加 allow_abbrev 参数。

在 3.8 版更改: 在之前的版本中，allow_abbrev 还会禁用短旗标分组，例如 -vv 表示为 -v -v。

在 3.9 版更改: 添加了 exit_on_error 形参。

'''
import argparse

parser = argparse.ArgumentParser(prog='color-theme-analyse',formatter_class=argparse.RawDescriptionHelpFormatter, description='功能介绍', epilog='基于 MMCQ 对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。\n\n https://gitee.com/hi-windom/color-theme-analyse  \n \n ')
parser.add_argument('--path',default=None, help='选择交给 %(prog)s 处理的文件夹（包含子文件夹）')

args = parser.parse_args()

import os,sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc','src'))
DPKG_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc_dpkg'))
if BASE_DIR not in sys.path:
    sys.path.insert(1,BASE_DIR)
if DPKG_DIR not in sys.path:
    sys.path.append(DPKG_DIR)



if __name__ == '__main__':
    try:
        from MMCQsc.scp.executable_check import *
    except Exception as e:
        print(e)
    else:
        from MMCQsc.scp import main
        try:
            result = main.mainFunc()
        except Exception as e:
            print(e)