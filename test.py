import unittest

from rwpy.code import create_ini,Ini,Section,Attribute,Element,IniBuilder,SectionBuilder
from rwpy.mod import IMod,Mod

class Test(unittest.TestCase):

    def test_create_ini(self):

        ex: str = "#abc\n[core]\n #hf:jskfj\nabc:456\ndef:\"\"\"\naz\n\"\"\""
        ini: Ini = create_ini(ex)
        sam: Ini = IniBuilder().append_ele('#abc').append_sec(SectionBuilder().setname('core').append_ele('#hf:jskfj').append_attr('abc','456').append_attr('def','\"\"\"\naz\n\"\"\"').build()).build()

        for i in range(0,len(sam.elements)):

            self.assertEqual(ini.elements[i],sam.elements[i])

        for i in range(0,len(sam.sections)):

            self.assertEqual(ini.sections[i].name,sam.sections[i].name)
            
            for j in range(0,len(sam.sections[i].elements)):

                self.assertEqual(ini.sections[i].elements[j],ini.sections[i].elements[j])


    def test_mod(self):
        pass