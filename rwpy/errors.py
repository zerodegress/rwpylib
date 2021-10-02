class RWPYError(Exception):
    def __init__(self,message: str):
        self.__message = message
        
    
    @property
    def message(self) -> str:
        return self.__message
        
        
    def __str__(self) -> str:
        return '{0}:{1}'.format(self.__class__.__name__,self.__message)
    __repr = __str__

class IniSyntaxError(RWPYError):
    def __init__(self,message: str):
        self.__message = message
        RWPYError.__init__(self,message)
    
    
class ModNotExistsError(RWPYError):
    def __init__(self,message: str):
        self.__message = message
        RWPYError.__init__(self,message)
    
    
class RepeatedModInfoError(RWPYError):
    def __init__(self,message: str):
        self.__message = message
        RWPYError.__init__(self,message)