import os

import rwpy.errors as errors
from rwpy.code import Ini,Section,Element,Attribute,create_ini
from rwpy.util import filterl



MOD_INFO_DEFAULT = '''
[mod]
title: 一个rwmod
description: 一个rwmod

tags: units

#thumbnail: mod-thumbnail.png
'''


class Mod(object):
    def __init__(self,dir: str):
        if not os.path.exists(dir):
            raise errors.ModNotExistsError('指定Mod不存在->' + dir)
        self.__dir = dir
        self.__files = []
        self.__modinfo = None
        for root,dirs,files in os.walk(dir,topdown=True):
            if 'mod-info.txt' in files:
                if self.__modinfo is None:
                    with open(os.path.join(root,'mod-info.txt'),'r') as f:
                        self.__modinfo = create_ini(f.read())
                else:
                    raise errors.RepeatedModInfoError('多余的mod-info.txt -> ' + os.path.join(root,file))
            for file in files:
                self.__files.append(os.path.relpath(os.path.join(root,file),self.__dir))


    def get_file_path(self,filename: str):
        for file in self.__files:
            if file.endswith(filename):
                return os.path.join(self.__dir,file)
                
                
    def getfiles(self,dir: str=None) -> list:
        if isinstance(dir,str):
            if dir == '.':
                return filterl(lambda x: os.path.dirname(os.path.join(self.__dir,x)) == self.__dir,self.__files)
            return filterl(lambda x: x.startswith(dir),self.__files)
        elif dir is None:
            return self.__files[:]
        else:
            raise TypeError()
            
            
    def getinis(self,dir: str=None) -> list:
        files = filterl(lambda x: x.endswith('.ini'),self.getfiles(dir))
        inis = []
        for p in files:
            with open(os.path.join(self.__dir,p),'r') as f:
                inis.append(create_ini(f.read()))
        return inis
                


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