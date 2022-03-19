import os,sys


def reinstallBase():
    '''
    仅用于调试
    '''
    os.system("pip install color-theme-analyse[base] -i https://mirrors.tencent.com/pypi/simple --force-reinstall")

def reinstallDev():
    '''
    仅用于调试
    '''
    os.system("pip install color-theme-analyse[dev] -i https://mirrors.tencent.com/pypi/simple --force-reinstall")

def reinstallMerge():
    '''
    仅用于调试
    '''
    os.system("pip install color-theme-analyse[merge] -i https://mirrors.tencent.com/pypi/simple --force-reinstall")

def uninstall_base():
    os.system("pip uninstall numpy -y")
    os.system("pip uninstall pillow -y")
    os.system("pip uninstall rich -y")

def uninstall_dev():
    os.system("pip uninstall wheel -y")
    os.system("pip uninstall twine -y")
    os.system("pip uninstall pyinstaller -y")
    os.system("pip uninstall setuptools -y")
    os.system("pip uninstall setuptools_scm -y")
    os.system("pip uninstall setuptools_scm_git_archive -y")

def uninstallMerge():
    '''
    仅用于调试
    '''
    uninstall_base()
    uninstall_dev()