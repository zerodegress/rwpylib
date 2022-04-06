import json
from functools import reduce
from typing import List,Tuple,Callable,Any,Type
from abc import ABC, abstractmethod


def connect_strs(strs: List[str],sep: str = '\n') -> str:
    '''链接一个list中的所有对象作为一个字符串'''
    if len(strs) == 0:
        return ''
    return reduce(lambda x,y: x + '\n' + y,map(lambda x: str(x),strs))

def filterl(func: Callable[[Any],bool],lst: list) -> list:
    '''filter，但返回list'''
    return list(filter(func,lst))


def check(obj: object,type: Type,message: str = '参数类型错误'):
    '''快速检查参数类型错误'''
    if not isinstance(obj,type):
        raise TypeError(message)




def CodeList(object):
    '''代码表'''
    def __init__(self,codelist_src: dict):
        check(codelist_src,dict)
        self.__src = codelist_src
        self.__namecheck = map(lambda x: (x['key'],x['section']),codelist_src['attributes'])
    
    
    @property
    def src(self) -> dict:
        '''源'''
        return self.__src
    
    
    @property
    def namecheck(self) -> List[Tuple[str,str]]:
        '''
        包含若干校验元素的校验名表，每个校验元素为2长度的元组，
        0位置为代码名，1位置为段落名
        '''
        return self.__namecheck[:]
    
    
    def getcodes(self,sec_name: str = None):
        '''返回段落下所有代码。不填参数默认为返回所有代码'''
        if sec_name is None:
            return self.__src['attributes'][:]
        check(sec_name,str)
        return filterl(lambda x: x['section'] == sec_name,self.__src['attributes'])
    



class IBuilder(ABC):
    '''接口'''
    @abstractmethod
    def build(self):
        '''构建，抽象函数'''
        pass


def load_codelist(filename: str = 'codelist.json') -> dict:
    '''加载代码表(json格式),开发中'''
    codelist:dict = {}
    #try:
    with open(filename,'r') as f:
        codelist = json.loads(f.read())
    #except IOError:
    return codelist