import unittest
import os
import shutil

from rwpy.code import Ini,Section,Attribute,Element
from rwpy.mod import IMod,Mod,mkmod,rmmod

class Test(unittest.TestCase):

    def test_create_ini(self):

        ex: str = "#abc\n[core]\n #hf:jskfj\nabc:456\ndef:\"\"\"\naz\n\"\"\""
        ini: Ini = Ini.create_ini(ex)
        sam: Ini = Ini.IniBuilder().setfilename('sam.ini').append_ele('#abc').append_sec(Section.SectionBuilder()\
        .setname('core')\
        .append_ele('#hf:jskfj')\
        .append_attr('abc','456')\
        .append_attr('def','\"\"\"\naz\n\"\"\"')\
        .build())\
        .build()
        sam.filename = 'sam2.ini'
        self.assertEqual(sam.filename,'sam2.ini')
        self.assertEqual(sam.core['abc'].value,'456')

        for i in range(0,len(sam.elements)):

            self.assertEqual(ini.elements[i],sam.elements[i])

        for i in range(0,len(sam.sections)):

            self.assertEqual(ini.sections[i].name,sam.sections[i].name)
            
            for j in range(0,len(sam.sections[i].elements)):

                self.assertEqual(ini.sections[i].elements[j],ini.sections[i].elements[j])


    def test_mod(self):
        
        if os.path.exists('mymod'):
            shutil.rmtree('mymod')

        mymod: Mod = mkmod('mymod')
        mymod.newini('abc.ini','#这是一个测试！')
        self.assertEqual(isinstance(mymod.getini('abc.ini'),Ini),True,'ini获取失败！')
        self.assertEqual(str(mymod.getini('abc.ini')).strip(),'#这是一个测试！',\
        'ini文件不匹配，内容竟为{}，而要求内容为{}'.format(str(mymod.getini('abc.ini')).strip(),'#这是一个测试！'))
        mymod.rmini('abc.ini')
        self.assertEqual(mymod.getini('abc.ini'),None,'ini文件未删除')
        rmmod('mymod')