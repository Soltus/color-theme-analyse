import argparse
import sys

class gitupC:
    pass
class Cgitup(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('%r %r %r' % (namespace, values, option_string))
        setattr(namespace, self.dest, values)
        print('%r %r %r' % (namespace, values, option_string))


parser = argparse.ArgumentParser(prog='gitup',formatter_class=argparse.RawDescriptionHelpFormatter, description='功能介绍', epilog='基于 MMCQ 对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。\n\n https://gitee.com/hi-windom/color-theme-analyse  \n \n ')
parser.add_argument('--version',default=None, action=Cgitup, help='define version')
parser.add_argument('--commit',default= False, action=argparse.BooleanOptionalAction)
parser.add_argument('--workdir',default=None, action=Cgitup, help='工作区')
parser.add_argument('--mode',choices=['r','w'],required=False)
# gitup = gitupC()
# args = parser.parse_args(args=sys.argv,namespace=Cgitup)
# print(args.version)