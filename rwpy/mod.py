import os
from typing import List,Tuple,Callable,NewType,Optional,Union,NoReturn

import rwpy.errors as errors
from rwpy.code import Ini,Section,Element,Attribute,create_ini
from rwpy.util import filterl


MOD_INFO_DEFAULT: str = '''
[mod]
title: 一个rwmod
description: 一个rwmod

tags: units

#thumbnail: mod-thumbnail.png
'''

not_ini_list: List[str] = [
'.mp4',
'.ogg',
'.wav',
'.tmx',
'.png'
]

class Unit(object):
    '''由ini及其他文件构造出的单位'''
    pass

class Mod(object):
    '''Mod'''
    def __init__(self,dir: str):
        '''抛出ModNorExistedError'''
        if not os.path.exists(dir):
            raise errors.ModNotExistsError('指定Mod不存在->' + dir)
        self.__dir = dir
        self.__modinfo = None
        for root,dirs,files in os.walk(dir,topdown=True):
            if 'mod-info.txt' in files:
                if self.__modinfo is None:
                    with open(os.path.join(root,'mod-info.txt'),'r') as f:
                        self.__modinfo = create_ini(f.read())
                else:
                    raise errors.RepeatedModInfoError('多余的mod-info.txt -> ' + os.path.join(root,file))


    @property
    def dir(self) -> str:
        '''Mod根文件夹路径'''
        return self.__dir
        
        
    @property
    def modinfo(self) -> str:
        '''mod-info.txt的内容'''
        return self.__modinfo
    
    
    def getfile(self,file: str) -> str:
        '''获取相对于mod路径下指定文件'''
        check(file,str)
        for root,dirs,files in os.walk(self.__dir):
            for file in files:
                if os.path.relpath(self.__dir,os.path.join(root,file)) == path:
                    return file
                    
    
    def getfiles(self,dir: Optional[str]=None) -> List[str]:
        '''获取相对于mod路径下某一文件夹下全部文件'''
        if not dir is None and not isinstance(dir,str):
            raise TypeError
        r_files = []
        for root,dirs,files in os.walk(self.__dir):
            if os.path.relpath(self.__dir,root) ==dir:
                return files
            elif dir is None:
                for file in files:
                    r_files.append(os.path.join(root,file))
        return r_files
                
    
    def getini(self,inifile: str) -> Ini:
        '''构建mod中的指定ini'''
        check(inifile,str)
        file = self.getfile(inifile)
        if not file is None:
            text = ''
            try:
                with open(file,'r') as fs:
                    text = fs.read()
            except UnicodeDecodeError:
                return None
            return create_ini(text,os.path.basename(inifile))
            
    
    def getinis(self,dir: Optional[str]=None) -> List[Ini]:
        '''构建mod下某一文件夹下全部ini'''
        files = self.getfiles(dir)
        inifiles = filterl(lambda x: not x.split('.')[-1] in not_ini_list,files)
        inis = []
        for inifile in inifiles:
            text = ''
            try:
                with open(inifile,'r') as fs:
                    text = fs.read()
                inis.append(create_ini(text,inifile))
            except UnicodeDecodeError:
                pass
        return filterl(lambda x: not x is None,inis)


def mkmod(name: str,namespace: str='default') -> Mod:
    '''
    创建新mod
    抛出IOError异常
    '''
    check(name,str)
    check(namespace,str)
    os.mkdir(name)
    os.mkdir(os.path.join(name,namespace))
    with open (os.path.join(name,'mod-info.txt'),'w') as f:
        f.write(MOD_INFO_DEFAULT)
    return Mod(name)