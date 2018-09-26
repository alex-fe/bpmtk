import random
import unittest

import utils as u
from log.log import SimpleLog
from miners.splitminer.dfgp.dfgp import DirectlyFollowGraph
from miners.splitminer.dfgp.filters import Filter


@unittest.skip('Not sure how to test')
class TestStandardFilter(unittest.TestCase):

    def setUp(self):
        node_codes = range(12)
        events = {code: 'test_{}'.format(code) for code in node_codes}
        traces = {
            u.make_trace(*random.sample(node_codes, 3)): x for x in range(3)
        }
        s_log = SimpleLog(traces, events, None)
        s_log.start_code = node_codes[0]
        s_log.end_code = node_codes[-1]
        self.graph = DirectlyFollowGraph(s_log)
        self.graph.build()

    def test_best_edges_on_max_freq(self):
        Filter._best_edges_on_max_freq(self.graph)

    def test_standard(self):
        Filter.standard(self.graph)
