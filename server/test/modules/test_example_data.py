import unittest

from app.modules.example_data import FilterableDict, ExampleUser


class TestCreateFilterableDict(unittest.TestCase):
    def test_empty_dict(self):
        f = FilterableDict()
        self.assertDictEqual(f.get(), {})
        self.assertDictEqual(f.set(), {})

    def test_commons_only(self):
        f = FilterableDict(commons={'apple': 1})
        self.assertDictEqual(f.get(), {'apple': 1})
        self.assertDictEqual(f.set(), {'apple': 1})

    def test_getters_only(self):
        f = FilterableDict(getters={'banana': 2})
        self.assertDictEqual(f.get(), {'banana': 2})
        self.assertDictEqual(f.set(), {})

    def test_setters_only(self):
        f = FilterableDict(setters={'orange': 3})
        self.assertDictEqual(f.get(), {})
        self.assertDictEqual(f.set(), {'orange': 3})

    def test_all_type_only(self):
        f = FilterableDict(commons={'apple': 1},
                           getters={'banana': 2},
                           setters={'orange': 3})
        self.assertDictEqual(f.get(), {'apple': 1, 'banana': 2})
        self.assertDictEqual(f.set(), {'apple': 1, 'orange': 3})


class TestPreFilledFilterableDict(unittest.TestCase):
    def setUp(self):
        self.f = FilterableDict(commons={'apple': 1, 'cacao': 11},
                                getters={'banana': 2, 'peach': 22},
                                setters={'orange': 3, 'plum': 33})

    def test_get_elements_by_name(self):
        self.assertEqual(self.f['apple'], 1)
        self.assertEqual(self.f['cacao'], 11)
        self.assertEqual(self.f['banana'], 2)
        self.assertEqual(self.f['peach'], 22)
        self.assertEqual(self.f['orange'], 3)
        self.assertEqual(self.f['plum'], 33)

    def test_filter_commons(self):
        self.assertDictEqual(self.f.get(['apple']), {'apple': 1})
        self.assertDictEqual(self.f.set(['apple']), {'apple': 1})

    def test_filter_getters(self):
        self.assertDictEqual(self.f.get(['peach']), {'peach': 22})
        self.assertDictEqual(self.f.set(['peach']), {})

    def test_filter_setters(self):
        self.assertDictEqual(self.f.get(['plum']), {})
        self.assertDictEqual(self.f.set(['plum']), {'plum': 33})

    def test_filter_multiple_elements(self):
        self.assertDictEqual(self.f.get(['cacao', 'banana', 'orange']), {'cacao': 11, 'banana': 2})
        self.assertDictEqual(self.f.set(['cacao', 'banana', 'orange']), {'cacao': 11, 'orange': 3})

    def test_change(self):
        self.assertDictEqual(self.f.get(change={'cacao': 110, 'banana': 20}),
                             {'apple': 1, 'cacao': 110, 'banana': 20, 'peach': 22})
        self.assertDictEqual(self.f.set(change={'cacao': 110, 'orange': 30}),
                             {'apple': 1, 'cacao': 110, 'orange': 30, 'plum': 33})

    def test_change_in_another_type(self):
        self.assertDictEqual(self.f.get(change={'orange': 330}),
                             {'apple': 1, 'cacao': 11, 'banana': 2, 'peach': 22, 'orange': 330})
        self.assertDictEqual(self.f.set(change={'banana': 20}),
                             {'apple': 1, 'cacao': 11, 'orange': 3, 'plum': 33, 'banana': 20})

    def test_change_a_filtered_field(self):
        self.assertDictEqual(self.f.get(['cacao', 'banana', 'orange'], change={'cacao': 110}),
                             {'cacao': 110, 'banana': 2})
        self.assertDictEqual(self.f.set(['cacao', 'banana', 'orange'], change={'cacao': 110}),
                             {'cacao': 110, 'orange': 3})

    def test_change_a_out_filtered_field(self):
        self.assertDictEqual(self.f.get(['cacao', 'banana', 'orange'], change={'peach': 220}),
                             {'cacao': 11, 'banana': 2})
        self.assertDictEqual(self.f.set(['cacao', 'banana', 'orange'], change={'plum': 330}),
                             {'cacao': 11, 'orange': 3})


class TestExampleUser(unittest.TestCase):
    def setUp(self):
        self.u = ExampleUser(commons={'username': 'apple', 'email': 'orange'},
                             setters={'password': 'banana'})

    def test_login(self):
        self.assertDictEqual(self.u.login(),
                             {'username': 'apple', 'password': 'banana', 'remember': False})

    def test_login_with_overridden_username(self):
        self.assertDictEqual(self.u.login(username='new_apple'),
                             {'username': 'new_apple', 'password': 'banana', 'remember': False})

    def test_login_with_overridden_password(self):
        self.assertDictEqual(self.u.login(password='new_banana'),
                             {'username': 'apple', 'password': 'new_banana', 'remember': False})

    def test_login_with_overridden_username_and_password(self):
        self.assertDictEqual(self.u.login(username='new_apple', password='new_banana'),
                             {'username': 'new_apple', 'password': 'new_banana', 'remember': False})

    def test_login_with_overridden_remember(self):
        self.assertDictEqual(self.u.login(remember=True),
                             {'username': 'apple', 'password': 'banana', 'remember': True})
