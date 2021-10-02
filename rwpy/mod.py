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
            raise errors.ModNotExistsError('指定Mod不存在->' + dir)
        self.__dir = dir
        self.files = []
        self.__modinfo = None
        for root,dirs,files in os.walk(dir,topdown=True):
            if 'mod-info.txt' in files:
                if self.__modinfo is None:
                    with open(os.path.join(root,'mod-info.txt'),'r') as f:
                        self.__modinfo = create_ini(f.read())
                else:
                    raise errors.RepeatedModInfoError('多余的mod-info.txt -> ' + os.path.join(root,file))
            for file in files:
                self.files.append(File(os.path.relpath(os.path.join(root,file),self.__dir)))
            

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