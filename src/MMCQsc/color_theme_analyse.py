
import os,sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc','src'))
DPKG_DIR = os.path.abspath(os.path.join(BASE_DIR, 'MMCQsc_dpkg'))
if BASE_DIR not in sys.path:
    sys.path.insert(1,BASE_DIR)
if DPKG_DIR not in sys.path:
    sys.path.insert(1,DPKG_DIR)

def Menu(choice:int=0):
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
    menu = '''
欢迎使用 MMCQsc
---------------
(1) 运行主程序
(2) 运行主程序（内置edge浏览器封装）
(3) 重装依赖包（差异模式）
(4) 重装依赖包（强力模式）
(5) 修复 MMCQsc_dpkg（暂不可用）
(6) 清理依赖包
Any other key to exit.
---------------
请输入对应数字：'''
    if choice == 0:
        repo = input(menu)
    else:
        repo = str(choice)
    if repo == '1':
        MainFunc()
    elif repo == '6':
        from MMCQsc.scp.scripts import pipw
        pipw.uninstallMerge()
    elif repo == '3':
        while True:
            _path = input("\n请绑定 Python 可执行文件的完整绝对路径，留空则默认绑定到当前的 launcher\n>>> ")
            if _path == '':
                break
            elif os.path.isfile(_path) and os.path.basename(_path) == 'python.exe':
                break
            else:
                print('\n无效路径\n')
        from MMCQsc.scp.scripts import pipw
        pipw.reinstallMerge(_path)
    elif repo == '4':
        while True:
            _path = input("\n请绑定 Python.exe 的绝对路径，留空则默认绑定到当前的 launcher\n>>> ")
            if _path == '':
                break
            elif os.path.isfile(_path) and os.path.basename(_path) == 'python.exe':
                break
            else:
                print('\n无效路径\n')
        from MMCQsc.scp.scripts import pipw
        pipw.reinstallMerge(_path,full=True)
    elif repo == '5':
         pass
    elif repo == '2':
        MainFunc(mode=True)
    else:
        raise ValueError('无效参数')
        exit(111)

def MainFunc(mode=False):
    try:
        from MMCQsc.scp import executable_check
    except Exception as e:
        print(e)
    else:
        from MMCQsc.scp import main
        try:
            result = main.mainFunc(mode)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    Menu()
