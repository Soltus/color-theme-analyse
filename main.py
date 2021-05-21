from multiprocessing import shared_memory
from concurrent import futures
import easygui as g
import test_3
import os
import time


def createServer():
    print('\n\n\n本地服务器创建成功：\nlocalhost:5858\n\n')
    os.system(
        'cd {}/src && python -m http.server 5858'.format(os.path.dirname(__file__)))


def openhtml():
    print('\n即将默认浏览器打开：\nlocalhost:5858\n\n')
    os.system('start http://localhost:5858')
    time.sleep(10)
    try:
        base_dir = os.path.dirname(__file__)
        os.remove(base_dir + '\\src\\index.js')
        os.remove(base_dir + '\\src\\index.css')
    except:
        pass
    # 网页渲染完毕就不需要HTTP服务，因此删去生成的CSS和JS并杀死进程，有网页交互需求就删去这部分代码
    os.system('taskkill /f /fi "IMAGENAME eq cmd.exe')


if __name__ == '__main__':
    try:
        shm = shared_memory.SharedMemory(
            name='main_run_share', create=True, size=4096)
    except:
        shm = shared_memory.SharedMemory(name='main_run_share')
        shm.buf[1] = 0
    buf = shm.buf
    # fileopenbox()函数的返回值是你选择的那个文件的具体路径
    if buf[1] > 0:
        pass
    else:
        img = g.fileopenbox('open file' + '会导入当前文件夹的全部图片')
        if img != None:  # 有传入才处理
            buf[1] = len(img)
            for i in range(2, 10, 1):
                buf[i] = 0
            test_3.domain(img)
            if buf[2] == 1:
                with futures.ProcessPoolExecutor(max_workers=None) as prolist:
                    prolist.submit(createServer)
                    prolist.submit(openhtml)  # 多进程才能打开


# shm.close()  # 关闭共享内存
# shm.unlink()  # 释放共享内存
