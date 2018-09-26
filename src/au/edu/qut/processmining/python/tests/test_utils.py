import unittest

import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.node_codes = [str(x) for x in range(3)] + ['four']

    def test_make_trace(self):
        trace = utils.make_trace(*self.node_codes)
        self.assertEqual(trace, '::0::1::2::four::')

    def test_t_split(self):
        trace = utils.make_trace(*self.node_codes)
        self.assertEqual(self.node_codes, utils.t_split(trace))
