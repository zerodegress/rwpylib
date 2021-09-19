import os
import json


class JSONObject(dict):
    def __getattr__(self,attr):
        return self[attr]

def load_codelist(filename='codelist.json') -> dict:
    codelistjson = None
    with open(filename,'r') as file:
        codelistjson = json.loads(file.read())
    return codelistjson
    

default_codelist = load_codelist()