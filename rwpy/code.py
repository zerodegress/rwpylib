import os
from functools import reduce
from enum import Enum


import rwpy.util as util
from rwpy.util import JSONObject as Jsobj


ElementType = Enum('ElementType',('space','note','attribute'))


def connect_strs(strs: list,sep: str='\n') -> str:
    return reduce(lambda x,y: x + '\n' + y,map(lambda x: str(x),strs))


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
        text += connect_strs(self.elements) + '\n'
        text += connect_strs(self.sections)
        return text
    __repr__ = __str__
    
    
    @property
    def filename(self):
        return self.__filename


def create_ini(text: str,filename: str='unititled.ini') -> Ini:
    lines = text.split('\n')
    lines = iter(lines)
    ini = Ini(filename)
    ptr = ini
    while True:
        try:
            line = next(lines)
        except StopIteration:
            break
        if ':' in line:
            atb_key = line.split(':')[0]
            atb_value = line.split(':',1)[1]
            if line.strip().endswith("'''"):
                while True:
                    try:
                        atb_value += next(lines)
                    except StopIteration:
                        raise Exception('三引号不正确完结')
                    if atb_value.strip().endswith("'''"):
                        break
            ptr.elements.append(Attribute(atb_key,atb_value))
        elif line.strip().startswith('[') and line.strip().endswith(']'):
            section = Section(line.strip().removeprefix('[').removesuffix(']'))
            ptr = section
            ini.sections.append(section)
        else:
            ptr.elements.append(Element(line))
    return ini