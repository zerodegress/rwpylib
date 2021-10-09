import os
from functools import reduce
from enum import Enum

from rwpy.util import filterl


from rwpy.errors import IniSyntaxError
import rwpy.util as util
from rwpy.util import JSONObject as Jsobj


ElementType = Enum('ElementType',('space','note','attribute'))


def connect_strs(strs: list,sep: str='\n') -> str:
    return reduce(lambda x,y: x + '\n' + y,map(lambda x: str(x),strs))


class Element(object):

    def __init__(self,content: str,linenum: int=-1):
        self.__content = content
        self.__linenum = linenum
        
    
    def __str__(self):
        return self.__content
    __repr__ = __str__
    
    
    @property
    def linenum(self):
        return self.__linenum
        

class Attribute(Element):

    def __init__(self,key: str,value: str,linenum: int=-1):
        self.__key = key
        self.__value = value
        Element.__init__(self,key + ': ' + value,linenum)
    
    
    @property
    def key(self) -> str:
        return self.__key
        
        
    @property
    def value(self) -> str:
        return self.__value
        
        
    __str__ = Element.__str__
    __repr = __str__
        

class ElementContainer(list):

    def __init__(self):
        list.__init__(self)
        
    
    def append(element: Element):
        if isinstance(element,Element):
            list.append(element)
        else:
            raise TypeError()


    def insert(index: int,element: Element):
        if isinstance(element,Element):
            list.insert(index,element)
        else:
            raise TypeError()

    
class Section(object):

    def __init__(self,name: str,linenum: int=-1):
        self.__name = name
        self.elements = []
        self.linenum = linenum
        
        
    def append(self,attr: Attribute):
        check(attr,Attribute)
        self.elements.append(attr)
        
        
    def __getitem__(self,item):
        check(item,str)
        attributes = filterl(lambda x: isinstance(x,Attribute),self.elements)
        finds = filter(lambda x: x.key == item,attributes)
        if len(finds) == 0:
            return
        else:
            return finds[-1]
        
        
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
        
        
    def __getitem__(self,item):
        check(item,str)
        attributes = filterl(lambda x: isinstance(x,Attribute),self.elements)
        finds = filter(lambda x: x.key == item,attributes)
        if len(finds) == 0:
            return
        else:
            return finds[-1]
        
    
    def __getattr__(self,attr):
        for sec in self.sections:
            if attr == sec.name:
                return sec


def create_ini(text: str,filename: str='unititled.ini') -> Ini:
    lines = text.split('\n')
    lines = iter(lines)
    ini = Ini(filename)
    ptr = ini
    linenum = 0
    while True:
        try:
            line = next(lines)
        except StopIteration:
            break
        linenum += 1
        if ':' in line:
            atb_key = line.split(':')[0].strip()
            atb_value = line.split(':',1)[1].strip()
            if atb_value.startswith('\"\"\"'):
                while True:
                    try:
                        atb_value += next(lines)
                    except StopIteration:
                        raise IniSyntaxError('行号:{0}|意外终止的多行文本'.format(linenum))
                    linenum += 1
                    if atb_value.strip().endswith('\"\"\"'):
                        break
            ptr.elements.append(Attribute(atb_key,atb_value,linenum))
        elif line.strip().startswith('[') and line.strip().endswith(']'):
            section = Section(line.strip().removeprefix('[').removesuffix(']'),linenum)
            ptr = section
            ini.sections.append(section)
        else:
            ptr.elements.append(Element(line,linenum))
    return ini