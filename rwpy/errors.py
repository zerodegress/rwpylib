

class RWPYError(Exception):
    '''RWPY库的基础错误'''
    def __init__(self,message: str):
        check(message,str)
        self.__message = message
        
    
    @property
    def message(self) -> str:
        return self.__message
        
        
    def __str__(self) -> str:
        return '{0}:{1}'.format(self.__class__.__name__,self.__message)
    __repr = __str__


class IniSyntaxError(RWPYError):
    '''ini语法错误'''
    def __init__(self,message: str):
        self.__message = message
        RWPYError.__init__(self,message)
    

class ModNotExistsError(RWPYError):
    '''Mod不存在错误'''
    def __init__(self,message: str):
        self.__message = message
        RWPYError.__init__(self,message)
    

class RepeatedModInfoError(RWPYError):
    '''重复的mod-info.txt错误'''
    def __init__(self,message: str):
        self.__message = message
        RWPYError.__init__(self,message)
        

class VisitAbstractMemberError(RWPYError):
    '''访问抽象成员错误'''
    def __init__(self,message: str):
        self.__message = message
        RWPYError.__init__(self,message)