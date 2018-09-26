import unittest

from log.log import LogEdge, LogNode


class TestLogEdge(unittest.TestCase):

    def test__eq__(self):
        one = LogEdge(None, None)
        two = LogEdge(None, None)
        self.assertNotEqual(one, two)
        self.assertEqual(one, one)


class TestLogNode(unittest.TestCase):

    def setUp(self):
        self.node = LogNode()

    def test__eq__(self):
        node2 = LogNode()
        self.assertEqual(self.node, self.node)
        self.assertNotEqual(self.node, node2)

    def test_increase_frequency(self):
        """Assert method increase_frequency adds the default of one if no args
        are passed, else add passed amount."""
        self.assertEqual(self.node.frequency, 0)
        self.node.increase_frequency()
        self.assertEqual(self.node.frequency, 1)
        self.node.increase_frequency(10)
        self.assertEqual(self.node.frequency, 11)

    def test_inc_start_frequency(self):
        """Assert inc_start_frequency increments start_frequency by 1."""
        self.assertEqual(self.node.start_frequency, 0)
        self.node.inc_start_frequency()
        self.assertEqual(self.node.start_frequency, 1)

    def test_inc_end_frequency(self):
        """Assert inc_end_frequency increments end_frequency by 1."""
        self.assertEqual(self.node.end_frequency, 0)
        self.node.inc_end_frequency()
        self.assertEqual(self.node.end_frequency, 1)

    def test_is_start_event(self):
        """Assert start_frequency is original i.e. start_frequency != 0"""
        self.assertTrue(self.node.is_start_event)
        self.node.inc_start_frequency()
        self.assertFalse(self.node.is_start_event)

    def test_is_end_event(self):
        """Assert end_frequency is original i.e. end_frequency != 0"""
        self.assertTrue(self.node.is_end_event)
        self.node.inc_end_frequency()
        self.assertFalse(self.node.is_end_event)
