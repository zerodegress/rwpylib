

class IniSyntaxError(Exception):
    def __init__(self,message: str):
        self.__message = message
        
    
    @property
    def message(self) -> str:
        return self.__message
        
        
    def __str__(self) -> str:
        return 'Ini语法错误:{0}'.format(self.__message)
    __repr = __str__