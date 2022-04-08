from typing import Callable, List,Dict,Optional,Union,NoReturn
import re
from abc import ABC, abstractmethod

from rwpy.util import filterl,IBuilder,check
from rwpy.errors import IniSyntaxError, SectionNotExistedError
from rwpy.util import connect_strs


not_copied_keys =[
('core','copyFrom'),
('#','@copyFromSection'),
('core','dont_load'),
('#','@copyFrom_skipThisSection')
]


def to_multiline(text: str) -> str:
    '''将字符串转换为多行文本'''
    return '\"\"\"{0}\"\"\"'.format(text)
    
    
def read_multiline(multiline: str) -> str:
    '''将多行文本转换为一般字符串'''
    return multiline.strip('\"\"\"')


class Element(object):
    '''元素，代码的基本单位'''
    def __init__(self,content: str,linenum: int = -1):

        self.__content: str = content
        self.__linenum: int = linenum
        
    
    def __str__(self) -> str:

        return self.__content
    
    
    @property
    def linenum(self) -> int:
        '''特殊属性，标识元素的行号'''
        return self.__linenum

    
    def __eq__(self,other) -> bool:

        if not isinstance(other,type(self)):

            return False

        if not str(self) == str(other):

            return False

        return True
        

class Attribute(Element):
    '''属性，代码的主要内容'''
    def __init__(self,key: str,value: str,linenum: int = -1):

        self.__key = key
        self.__value = value
        Element.__init__(self,key + ': ' + value,linenum)
    
    
    @property
    def key(self) -> str:
        '''属性的键'''
        return self.__key
        
    
    @key.setter
    def key(self,key: str): 

        check(key,str)
        self.__key = key
        self._Element__content = self.__key + ': ' + self.__value
        
        
    @property
    def value(self) -> str:
        '''属性的值'''
        return self.__value
        
    
    @value.setter
    def value(self,value: str):

        check(value,str)
        self.__value = value
        self._Element__content = self.__key + ': ' + self.__value


    def __eq__(self,other) -> bool:

        if not isinstance(other,type(self)):

            return False
        
        if not self.key == other.key or not self.value == other.value:

            return False

        return True


class ISection(ABC):
    '''ISection接口'''
    @abstractmethod
    def __init__(self,name: str):
        pass


    @abstractmethod
    def append(self,ele: Element):
        pass


    @abstractmethod
    def insert(self,ele: Element,before: Union[int,str]) -> NoReturn:
        pass

    
    @abstractmethod
    def remove_attribute(self,key: str) -> NoReturn:
        pass
        
    
    @abstractmethod
    def __getitem__(self,item: str) -> Optional[Attribute]:
        pass
        
        
    @abstractmethod
    def __str__(self) -> str:
        pass
        
    
    @abstractmethod
    def get_attribute(self,key: str) -> Attribute:
        pass
        
    
    @abstractmethod
    def getattrs(self) -> List[Attribute]:
        pass


class Section(ISection):
    '''段落，代码的组织单位'''
    def __init__(self,name: str,linenum: int = -1):

        self.__name: str = name
        self.__elements: List[Element] = []
        self.__attributes: Dict[str,Attribute] = {}
        self.linenum: int = linenum
        self.__attributes: Dict[str,Attribute] = {}
    
    
    @property
    def elements(self) -> List[Element]:

        return self.__elements
        
    
    @elements.setter
    def elements(self,elements: List[Element]) -> NoReturn:

        check(elements,list)
        if any(map(lambda x: not isinstance(x,Element),elements)):
            raise TypeError()
        self.__elements = elements

        
    @property
    def name(self) -> str:

        return self.__name
        
        
    @name.setter
    def name(self,name: str) -> NoReturn:

        check(name,str)
        self.__name = name

    
    def append(self,ele: Element):
        '''向段落中追加元素'''
        check(ele,Element)
        self.elements.append(ele)

        if isinstance(ele,Attribute):

            self.__attributes[ele.key] = ele
    
    
    def insert(self,ele: Element,before: Union[int,str]) -> NoReturn:
        '''在段落中指定位置插入元素，或向指定属性后插入元素'''
        check(ele,Element)

        if isinstance(before,int):

            self.__elements.insert(before,ele)

        elif isinstance(before,str):

            for i in range(0,len(self.__elements)):

                if isinstance(self.__elements[i],Attribute):

                    if self.__elements[i].key == before:

                        self.__elements.insert(ele)

        else:

            raise TypeError()
                    
                        
    def remove_attribute(self,key: str) -> NoReturn:
        '''删除指定键的属性'''
        check(key,str)
        for i in range(0,len(self.__elements)):

            if isinstance(self.__elements[i],Attribute):

                if self.__elements[i].key == key:

                    self.__elements.pop(i)
                    self.__attributes.pop(key)
        
        
    
    def __getitem__(self,item: str) -> Optional[Attribute]:
        '''获取指定键的属性'''
        check(item,str)

        if item in self.__attributes:

            return self.__attributes[item]

        else:

            return None
        
        
    def __str__(self) -> str:
        '''对应的文本'''
        text = '[{0}]\n'.format(self.__name) + connect_strs(self.elements)
        return text
        
    
    def get_attribute(self,key: str) -> Attribute:
        '''获取指定键的属性。如果不存在，则追加该属性'''
        if not key in self.__attributes:
            self.append(Attribute(key,''))
        return self.__attributes[key]
        
    
    def getattrs(self) -> List[Attribute]:
        '''获取段落中全部属性'''
        return filterl(lambda x: isinstance(x,Attribute),self.elements)
    

    class SectionBuilder(IBuilder):
        '''段落构造器，用于快速生成段落'''
        def __init__(self,template = None):

            super().__init__()

            if template is None:

                self.__elements = []
                self.__name = 'section'

            elif isinstance(template,ISection):

                self.__elements = template.elements[:]
                self.__name = template.name

            else:

                raise TypeError()
        
    
        def setname(self,name: str):
            '''设置生成段落名'''
            check(name,str)
            self.__name = name
            return self
        
        
        def append_attr(self,key: str,value: str,linenum: int = -1):
            '''追加属性'''
            check(key,str)
            check(value,str)
            self.__elements.append(Attribute(key,value,linenum))
            return self
            
        
        def append_ele(self,content: str,linenum: int = -1):
            '''追加元素'''
            check(content,str)
            self.__elements.append(Element(content,linenum))
            return self
            
        
        def build(self) -> ISection:
            '''构建段落'''
            sec = Section(self.__name)
            for ele in self.__elements:
                sec.append(ele)
            return sec


class IIni(ABC):
    @abstractmethod
    def __init__(self,filename: str = 'untitled.ini'):
        pass


    @property
    @abstractmethod
    def filename(self) -> str:
        pass


    @filename.setter
    @abstractmethod
    def filename(self,name: str) -> NoReturn:
        pass


    @property
    @abstractmethod
    def elements(self) -> List[Element]:
        pass


    @elements.setter
    @abstractmethod
    def elements(self,ele: List[Element]) -> None:
        pass


    @property
    @abstractmethod
    def sections(self) -> List[Section]:
        pass


    @sections.setter
    @abstractmethod
    def sections(self,secs: List[Section]) -> NoReturn:
        pass

    
    @abstractmethod
    def __str__(self) -> str:
        pass
        
    
    @abstractmethod
    def __getattr__(self,attr: Optional[str] = None) -> Optional[Section]:
        pass
            
    
    @abstractmethod
    def get_section(self,name: str) -> Section:
        pass
    
    
    @abstractmethod
    def append(self,sec: Section) -> NoReturn:
        pass
        

    @abstractmethod
    def insert_section(self,sec: Section,before: str) -> NoReturn:
        pass

    
    @abstractmethod
    def remove(self,name: str) -> NoReturn:
        pass
                
    
    @abstractmethod
    def write(self):
        pass

    
    @abstractmethod
    def merge(self,ini):
        pass
    

class Ini(IIni):
    '''代码文件'''
    def __init__(self,filename: str = 'untitled.ini'):
        self.__elements: List[Element] = []
        self.__sections: List[Section] = []
        self.__filename: str = filename
        
    
    def __str__(self) -> str:
        '''对应的文本'''
        text: str = ''
        text += connect_strs(self.elements) + '\n'
        text += connect_strs(self.sections)
        return text
    
    
    @property
    def filename(self) -> str:
        '''代码文件的文件路径'''
        return self.__filename


    @filename.setter
    def filename(self,name: str) -> NoReturn:
        check(name,str)
        self.__filename = name


    @property
    def elements(self) -> List[Element]:

        return self.__elements

    
    @elements.setter
    def elements(self,eles: List[Element]) -> NoReturn:

        check(eles,list)
        if any(map(lambda x: not isinstance(x,Element),eles)):
            raise TypeError()
        self.__elements = eles


    @property
    def sections(self) -> List[Section]:

        return self.__sections


    @sections.setter
    def sections(self,secs: List[Section]) -> NoReturn:

        check(secs,list)
        if any(map(lambda x: not isinstance(x,Section),secs)):
            raise TypeError()
        self.__sections = secs
        
    
    def __getattr__(self,attr: Optional[str] = None) -> Optional[Section]:
        '''获取一个指定名称的段落'''
        if self.sections is None:

            return self.sections

        for sec in self.sections:

            if attr == sec.name:

                return sec
            
            
    def get_section(self,name: str) -> Section:
        '''获取一个指定名称的段落'''
        finds = filterl(lambda x: x.name == name,self.sections)

        if len(finds) == 0:

            sec = Section(name)
            self.sections.append(sec)
            return sec

        else:

            return finds[-1]

    getsection = get_section
    
    
    def append(self,obj: Union[Section,Element]) -> NoReturn:
        '''追加段落或头部元素'''
        if isinstance(obj,Section):

            self.__sections.append(obj)

        elif isinstance(obj,Element):

            self.__elements.append(obj)

        else:

            raise TypeError()

    append_sec: Callable[[IIni,Union[Section,Element]],NoReturn] = append
    append_ele: Callable[[IIni,Union[Section,Element]],NoReturn] = append
        
        
    def remove(self,name: str) -> bool:
        '''删除指定名称的段落'''
        check(name,str)

        for i in range(0,len(self.sections)):

            if self.sections[i].name == name:

                self.sections.pop(i)
                return True

        return False
            
    def removeat(self,pos: int) -> bool:
        '''删除指定位置的头部元素'''
        check(pos,int)

        if pos >= len(self.__elements):

            raise IndexError()

        else:

            self.__elements.pop(pos)
            
    def insert_section(self,sec: Section,before: str) -> NoReturn:
        '''在指定的段落之前插入段落'''
        check(sec,Section)

        for i in range(0,len(self.__sections)):

            if self.__sections[i].name == before:

                self.__sections.insert(i,sec)

        raise SectionNotExistedError()
                
    
    def write(self):
        '''
        输出ini内容到文件
        抛出IOError异常
        '''
        with open(self.__filename,'w',encoding='utf-8') as f:
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

            this_sec: Optional[Section] = self.getsection(sec.name)

            if this_sec is None:
                continue

            for attr in sec.getattrs():
                if not attr.key in map(lambda x: x.key,this_sec.getattrs()) and not attr.key in not_copied_keys[1]:
                    this_sec.append(Attribute(attr.key,attr.value))
    

    class IniBuilder(IBuilder):
        '''代码文件构造器，用于快速生成代码文件'''
        def __init__(self,template = None):
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
            
        
        def append_ele(self,content: str,linenum: int = -1):
            '''向生成ini头部追加元素'''
            check(content,str)
            self.__elements.append(Element(content,linenum))
            return self
            
        
        def append_sec(self,section: Section):
            '''向生成ini追加段落'''
            check(section,Section)
            self.__sections.append(section)
            return self
            
        
        def build(self) -> IIni:
            '''构建ini'''
            ini = Ini(self.__filename)
            for ele in self.__elements:
                ini.append(ele)
            for sec in self.__sections:
                ini.append(sec)
            return ini


    def create_ini(text: str,filename: str = 'untitled.ini') -> IIni:
        '''
        从字符串创建ini，第二版
        抛出IniSyntaxError
        '''
        check(text,str)
        check(filename,str)
        
        if text.isspace() or text == '':
            return Ini()
            
        inib: Ini.IniBuilder = Ini.IniBuilder().setfilename(filename)
        ptr: IBuilder = inib
        lines: List[str] = text.split('\n')
        linenum: int = 0
        alinenum: int = 0
        
        while len(lines) > 0:
            line = lines.pop(0)
            linenum += 1

            if line.lstrip().startswith('#'):
                ptr.append_ele(line)
            
            if not re.match(r'\s*\[.+\]',line.strip()) is None:
            
                if isinstance(ptr,Section.SectionBuilder):
                    ptrs: Section = ptr.build()
                    ptrs.linenum = alinenum
                    inib.append_sec(ptrs)
                    
                ptr = Section.SectionBuilder().setname(line.strip()[1:-1])
                alinenum = linenum
                
            elif not re.match(r'\s*[^#].*:.+',line) is None:
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
                
        if isinstance(ptr,Section.SectionBuilder):

            ptrs: Section = ptr.build()
            ptrs.linenum = alinenum
            inib.append_sec(ptrs)
            
        ini: Ini = inib.build()
        return ini
            



        
        

    
    
