from app.modules.example_data import ExampleUsers as Users, ExampleVendors as Vendors, ExampleUnits as Units, \
    ExampleCustomers as Customers, ExampleAcquisitions as Acquisitions, ExampleStocktakings as Stocktakings, \
    ExampleItems as Items
from test.views import CommonRightsTest, rights_data_provider


@rights_data_provider("/sessions")
class TestSessionsRights(CommonRightsTest):
    INIT_PUSH = {"/users": [Users.USER2]}
    DATA_MAP = {"admin": Users.ADMIN, "user1": Users.USER1, "user2": Users.USER2}
    RIGHTS = {
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
    }


@rights_data_provider("/users")
class TestUsersRights(CommonRightsTest):
    INIT_PUSH = {"/users": [Users.USER2]}
    DATA_MAP = {"admin": Users.ADMIN, "user1": Users.USER1, "user2": Users.USER2, "user3": Users.USER3}
    RIGHTS = {
        "anonymous": {
            "get": [False, ("admin", False), ("user1", False)],
            "post": [("user3", False)],
            "put": [("admin", False), ("user1", False)],
            "delete": [("admin", False), ("user1", False)],
        },
        "admin": {
            "get": [True, ("admin", True), ("user1", True)],
            "post": {"user3": True},
            "put": {"admin": True, "user1": True},
            "delete": {"admin": False, "user1": True}
        },
        "user1": {
            "get": [False, ("admin", True), ("user1", True)],
            "post": {"user3": True},
            "put": {"admin": False, "user1": True, "user2": False},
            "delete": {"admin": False, "user1": False, "user2": False},
        },
    }


@rights_data_provider("/vendors")
class TestVendorRights(CommonRightsTest):
    INIT_PUSH = {"/vendors": [Vendors.VENDOR1]}
    DATA_MAP = {"vendor1": Vendors.VENDOR1, "vendor2": Vendors.VENDOR2}
    RIGHTS = {
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
    }


@rights_data_provider("/units")
class TestUnitRights(CommonRightsTest):
    INIT_PUSH = {"/units": [Units.UNIT1]}
    DATA_MAP = {"unit1": Units.UNIT1, "unit2": Units.UNIT2}
    RIGHTS = {
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
    }


@rights_data_provider("/customers")
class TestCustomerRights(CommonRightsTest):
    INIT_PUSH = {"/customers": [Customers.CUSTOMER1]}
    DATA_MAP = {"customer1": Customers.CUSTOMER1, "customer2": Customers.CUSTOMER2}
    RIGHTS = {
        "anonymous": {
            "get": [False, ("customer1", False)],
            "post": [("customer2", False)],
            "put": [("customer1", False)],
            "delete": [("customer1", False)],
        },
        "admin": {
            "get": [True, ("customer1", True)],
            "post": [("customer2", True)],
            "put": [("customer1", True)],
            "delete": [("customer1", True)],
        },
        "user1": {
            "get": [True, ("customer1", True)],
            "post": [("customer2", True)],
            "put": [("customer1", True)],
            "delete": [("customer1", True)],
        },
    }


@rights_data_provider("/acquisitions")
class TestAcquisitionRights(CommonRightsTest):
    INIT_PUSH = {"/acquisitions": [Acquisitions.ACQUISITION1]}
    DATA_MAP = {"acquisition1": Acquisitions.ACQUISITION1, "acquisition2": Acquisitions.ACQUISITION2}
    RIGHTS = {
        "anonymous": {
            "get": [False, ("acquisition1", False)],
            "post": [("acquisition2", False)],
            "put": [("acquisition1", False)],
            "delete": [("acquisition1", False)],
        },
        "admin": {
            "get": [True, ("acquisition1", True)],
            "post": [("acquisition2", True)],
            "put": [("acquisition1", True)],
            "delete": [("acquisition1", True)],
        },
        "user1": {
            "get": [True, ("acquisition1", True)],
            "post": [("acquisition2", True)],
            "put": [("acquisition1", True)],
            "delete": [("acquisition1", True)],
        },
    }


@rights_data_provider("/stocktakings")
class TestStocktakingRights(CommonRightsTest):
    INIT_PUSH = {"/stocktakings": [Stocktakings.STOCKTAKING1]}
    DATA_MAP = {"stocktaking1": Stocktakings.STOCKTAKING1, "stocktaking2": Stocktakings.STOCKTAKING2}
    RIGHTS = {
        "anonymous": {
            "get": [False, ("stocktaking1", False)],
            "post": [("stocktaking2", False)],
            "put": [("stocktaking1", False)],
            "delete": [("stocktaking1", False)],
        },
        "admin": {
            "get": [True, ("stocktaking1", True)],
            "post": [("stocktaking2", True)],
            "put": [("stocktaking1", True)],
            "delete": [("stocktaking1", True)],
        },
        "user1": {
            "get": [True, ("stocktaking1", True)],
            "post": [("stocktaking2", True)],
            "put": [("stocktaking1", True)],
            "delete": [("stocktaking1", True)],
        },
    }


@rights_data_provider("/items")
class TestItemRights(CommonRightsTest):
    INIT_PUSH = {
        "/items": [Items.ITEM1],
        "/vendors": [Vendors.VENDOR1, Vendors.VENDOR2],
        "/units": [Units.UNIT1, Units.UNIT2],
    }
    DATA_MAP = {"item1": Items.ITEM1, "item2": Items.ITEM2}
    RIGHTS = {
        "anonymous": {
            "get": [False, ("item1", False)],
            "post": [("item2", False)],
            "put": [("item1", False)],
            "delete": [("item1", False)],
        },
        "admin": {
            "get": [True, ("item1", True)],
            "post": [("item2", True)],
            "put": [("item1", True)],
            "delete": [("item1", True)],
        },
        "user1": {
            "get": [True, ("item1", True)],
            "post": [("item2", True)],
            "put": [("item1", True)],
            "delete": [("item1", True)],
        },
    }
