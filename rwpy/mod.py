from abc import ABC, abstractclassmethod, abstractmethod
from typing import List, NoReturn,Optional
from zipfile import ZipFile
import os
import shutil


from rwpy.code import Ini,Section,Element,Attribute
from rwpy.util import filterl,check
import rwpy.errors as errors


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

class IMod(ABC):

    @property
    @abstractmethod
    def dir(self) -> str:
        pass
        
        
    @property
    @abstractmethod
    def modinfo(self) -> Optional[Ini]:
        pass

    @abstractmethod
    def __init__(self,dir: str):
        pass

    @abstractmethod
    def getfile(self,path: str) -> Optional[str]:
        pass

    @abstractmethod
    def getfiles(self,dir: Optional[str]=None) -> List[str]:
        pass

    @abstractmethod
    def getini(self,inifile: str) -> Optional[Ini]:
        pass

    @abstractmethod
    def getinis(self,dir: Optional[str] = None) -> List[Ini]:
        pass


class Mod(IMod):
    '''Mod'''
    
    def __init__(self,dir: str):
        '''抛出ModNotExistedError和RepeatedModInfoError异常'''
        
        if not os.path.exists(dir):
            raise errors.ModNotExistsError('指定Mod不存在->' + dir)
            
        self.__dir: str = dir
        self.__modinfo: Optional[Ini] = None
        
        for root,dirs,files in os.walk(dir,topdown=True):
        
            if 'mod-info.txt' in files:
            
                if self.__modinfo is None:
                
                    with open(os.path.join(root,'mod-info.txt'),'r',encoding='UTF-8') as f:
                        self.__modinfo = Ini.create_ini(f.read())
                        
                else:
                    raise errors.RepeatedModInfoError('多余的mod-info.txt -> ' + os.path.join(root,'mod-info.txt'))


    @property
    def dir(self) -> str:
        '''Mod根文件夹路径'''
        return self.__dir
        
        
    @property
    def modinfo(self) -> Optional[Ini]:
        '''mod-info.txt的内容'''
        return self.__modinfo
    
    
    def getfile(self,path: str) -> Optional[str]:
        '''获取相对于mod路径下指定文件'''
        check(path,str)
        
        for root,dirs,files in os.walk(self.__dir):
        
            for file in files:
            
                if os.path.relpath(self.__dir,os.path.join(root,file)) == path:
                    return file
                    
    
    def getfiles(self,dir: Optional[str]=None) -> List[str]:
        '''获取相对于mod路径下某一文件夹下全部文件'''
        if not dir is None and not isinstance(dir,str):
            raise TypeError
            
        r_files: List[str] = []
        
        for root,dirs,files in os.walk(self.__dir):
            if os.path.relpath(self.__dir,root) == dir:
                return files
                
            elif dir is None:
                for file in files:
                    r_files.append(os.path.join(root,file))
                    
        return r_files
                
    
    def getini(self,inifile: str) -> Optional[Ini]:
        '''构建mod中的指定ini'''
        check(inifile,str)
        file: str = self.getfile(inifile)
        
        if not file is None:
            text: str = ''
            
            try:
                with open(file,'r') as fs:
                    text = fs.read()
                    
            except UnicodeDecodeError:
                return None
                
            return Ini.create_ini(text,os.path.basename(inifile))
            
    
    def getinis(self,dir: Optional[str] = None) -> List[Ini]:
        '''构建mod下某一文件夹下全部ini'''
        
        files: List[str] = self.getfiles(dir)
        inifiles: List[str] = filterl(lambda x: not x.split('.')[-1] in not_ini_list,files)
        inis: List[Ini] = []
        
        for inifile in inifiles:
            text: str = ''
            
            try:
                with open(inifile,'r') as fs:
                    text = fs.read()
                inis.append(Ini.create_ini(text,inifile))
                
            except UnicodeDecodeError:
                pass
                
        return filterl(lambda x: not x is None,inis)
        
        
    def newini(self,relpath: str,content: str = '') -> Ini:
        ini: Optional[Ini] = None
        path = os.path.join(self.dir, relpath)
        with open(path,'w',encoding='UTF-8') as f:
            ini = Ini.create_ini(f.read, filename = path)
        return ini
        
        
    def rmini(self,relpath: str) -> NoReturn:
        try:
            Ini.create_ini(os.path.join(self.dir, relpath))
        except IniSyntaxError:
            return
        except IOError:
            return
        os.remove(os.path.join(self.dir, relpath))
        

def mkmod(name: str,namespace: str = 'default') -> Mod:
    '''
    创建新mod
    抛出IOError异常
    '''
    check(name,str)
    check(namespace,str)
    os.mkdir(name)
    os.mkdir(os.path.join(name,namespace))
    
    with open (os.path.join(name,'mod-info.txt'),'w',encoding = 'UTF-8') as f:
        f.write(MOD_INFO_DEFAULT)
        
    return Mod(name)

def rmmod(path: str) -> NoReturn:
    '''
    删除一个已经存在的mod
    抛出ModNotExistsError异常
    '''
    if os.path.exists(path):
        if path.split('.')[-1] in ('zip','rwmod','rar'):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            raise errors.ModNotExistsError('指定要删除的mod不存在 ->' + path)