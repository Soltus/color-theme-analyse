import os,sys
if os.name == 'posix':
    CLS = 'clear'
    DIR_SPLIT = '/'
else:
    CLS = 'cls'
    DIR_SPLIT = '\\'
class Pgd:
    def __init__(self):
        self.url = 'https://pypi.douban.com/simple/'

    def task(self,im,re):
        self.im = im
        self.re = re
        import os
        repo = input('\n\n Unable to import package [{}] from \n\t{} , \n\n Do you want to download ? \n\n\t\tProccess ? [Y/n]\t'.format(self.im, sys.path))
        if repo in ['Y','y']:
            os.system(CLS)
            os.system("pip install {} -i {}".format(self.re, self.url))
            return 1
        return 0