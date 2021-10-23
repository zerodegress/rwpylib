import os
from functools import reduce
from enum import Enum
import re

from rwpy.util import filterl,Builder,check
from rwpy.errors import IniSyntaxError


not_copied_keys =[
('core','copyFrom'),
('#','@copyFromSection'),
('core','dont_load'),
('#','@copyFrom_skipThisSection')
]


def connect_strs(strs: list,sep: str='\n') -> str:
    '''链接一个list中的所有对象作为一个字符串'''
    if len(strs) == 0:
        return ''
    return reduce(lambda x,y: x + '\n' + y,map(lambda x: str(x),strs))


class Element(object):
    '''元素，代码的基本单位'''
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
    '''属性，代码的主要内容'''
    def __init__(self,key: str,value: str,linenum: int=-1):
        self.__key = key
        self.__value = value
        Element.__init__(self,key + ': ' + value,linenum)
    
    
    @property
    def key(self) -> str:
        '''属性的键'''
        return self.__key
        
        
    @property
    def value(self) -> str:
        '''属性的值'''
        return self.__value


class Section(object):
    '''段落，代码的组织单位'''
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
        finds = filterl(lambda x: x.key == item,attributes)
        if len(finds) == 0:
            return None
        else:
            return finds[-1]
        
        
    def __str__(self):
        '''对应的文本'''
        text = '[{0}]\n'.format(self.__name) + connect_strs(self.elements)
        return text
    __repr__ = __str__
    
    
    @property
    def name(self) -> str:
        return self.__name
        
    
    def getattrs(self) -> list:
        '''获取段落中全部属性'''
        return filterl(lambda x: isinstance(x,Attribute),self.elements)
    

class Ini(object):
    '''代码文件'''
    def __init__(self,filename='untitled.ini'):
        self.elements = []
        self.sections = []
        self.__filename = filename
        
    
    def __str__(self):
        '''对应的文本'''
        text = ''
        text += connect_strs(self.elements) + '\n'
        text += connect_strs(self.sections)
        return text
    __repr__ = __str__
    
    
    @property
    def filename(self):
        '''代码文件的文件路径'''
        return self.__filename
        
    
    def __getitem__(self,item):
        '''获取一个指定键的属性'''
        check(item,str)
        attributes = filterl(lambda x: isinstance(x,Attribute),self.elements)
        finds = filter(lambda x: x.key == item,attributes)
        if len(finds) == 0:
            return None
        else:
            return finds[-1]
        
    
    def __getattr__(self,attr):
        '''获取一个指定名称的段落'''
        for sec in self.sections.reverse():
            if attr == sec.name:
                return sec
            return None
            
            
    def getsection(self,name: str):
        '''获取一个指定名称的段落'''
        finds = filterl(lambda x: x.name == name,self.sections)
        if len(finds) == 0:
            return None
        else:
            return finds[-1]
                
    
    def write(self):
        '''输出ini内容到文件'''
        with open(self.__filename,'w') as f:
            f.write(str(self))


    def merge(self,ini):
        '''合并指定ini到本ini'''
        if not type(ini) == type(self):
            raise TypeError()
        for sec in ini.sections:
            skip = sec['@copyFrom_skipThisSection']
            if not skip is None:
                if skip.value == 'true':
                    continue
            if not sec.name in map(lambda x: x.name,self.sections):
                self.sections.append(Section(sec.name))
            this_sec = self.getsection(sec.name)
            for attr in sec.getattrs():
                if not attr.key in map(lambda x: x.key,this_sec.getattrs()) and not attr.key in not_copied_keys[1]:
                    this_sec.append(Attribute(attr.key,attr.value))
            


class SectionBuilder(Builder):
    '''段落构造器，用于快速生成段落'''
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
    
    
    def append_attr(self,key: str,value: str,linenum: int=-1):
        '''追加属性'''
        check(key,str)
        check(value,str)
        self.__elements.append(Attribute(key,value,linenum))
        return self
        
    
    def append_ele(self,content: str,linenum: int=-1):
        '''追加元素'''
        check(content,str)
        self.__elements.append(Element(content,linenum))
        return self
        
    
    def build(self) -> Section:
        '''构建段落'''
        sec = Section(self.__name)
        sec.elements = self.__elements[:]
        return sec
        
        
class IniBuilder(Builder):
    '''代码文件构造器，用于快速生成代码文件'''
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
    
    
    def append_attr(self,key: str,value: str,linenum: int=-1):
        '''向生成ini头部追加属性'''
        check(key,str)
        check(value,str)
        self.__elements.append(Attribute(key,value,linenum))
        return self
        
    
    def append_ele(self,content: str,linenum: int=-1):
        '''向生成ini头部追加元素'''
        check(content,str)
        self.__elements.append(Element(content,linenum))
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
    


def create_ini(text: str,filename: str='untitled.ini') -> Ini:
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
    
    
def create_ini2(text: str,filename: str='untitled.ini') -> Ini:
    check(text,str)
    check(filename,str)
    if text.isspace() or text == '':
        return Ini()
    inib = IniBuilder().setfilename(filename)
    ptr = inib
    lines = text.split('\n')
    linenum = 0
    while len(lines) > 0:
        line = lines.pop(0)
        linenum += 1
        if not re.match(r'^[.*]$',line.strip()) is None:
            if isinstance(ptr,SectionBuilder):
                inib.append_sec(ptr.build())
            ptr = SectionBuilder().setname(line.strip()[1:-1])
        elif not re.match(r'^.*:.*$',line) is None:
            key,value = line.split(':',1)[0], line.split(':',1)[1]
            clinenum = linenum
            if value.lstrip().startswith('\"\"\"'):
                while True:
                    if len(lines) == 0:
                        raise IniSyntaxError('行号:{0}|意外终止的多行文本'.format(linenum))
                    value += '\n' + lines.pop(0)
                    linenum += 1
                    if value.rstrip().endswith('\"\"\"'):
                        break
            ptr.append_attr(key.strip(),value.strip(),clinenum)
        else:
            ptr.append_ele(line,linenum)
    if isinstance(ptr,SectionBuilder):
        inib.append_sec(ptr.build())
    return inib.build()