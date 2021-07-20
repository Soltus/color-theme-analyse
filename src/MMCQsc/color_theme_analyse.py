import os,sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

if root_path not in sys.path:
    sys.path.append(root_path)

def hello_soltus():
    import argparse

    parser = argparse.ArgumentParser(prog='color-theme-analyse',formatter_class=argparse.RawDescriptionHelpFormatter, description='功能介绍', epilog='基于 MMCQ 对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。\n\n https://gitee.com/hi-windom/color-theme-analyse  \n \n ')
    parser.add_argument('--path',default=None, help='选择交给 %(prog)s 处理的文件夹（包含子文件夹）')

    args = parser.parse_args()

if __name__ == '__main__':
    from scp import executable_check
    from scp import main
    result = main.mainFunc()
