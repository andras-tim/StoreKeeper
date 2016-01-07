from app.server import app, lm
from app.modules.example_data import ExampleUsers as Users, ExampleUser
from test.e2e.base_api_test import CommonApiTest


class CommonSessionTest(CommonApiTest):
    """
    Super class of Session tests

    Have to turn off temporary TESTING mode, because Flask-Login will not authenticate @login_required requests.
    https://flask-login.readthedocs.org/en/latest/#protecting-views
    """
    def setUp(self):
        CommonSessionTest.__set_testing_mode(False)
        super().setUp()
        self.authenticated_user = None

    def tearDown(self):
        super().tearDown()
        CommonSessionTest.__set_testing_mode(True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.__set_testing_mode(True)

    def _fill_up(self, list_of_endpoint_and_objects: list):
        __tracebackhide__ = True
        if not self.INIT_PUSH:
            return

        self.assertApiLogin(Users.ADMIN)
        super()._fill_up(list_of_endpoint_and_objects)
        self.assertApiLogout()

    def assertApiLogin(self, credential: (dict, ExampleUser), expected_data: (str, list, dict, None)=None,
                       expected_status_codes: (int, list)=201):
        if isinstance(credential, ExampleUser):
            credential = credential.login()
        self.assertApiPost(data=credential, endpoint='/session',
                           expected_data=expected_data, expected_status_codes=expected_status_codes)
        self.authenticated_user = credential

    def assertApiLogout(self, expected_data: (str, list, dict, None)=None, expected_status_codes: (int, list)=200):
        self.assertApiDelete(expected_data=expected_data, endpoint='/session',
                             expected_status_codes=expected_status_codes)
        self.authenticated_user = None

    def assertApiSession(self, expected_data: (str, list, dict, None)=None, expected_status_codes: (int, list)=200):
        self.assertApiGet(expected_data=expected_data, endpoint='/session',
                          expected_status_codes=expected_status_codes)

    @classmethod
    def __set_testing_mode(cls, enable: bool):
        app.config['TESTING'] = enable
        lm.init_app(app)
