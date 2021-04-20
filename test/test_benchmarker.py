import unittest
import p2d2.__main__ as benchmarker
from .mock import monitor as mock_monitor


class MockMonitorTestCase(unittest.TestCase):
    def setUp(self):
        benchmarker.monitor = mock_monitor

    def test_runs(self):
        benchmarker.main()
        self.assertEqual(True, True)


#    def test_widget_resize(self):
#        self.widget.resize(100,150)
#        self.assertEqual(self.widget.size(), (100,150),
#                         'wrong size after resize')
