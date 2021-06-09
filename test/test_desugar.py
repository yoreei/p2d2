import unittest
from p2d2.preprocessor.desugar import desugar


class TestDesugar(unittest.TestCase):
    def setUp(self):
        pass
    def codeEqual(self, code1, code2):
        # TODO normalize code?
        code1 = code1.replace(", ",",")
        code2 = code2.replace(", ",",")
        return self.assertEqual(code1, code2)

     #def test_getitem(self):
     #    code="""\
     #        df.func()
     #        df['hi']
     #        df[['hi','ho','he']]
     #        df[123]
     #        df[1,2,3]
     #    parsed = astroid.parse(code)
     #    calls = len(list(parsed.nodes_of_class(astroid.Call)))
     #    subscripts = len(list(parsed.nodes_of_class(astroid.Subscript)))
     #    self.assertEqual(calls, 5)
     #    self.assertEqual(subscripts, 0)

    def test_slice_3int(self):
        sugar = "a[1:2:3]"
        non_sugar = desugar(sugar) 
        expected = "a.__getitem__(slice(1,2,3))"
        self.codeEqual(non_sugar, expected)

    def test_slice_3none(self):
        sugar = "a[::]"
        non_sugar = desugar(sugar) 
        expected = "a.__getitem__(slice(None, None, None))"
        self.codeEqual(non_sugar, expected)

    def test_slice_none_int_none(self):
        sugar = "a[:1]"
        non_sugar = desugar(sugar) 
        expected = "a.__getitem__(slice(None, 1, None))"
        self.codeEqual(non_sugar, expected)

    def test_slice_none_none_str(self):
        sugar = "a[::'world']"
        non_sugar = desugar(sugar) 
        expected = "a.__getitem__(slice(None, None, 'world'))"
        self.codeEqual(non_sugar, expected)

    def test_index_int(self):
        sugar = "a[3]"
        non_sugar = desugar(sugar) 
        expected = "a.__getitem__(3)"
        self.codeEqual(non_sugar, expected)

    def test_index_str(self):
        sugar = "a['hello world']"
        non_sugar = desugar(sugar) 
        expected = "a.__getitem__('hello world')"
        self.codeEqual(non_sugar, expected)

    def test_index_3int(self):
        sugar = "a[0,1,2]"
        non_sugar = desugar(sugar) 
        expected = "a.__getitem__((0,1,2))"
        self.codeEqual(non_sugar, expected)

    def test_slice_index(self):
        sugar = "a[0:1:2,3,4]"
        non_sugar = desugar(sugar) 
        expected = "a.__getitem__((slice(0,1,2),3,4))"
        self.codeEqual(non_sugar, expected)
        
#    def test_fail(self):
#        self.assertEqual(1,0)


#    def test_widget_resize(self):
#        self.widget.resize(100,150)
#        self.assertEqual(self.widget.size(), (100,150),
#                         'wrong size after resize')
