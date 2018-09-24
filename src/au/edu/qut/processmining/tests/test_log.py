import unittest

from log.log import LogEdge


class TestLogEdge(unittest.TestCase):

    def test_unique_id(self):
        one = LogEdge()
        two = LogEdge()
        self.assertNotEqual(one.id, two.id)


class TestLogNode(unittest.TestCase):
    pass
