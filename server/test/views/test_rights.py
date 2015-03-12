from ddt import ddt, data

from app.modules.example_data import ExampleUsers as Users, ExampleVendors as Vendors, ExampleUnits as Units
from test.views import CommonRightsTest


@ddt
class TestSessionsRights(CommonRightsTest):
    ENDPOINT = "/sessions"
    INIT_PUSH = {"/users": [Users.USER2]}
    DATA_MAP = {"admin": Users.ADMIN, "user1": Users.USER1, "user2": Users.USER2}
    RIGHTS = CommonRightsTest.iterate_rights({
        "anonymous": {
            "get": False,
            "post": [("admin", True), ("user1", True)],
            "delete": False,
        },
        "admin": {
            "get": True,
            "post": [("admin", True), ("user1", True)],
            "delete": True,
        },
        "user1": {
            "get": True,
            "post": [("admin", True), ("user1", True), ("user2", True)],
            "delete": True,
        },
    })

    @data(*RIGHTS)
    def test_rights(self, r: dict):
        self._test_right(**r)


@ddt
class TestUsersRights(CommonRightsTest):
    ENDPOINT = "/users"
    INIT_PUSH = {"/users": [Users.USER2]}
    DATA_MAP = {"admin": Users.ADMIN, "user1": Users.USER1, "user2": Users.USER2, "user3": Users.USER3}
    RIGHTS = CommonRightsTest.iterate_rights({
        "anonymous": {
            "get": [False, ("admin", False), ("user1", False)],
            "post": [("user3", False)],
            "put": [("admin", False), ("user1", False)],
            "delete": [("admin", False), ("user1", False)],
        },
        "admin": {
            "get": [True, ("admin", True), ("user1", True)],
            "post": {"user3": True},
            "put": {"admin":  True,  "user1": True},
            "delete": {"admin": False, "user1": True}
        },
        "user1": {
            "get": [False, ("admin", True), ("user1", True)],
            "post": {"user3":   True},
            "put": {"admin":    False, "user1": True,  "user2": False},
            "delete": {"admin": False, "user1": False, "user2": False},
        },
    })

    @data(*RIGHTS)
    def test_rights(self, r: dict):
        self._test_right(**r)


@ddt
class TestVendorRights(CommonRightsTest):
    ENDPOINT = "/vendors"
    INIT_PUSH = {"/vendors": [Vendors.VENDOR1]}
    DATA_MAP = {"vendor1": Vendors.VENDOR1, "vendor2": Vendors.VENDOR2}
    RIGHTS = CommonRightsTest.iterate_rights({
        "anonymous": {
            "get": [False, ("vendor1", False)],
            "post": [("vendor2", False)],
            "put": [("vendor1", False)],
            "delete": [("vendor1", False)],
        },
        "admin": {
            "get": [True, ("vendor1", True)],
            "post": [("vendor2", True)],
            "put": [("vendor1", True)],
            "delete": [("vendor1", True)],
        },
        "user1": {
            "get": [True, ("vendor1", True)],
            "post": [("vendor2", True)],
            "put": [("vendor1", True)],
            "delete": [("vendor1", True)],
        },
    })

    @data(*RIGHTS)
    def test_rights(self, r: dict):
        self._test_right(**r)


@ddt
class TestUnitRights(CommonRightsTest):
    ENDPOINT = "/units"
    INIT_PUSH = {"/units": [Units.UNIT1]}
    DATA_MAP = {"unit1": Units.UNIT1, "unit2": Units.UNIT2}
    RIGHTS = CommonRightsTest.iterate_rights({
        "anonymous": {
            "get": [False, ("unit1", False)],
            "post": [("unit2", False)],
            "put": [("unit1", False)],
            "delete": [("unit1", False)],
        },
        "admin": {
            "get": [True, ("unit1", True)],
            "post": [("unit2", True)],
            "put": [("unit1", True)],
            "delete": [("unit1", True)],
        },
        "user1": {
            "get": [True, ("unit1", True)],
            "post": [("unit2", True)],
            "put": [("unit1", True)],
            "delete": [("unit1", True)],
        },
    })

    @data(*RIGHTS)
    def test_rights(self, r: dict):
        self._test_right(**r)
