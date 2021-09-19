import os
from functools import reduce

import rwpy.util as util
from rwpy.util import JSONObject as Jsobj
from rwpy.errors import UndefinedElementTypeError as UETError
from enum import Enum


ElementType = Enum('ElementType',('space','note','attribute'))


def connect_strs(strs: list,sep: str='\n') -> str:
    text = ''
    for s in strs:
        text += str(s) + sep
    return text


class Element(object):
    def __init__(self,content: str):
        self.__content = content
        
    
    def __str__(self):
        return self.__content
        
         
    __repr__ = __str__ 
        

class Attribute(Element):
    def __init__(self,key: str,value: str):
        self.__key = key
        self.__value = value
        Element.__init__(self,key + ': ' + value)
    
    
    @property
    def key(self) -> str:
        return self.__key
        
        
    @property
    def value(self) -> str:
        return self.__value
        
        
    __str__ = Element.__str__
    __repr = __str__
        

class ElementContainer(object):
    def __init__(self):
        self.__elements = []
        
    
    def append(element):
        if isinstance(element,Element):
            self.__elements.append(element)


class Section(object):
    def __init__(self,name: str):
        self.__name = name
        self.elements = []
        
        
    def __str__(self):
        text = '[{0}]\n'.format(self.__name) + connect_strs(self.elements)
        return text
    __repr__ = __str__
    
    
    @property
    def name(self):
        return self.__name
    

class Ini(object):
    def __init__(self,filename='untitled.ini'):
        self.elements = []
        self.sections = []
        self.__filename = filename
        
    
    def __str__(self):
        text = ''
        text += connect_strs(self.elements)
        text += connect_strs(self.sections)
        return text
    __repr__ = __str__
    
    
    @property
    def filename(self):
        return self.__filename


def make_element(type: ElementType) -> dict:
    r_element = {}
    if isinstance(type,ElementType):
        r_element['type'] = str(type).split('.')[1]
    else:
        raise UETError('make_element()函数参数的类型名“{0}”不在rwpy.code.ElementType中'.format(type),__file__)
    return r_element
    
    
def make_section(name: str) -> dict:
    return {'name': name,'elements': []}