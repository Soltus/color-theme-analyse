import os

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

def uninstall_merg():
    uninstall_base()
    uninstall_dev()
