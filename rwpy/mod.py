import os

import rwpy.errors as errors
from rwpy.code import Ini
from rwpy.code import Section
from rwpy.code import Element
from rwpy.code import Attribute
from rwpy.code import create_ini


MOD_INFO_DEFAULT = '''
[mod]
title: 一个rwmod
description: 一个rwmod

tags: units

#thumbnail: mod-thumbnail.png
'''


class Namespace(object):
    def __init__(self,name: str):
        self.__name = name
        self.files = []
        
        
    @property
    def name(self):
        return self.__name
        
        
    def __str__(self):
        return self.__name
    __repr__ = __str__
        
        
class File(object):
    def __init__(self,relpath: str):
        self.__relpath = relpath
        
        
    @property
    def relpath(self):
        return self.__relpath
        
        
    def __str__(self):
        return self.__relpath
    __repr__ = __str__


class Mod(object):
    def __init__(self,dir: str):
        if not os.path.exists(dir):
            raise errors.ModNotExistsError('ModNotExistError:指定Mod不存在->' + dir)
        self.__dir = dir
        self.namespaces = []
        self.rootfiles = []
        self.__modinfo = None
        if os.path.exists(os.path.join(dir,'mod-info.txt')):
            with open(os.path.join(dir,'mod-info.txt')) as f:
                self.__modinfo = create_ini(f.read())
        for root,dirs,files in os.walk(dir,topdown=True):
            if root == self.__dir:
                for dir in dirs:
                    self.namespaces.append(Namespace(dir))
                for file in files:
                    self.rootfiles.append(file)
            else:
                namespace = root.removeprefix(self.__dir + os.sep).split(os.sep,1)[0]
                ptrs = list(filter(lambda x: x.name == namespace,self.namespaces))
                ptr = ptrs[0]
                for file in files:
                    f = File(os.path.relpath(os.path.join(root,file),os.path.join(self.__dir,namespace)))
                    ptr.files.append(f)
            

    @property            
    def dir(self):
        return self.__dir
        
        
    @dir.setter
    def dir(self,newname: str):
        os.rename(self.__dir,newname)
        self.__dir = newname
        
        
    @property
    def modinfo(self):
        return self.__modinfo
        

def mkmod(name: str,namespace: str='default'):
    os.mkdir(name)
    os.mkdir(os.path.join(name,namespace))
    with open (os.path.join(name,'mod-info.txt'),'w') as f:
        f.write(MOD_INFO_DEFAULT)
    return Mod(name)