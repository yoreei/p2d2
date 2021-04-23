import unittest
import p2d2.desugar as desugar
import astroid


class TestDesugar(unittest.TestCase):
    def setUp(self):
        desugar.all()

    def test_getitem(self):
        code="""\
            df.func()
            df['hi']
            df[['hi','ho','he']]
            df[123]
            df[1,2,3]
"""
        parsed = astroid.parse(code)
        calls = len(list(parsed.nodes_of_class(astroid.Call)))
        subscripts = len(list(parsed.nodes_of_class(astroid.Subscript)))
        self.assertEqual(calls, 5)
        self.assertEqual(subscripts, 0)

#    def test_fail(self):
#        self.assertEqual(1,0)


#    def test_widget_resize(self):
#        self.widget.resize(100,150)
#        self.assertEqual(self.widget.size(), (100,150),
#                         'wrong size after resize')
