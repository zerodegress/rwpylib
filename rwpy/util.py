import os
import json

from rwpy.errors import VisitAbstractMemberError


def filterl(func,lst):
    '''filter，但返回list'''
    return list(filter(func,lst))


def check(obj,type,message: str='参数类型错误'):
    '''快速检查参数类型错误'''
    if not isinstance(obj,type):
        raise TypeError()


class Builder(object):

    def __init__(self,template=None):
        pass
            
    
    def build(self):
        '''构建，抽象函数'''
        raise VisitAbstractMemberError()
        

class CodeList(object):
    
    def __init__(self):
        self.elements = []
        self.sections = []
        self.types = []
    __slots__ = ('author','description','version','game_version')


class JSONObject(dict):

    def __getattr__(self,attr):
        return self[attr]


def load_codelist(filename='codelist.json') -> CodeList:
    '''加载代码表(json格式)，未完成'''
    codelistjson = {}
    with open(filename,'r') as file:
        codelistjson = json.loads(file.read())
    codelist = CodeList()
    codelist.elements = codelistjson['elements']
    codelist.sections = codelistjson['sections']
    codelist.types = codelistjson['types']
    codelist.author = codelistjson['types']
    codelist.description = codelistjson['description']
    codelist.version = codelistjson['version']
    codelist.game_version = codelistjson['game_version']
    return codelist
