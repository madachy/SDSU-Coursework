import unittest

from basicsearch_lib02.queues import PriorityQueue
from explored import Explored


class TestExplored(unittest.TestCase):
    # noinspection PyPep8Naming
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.explored = Explored()

    def test_exists(self):
        example_state = 'hello world'
        self.explored.add(example_state)
        self.assertTrue(self.explored.exists(example_state))

    def test_non_exists(self):
        example_state = 'the quick brown fox jumps over the lazy dog'
        self.assertFalse(self.explored.exists(example_state))


class TestPriorityQueue(unittest.TestCase):
    # noinspection PyPep8Naming
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.pq = PriorityQueue()

    def test_pop(self):
        self.pq.append(self.SampleObj(1, 1))
        self.pq.append(self.SampleObj(3, 3))
        self.pq.append(self.SampleObj(2, 2))

        self.assertEqual(self.pq.pop().value, 1)
        self.assertEqual(self.pq.pop().value, 2)
        self.assertEqual(self.pq.pop().value, 3)

    class SampleObj(object):
        def __init__(self, value, priority):
            self.value = value
            self.priority = priority

        def __lt__(self, other):
            return self.priority < other.priority


if __name__ == '__main__':
    unittest.main()
