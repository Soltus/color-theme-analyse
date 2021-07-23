import os,sys,shutil
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
if root_path not in sys.path:
    sys.path.append(root_path)


import argparse

parser = argparse.ArgumentParser(prog='color-theme-analyse',formatter_class=argparse.RawDescriptionHelpFormatter, description='功能介绍', epilog='基于 MMCQ 对图片进行色彩主题分析，采用图片压缩和多进程来加速批量分析速度。\n\n https://gitee.com/hi-windom/color-theme-analyse  \n \n ')
parser.add_argument('--path',default=None, help='选择交给 %(prog)s 处理的文件夹（包含子文件夹）')

args = parser.parse_args()


if __name__ == '__main__':
    SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),'src'))
    try:
        from MMCQsc.scp import executable_check
    except:
        exit()
    else:
        from MMCQsc.scp import main
        try:
            result = main.mainFunc()
        except BaseException as e:
            if isinstance(e, KeyboardInterrupt):
                print("{} 服务已停止\n用户强制退出".format(__file__))
        finally:
            try:
                os.remove(os.path.join(SRC_DIR + '\\index.js'))
                os.remove(os.path.join(SRC_DIR + '\\index.css'))
                shutil.rmtree(os.path.join(SRC_DIR + '\\finish'))
                shutil.rmtree(os.path.join(SRC_DIR + '\\compress'))
                print('成功删除不重要的自动生成文件')
            except:
                print('未能删除自动生成文件')
            finally:
                exit()
