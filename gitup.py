import argparse
import sys
from subprocess import Popen,PIPE,check_call
import shlex
class Cgitup(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        # print('\n%r = %r' % (option_string,values))
        # print(namespace)

def git_v_tag(v,c,cwd):
    """
    请确保命令行能够正确使用 Git 命令。
    应当注意，将构建时动态写入的文件从 Git 中移除
    """
    args = shlex.split(f"git add .")
    repo = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0, universal_newlines=True, stdout=PIPE, cwd=cwd)
    repo.wait()
    # 工作区 -> 暂存区
    if c:
        args = shlex.split(f"git commit -a -m 'setup.py auto commit'")
        repo = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0, universal_newlines=True, stdout=PIPE, cwd=cwd)
        repo.wait()
    # 打标签应当在提交之后，生成干净的无本地标识符的包
    if v == '0.0.0':
        args = shlex.split(f"git tag {v}")
        repo = Popen(args, bufsize=0, executable=None, close_fds=False, shell=True, env=None, startupinfo=None, creationflags=0, universal_newlines=True, stdout=PIPE, cwd=cwd)
        repo.wait()


parser = argparse.ArgumentParser(prog='gitup',formatter_class=argparse.RawDescriptionHelpFormatter, description='功能介绍', epilog='基于 MMCQ 对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。\n\n https://gitee.com/hi-windom/color-theme-analyse  \n \n ')
parser.add_argument('--version',default=None, action=Cgitup, help='define version')
parser.add_argument('--commit',default=True, action=argparse.BooleanOptionalAction)
parser.add_argument('--workdir',default=None, action=Cgitup, help='工作区')
# parser.add_argument('--mode',choices=['r','w'],required=False)

args = parser.parse_args()
git_v_tag(v=args.version,c=args.commit,cwd=args.workdir)


