import random
import unittest

import utils as u
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


class TestDirectlyFollowGraph(unittest.TestCase):

    def setUp(self):
        node_codes = range(12)
        self.events = {code: 'test_{}'.format(code) for code in node_codes}
        self.traces = {
            u.make_trace(*random.sample(node_codes, 3)): x for x in range(3)
        }
        s_log = SimpleLog(self.traces, self.events, None)
        s_log.start_code = node_codes[0]
        s_log.end_code = node_codes[-1]
        self.graph = DirectlyFollowGraph(s_log)

    def _create_test_edge(
        self, source=DFGNode(code='0'), target=DFGNode(code='1')
    ):
        """Create two connected node.
        Args:
            source (DFGNode): Source node.
            target (DFGNode): Target node.
        Returns:
            Source and target node, and connecting edge.
        """
        edge = DFGEdge(source, target)
        self.graph.add_node(source)
        self.graph.add_node(target)
        self.graph.add_edge(edge)
        return source, target, edge

    def test_add_node(self):
        """Assert node was successfully added to graph's nodes."""
        self.assertFalse(self.graph.nodes)  # empty before adding node

        n = DFGNode(code='zero')
        self.graph.add_node(n)
        self.assertIs(n, self.graph.nodes.get(n.code))

    def test_add_edge(self):
        """Assert edge was successfully added to graph's edges with respect to
        incoming/outgoing continuity."""
        source, target, edge = self._create_test_edge()

        self.assertIn(edge, self.graph.edges)
        self.assertIn(edge.target.code, self.graph.incoming)
        self.assertIn(edge.source.code, self.graph.outgoing)
        self.assertIs(
            self.graph.dfgp[edge.source.code][edge.target.code], edge
        )

    def test_remove_edge_safe(self):
        """When marked safe and the conditions apply, edge is not removed."""
        source, target, edge = self._create_test_edge()
        self.assertFalse(self.graph.remove_edge(edge, True))

    def test_remove_edge(self):
        """Assert edge is cleanly removed from graph."""
        source, target, edge = self._create_test_edge()
        self.assertTrue(self.graph.remove_edge(edge, False))
        self.assertNotIn(edge, self.graph.incoming[edge.target.code])
        self.assertNotIn(edge, self.graph.outgoing[edge.source.code])
        self.assertNotIn(edge, self.graph.edges)
        self.assertNotIn(edge.target.code, self.graph.dfgp[edge.source.code])

    def test_remove_node(self):
        """Assert node was successfully removed from graph's nodes as well as
        extending edges."""
        source, target, edge = self._create_test_edge()

        self.graph.remove_node(target.code)
        self.assertNotIn(target.code, self.graph.nodes)

    def test_build_edges(self):
        """Assert that graph is built correctly with regards to edge ordering.
        """
        self.graph.build()
        for source, edges in self.graph.dfgp.items():
            for target, edge in edges.items():
                self.assertEqual(source, edge.source.code)
                self.assertEqual(target, edge.target.code)

    def test_build_follow_traces(self):
        """Assert graph follows the path indicated by the traces."""
        self.graph.build()
        for t in self.traces:
            trace_list = u.t_split(t)
            while len(trace_list) > 1:
                start = int(trace_list.pop(0))
                target = int(trace_list[0])
                self.assertIn(start, self.graph.dfgp)
                self.assertIn(target, self.graph.dfgp[start])

    @unittest.skip('Not finished')
    def test_build_frequencies(self):
        self.graph.build()

    def test_detect_simple_loops(self):
        """Assert that all loops of length one (e.g. node to same node) are
        found."""
        node = DFGNode(code='0')
        self._create_test_edge(node, node)
        edge = list(self.graph.edges)[0]
        self.assertEqual(edge.source.code, edge.target.code)  # Assert loop
        self.assertIn(edge.source.code, self.graph.dfgp[edge.source.code])

        self.graph.detect_loops_simple()
        self.assertFalse(self.graph.edges)
        self.assertNotIn(edge.source.code, self.graph.dfgp[edge.source.code])

    @unittest.skip('Not finished')
    def test_loops_extended(self):
        pass

    @unittest.skip('Not finished')
    def test_detect_parallelisms(self):
        pass
