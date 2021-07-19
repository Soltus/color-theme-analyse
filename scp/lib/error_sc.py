from enum import Enum,unique
class __Python__Env__Error(Exception):
    def __init__(self,id):
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
        e81630 = ('',' Can NOT run in Python 2.x ')
        e57453 = ('',' Can NOT run in Python < 3.6 ')
        e97304 = ('','')
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