import app
app.test_mode = True

from app.server import app, lm
from app.modules.example_data import ExampleUsers as Users
from test.views.base_api_test import LowLevelCommonApiTest


class CommonSessionTest(LowLevelCommonApiTest):
    """
    Super class of Session tests

    Have to turn off temporary TESTING mode, because Flask-Login will not authenticate @login_required requests.
    https://flask-login.readthedocs.org/en/latest/#protecting-views
    """
    def setUp(self):
        CommonSessionTest.__set_testing_mode(False)
        super().setUp()
        self.admin_is_authenticated = False

    def tearDown(self):
        super().tearDown()
        CommonSessionTest.__set_testing_mode(True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.__set_testing_mode(True)

    @classmethod
    def __set_testing_mode(cls, enable: bool):
        app.config["TESTING"] = enable
        lm.init_app(app)

    def assertRequest(self, *args, **kwargs):
        if self.admin_is_authenticated:
            super().assertApiRequest("delete", "/sessions")
            self.admin_is_authenticated = False
        super().assertApiRequest(*args, **kwargs)

    def assertRequestAsAdmin(self, *args, **kwargs):
        if not self.admin_is_authenticated:
            super().assertApiRequest("post", "/sessions", data=Users.ADMIN.login(),
                                  expected_data=Users.ADMIN.get(),
                                  expected_status_codes=201)
            self.admin_is_authenticated = True
        super().assertApiRequest(*args, **kwargs)
