import os
from functools import reduce
from enum import Enum

from rwpy.util import filterl,Builder,check
from rwpy.errors import IniSyntaxError


def connect_strs(strs: list,sep: str='\n') -> str:
    '''链接一个list中的所有对象作为一个字符串'''
    if len(strs) == 0:
        return ''
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


class Section(object):

    def __init__(self,name: str,linenum: int=-1):
        self.__name = name
        self.elements = []
        self.linenum = linenum
        
    
    def append(self,ele: Element):
        '''向段落中追加元素'''
        check(ele,Element)
        self.elements.append(ele)
        
    
    def __getitem__(self,item):
        '''获取指定键的属性'''
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
        '''获取一个指定键的属性'''
        check(item,str)
        attributes = filterl(lambda x: isinstance(x,Attribute),self.elements)
        finds = filter(lambda x: x.key == item,attributes)
        if len(finds) == 0:
            return
        else:
            return finds[-1]
        
    
    def __getattr__(self,attr):
        '''获取一个指定名称的段落'''
        for sec in self.sections.reverse():
            if attr == sec.name:
                return sec
                
    
    def write(self):
        '''输出ini内容到文件'''
        with open(self.__filename,'w') as f:
            f.write(str(self))


class SectionBuilder(Builder):

    def __init__(self,template=None):
        Builder.__init__(self,template)
        if template is None:
            self.__elements = []
            self.__name = 'section'
        elif isinstance(template,Section):
            self.__elements = template.elements[:]
            self.__name = template.name
        else:
            raise TypeError()
    
   
    def setname(self,name: str):
        '''设置生成段落名'''
        check(name,str)
        self.__name = name
        return self
    
    
    def append_attr(self,key: str,value: str):
        '''追加属性'''
        check(key,str)
        check(value,str)
        self.__elements.append(Attribute(key,value))
        return self
        
    
    def append_ele(self,content: str):
        '''追加元素'''
        check(content,str)
        self.__elements.append(Element(content))
        return self
        
    
    def build(self) -> Section:
        '''构建段落'''
        sec = Section(self.__name)
        sec.elements = self.__elements[:]
        return sec
        
        
class IniBuilder(Builder):

    def __init__(self,template=None):
        if template is None:
            self.__elements = []
            self.__sections = []
            self.__filename = 'untitled.ini'
        elif isinstance(template,Ini):
            self.__elements = template.elements[:]
            self.__sections = template.sections[:]
            self.__filename = template.filename
        else:
            raise TypeError()
    
    
    def setfilename(self,filename: str):
        '''设置生成ini文件名'''
        check(filename,str)
        self.__filename = filename
        return self
    
    
    def append_attr(self,key: str,value: str):
        '''向生成ini头部追加属性'''
        check(key,str)
        check(value,str)
        self.__elements.append(Attribute(key,value))
        return self
        
    
    def append_ele(self,content: str):
        '''向生成ini头部追加元素'''
        check(content,str)
        self.__elements.append(Element(content))
        return self
        
    
    def append_sec(self,section: Section):
        '''向生成ini追加段落'''
        check(section,Section)
        self.__sections.append(section)
        return self
        
    
    def build(self) -> Section:
        '''构建ini'''
        ini = Ini(self.__filename)
        ini.elements = self.__elements[:]
        ini.sections = self.__sections[:]
        return ini
    


def create_ini(text: str,filename: str='unititled.ini') -> Ini:
    '''由字符串创建ini'''
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