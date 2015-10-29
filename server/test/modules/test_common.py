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


class TestFilterDict(unittest.TestCase):
    DATA = {
        'apple': 1,
        'orange': 2,
        'peach': 3,
    }

    def test_filter_dict(self):
        assert common.filter_dict(self.DATA, {'apple', 'orange'}) == {
            'apple': 1,
            'orange': 2,
        }
        assert common.filter_dict(self.DATA, {'apple', 'peach'}) == {
            'apple': 1,
            'peach': 3,
        }


class TestRecursiveDictUpdate(unittest.TestCase):
    def setUp(self):
        self.single_level = {
            'apple': 1,
            'orange': 2,
            'peach': 3,
        }

        self.multi_level = {
            'fruit': self.single_level,
            'vegetables': {
                'carrot': {
                    'small': 1
                }
            },
        }

    def test_update_single_level_dict_with_single_level_dict(self):
        common.recursive_dict_update(self.single_level, {
            'apple': 4,
            'kiwi': 5,
        })

        assert self.single_level == {
            'apple': 4,
            'orange': 2,
            'peach': 3,
            'kiwi': 5,
        }

    def test_update_single_level_dict_with_multi_level_dict(self):
        common.recursive_dict_update(self.single_level, {
            'apple': {
                'small': 4
            },
            'kiwi': {
                'big': 5
            },
        })

        assert self.single_level == {
            'apple': {
                'small': 4
            },
            'orange': 2,
            'peach': 3,
            'kiwi': {
                'big': 5
            },
        }

    def test_update_multi_level_dict_with_multi_level_dict(self):
        common.recursive_dict_update(self.multi_level, {
            'fruit': {
                'apple': 4,
                'orange': {
                    'small': 5
                },
                'kiwi': 6,
            },
            'vegetables': {
                'carrot': 7
            }
        })

        assert self.multi_level == {
            'fruit': {
                'apple': 4,
                'orange': {
                    'small': 5
                },
                'peach': 3,
                'kiwi': 6,
            },
            'vegetables': {
                'carrot': 7
            },
        }
        assert self.single_level == {
            'apple': 4,
            'orange': {
                'small': 5
            },
            'peach': 3,
            'kiwi': 6,
        }
