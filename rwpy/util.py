import os
import json


class CodeList(object):
    
    def __init__(self):
        self.elements = []
        self.sections = []
        self.types = []
    __slots__ = ('author','description','version','game_version')
    

class JSONObject(dict):

    def __getattr__(self,attr):
        return self[attr]


def load_codelist(filename='codelist.json') -> CodeList:
    codelistjson = {}
    with open(filename,'r') as file:
        codelistjson = json.loads(file.read())
    codelist = CodeList()
    codelist.elements = codelistjson['elements']
    codelist.sections = codelistjson['sections']
    codelist.types = codelistjson['types']
    codelist.author = codelistjson['types']
    codelist.description = codelistjson['description']
    codelist.version = codelistjson['version']
    codelist.game_version = codelistjson['game_version']
    return codelist
