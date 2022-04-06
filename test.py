import unittest

from rwpy.code import create_ini,Ini,Section,Attribute,Element

class Test(unittest.TestCase):

    def test_create_ini(self):

        ex: str = "#abc\n[core]\n #hf:jskfj\nabc:456"
        ini: Ini = create_ini(ex)

        for head in ini.elements:
            print("头部元素：" + str(head))

        for sec in ini.sections:

            print("段落：" + sec.name)

            for ele in sec.elements:

                if isinstance(ele,Attribute):

                    print("属性：" + ele.key)
                    print("值：" + ele.value)

                else:

                    print("元素：" + str(ele))