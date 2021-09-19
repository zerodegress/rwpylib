

class UndefinedElementTypeError(Exception):
    def __init__(self,message: str,filename: str):
        self.message = message
        self.filename = filename
        
    def __str__(self):
        return '发生了“未定义元素类型异常”，\n文件名:{0},\n{1}'.format(self.filename,self.message)
    __repr__ = __str__
    
    
