from enum import Enum,unique
class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class EnvError(Error):
    def __init__(self,id='e00000'):
        self.show(id)

    def show(self,id):
        self.id = id
        self.name = self.get_name(id)
        self.description = self.get_description(id)

    def get_name(self,id):
        return self.__PEE[id].value[0]

    def get_description(self,id):
        return self.__PEE[id].value[1]

    def help(self,id):
        return [id,self.get_name(id),self.get_description(id)]

    def get_all(self,type='dict'):
        result = {}
        for i in self.__PEE:
            result[i.name] = i.value
        if type != 'json':
            return result
        else:
            import json
            jsonStr = json.dumps(result,ensure_ascii=False, sort_keys=True, indent=4, separators=(' ,', ' : \n    '))
            return jsonStr


    # @unique
    class __PEE(Enum):
        e00000 = ('未知的错误','这是开发者定义的异常，但未提供有关异常的任何帮助信息')
        e81630 = ('',' Can NOT run in Python 2.x ')
        e57453 = ('',' Can NOT run in Python < 3.6 ')
        e97304 = ('','\n\n\t''This script is only for use with ''Python 3.6 or later\n\n\t https://gitee.com/hi-windom/color-theme-analyse/ \n\n')
        e92577 = ('','')
        e16651 = ('','')
        e00324 = ('','')
        e92532 = ('','')
        e13599 = ('','')
        e30056 = ('','')
        e13877 = ('','')
        e01874 = ('','')
        e83112 = ('','')
        e51957 = ('','')
        e34931 = ('','')
        e12154 = ('','')
        e32709 = ('','')
        e34688 = ('','')
        e79646 = ('','')
        e80476 = ('','')
        e26224 = ('','')
        e60388 = ('','')
        e75028 = ('','')
        e10496 = ('','')
        e61843 = ('','')