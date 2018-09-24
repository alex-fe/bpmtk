import re
import unittest

from log.log import SimpleLog
from miners.splitminer.dfgp.dfgp import DFGEdge, DFGNode, DirectlyFollowGraph


class TestDFGEdge(unittest.TestCase):

    def setUp(self):
        source = DFGNode(code='zero')
        target = DFGNode(code='one')
        self.edge = DFGEdge(source, target)

    def test__str__(self):
        """Test DFGEdge's __str__ method."""
        self.assertEqual(str(self.edge), '0')
        self.edge.frequency = 12
        self.assertEqual(str(self.edge), '12')

    # def test_print_(self):
    #     """Assert print_ message is prints source to target with frequency in
    #     correct arrangement."""
    #     # assert first part is source code
    #     self.assertEqual(
    #         re.match('.+?(?= >)', self.edge.print_)[0], self.edge.source.code
    #     )
    #     # assert 2nd part is target code
    #
    #     # message =
    #     # self.assertEqual(self.edge.print_,


class TestDirectlyFollowGraph(unittest.TestCase):

    def setUp(self):
        events = None
        traces = {}
        s_log = SimpleLog(traces, events, None)
        s_log.start_code = None
        s_log.end_code = None
        self.graph = DirectlyFollowGraph(s_log)

    def test_add_node(self):
        """Assert node was successfully added to dfgp's nodes."""
        self.assertFalse(self.graph.nodes)  # empty before adding node

        n = DFGNode(code='zero')
        self.graph.add_node(n)
        self.assertIs(n, self.graph.nodes.get(n.code))

    def test_add_edge(self):
        """Assert edge was successfully added to dfgp's edges with respect to
        incoming/outgoing continuity."""
        self.assertFalse(self.graph.edges)  # empty before adding node
        self.assertFalse(self.graph.incoming)
        self.assertFalse(self.graph.outgoing)

        source = DFGNode(code='zero')
        target = DFGNode(code='one')
        edge = DFGEdge(source, target)
        self.graph.add_edge(edge)
        self.assertIn(edge, self.graph.edges)
        self.assertIn(edge.target.code, self.graph.incoming)
        self.assertIn(edge.source.code, self.graph.outgoing)
        self.assertIs(
            self.graph.dfgp[edge.source.code][edge.target.code], edge
        )

    def test_remove_node(self):
        pass
