import os

MOD_INFO_DEFAULT = '''
[mod]
title: Mega Builders
description: Example mod which replaces builders with Mega Builders

tags: starting-units, units

thumbnail: mod-thumbnail.png
'''

def mkmod(name:str,namespace:str='default'):
    os.mkdir(name)
    os.mkdir(os.path.join(name,namespace))
    with open (os.path.join(name,'mod-info.txt'),'w') as f:
        f.write(MOD_INFO_DEFAULT)
    