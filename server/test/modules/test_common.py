import unittest

from app.modules import common


class TestListInListHelpers(unittest.TestCase):
    REFERENCE = ['apple', 'banana', 'orange']
    REDUCED = ['apple', 'banana']
    EXTENDED = ['apple', 'banana', 'orange', 'kiwi']
    OVERLAPPED = ['banana', 'orange', 'kiwi']
    DISJUNCT = ['kiwi', 'PEACH']

    def test_list_in_list(self):
        assert common.list_in_list(self.REDUCED, self.REFERENCE) == [True, True]
        assert common.list_in_list(self.EXTENDED, self.REFERENCE) == [True, True, True, False]
        assert common.list_in_list(self.OVERLAPPED, self.REFERENCE) == [True, True, False]
        assert common.list_in_list(self.DISJUNCT, self.REFERENCE) == [False, False]

    def test_any_in(self):
        assert common.any_in(self.REDUCED, self.REFERENCE)
        assert common.any_in(self.EXTENDED, self.REFERENCE)
        assert common.any_in(self.OVERLAPPED, self.REFERENCE)
        assert not common.any_in(self.DISJUNCT, self.REFERENCE)
