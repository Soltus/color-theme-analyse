import argparse
import sys

class gitupC:
    pass

parser = argparse.ArgumentParser(prog='gitup',formatter_class=argparse.RawDescriptionHelpFormatter, description='功能介绍', epilog='基于 MMCQ 对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。\n\n https://gitee.com/hi-windom/color-theme-analyse  \n \n ')
parser.add_argument('--version',default=None,action='store', help='define version')
gitup = gitupC()
args = parser.parse_args(args=sys.argv,namespace=gitup)
print(gitup.version)