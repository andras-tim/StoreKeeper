class FilterableDict(object):
    def __init__(self, commons: (dict, None)=None, getters: (dict, None)=None, setters: (dict, None)=None):
        self.__commons = commons or {}
        self.__getters = getters or {}
        self.__setters = setters or {}

    def __getitem__(self, item: str):
        result = dict(self.__commons)
        result.update(self.__getters)
        result.update(self.__setters)
        return result[item]

    def get(self, fields_in_result: (list, None)=None, change: (dict, None)=None) -> dict:
        return self.__get_results(self.__getters, fields_in_result, change)

    def set(self, fields_in_result: (list, None)=None, change: (dict, None)=None) -> dict:
        return self.__get_results(self.__setters, fields_in_result, change)

    def __get_results(self, call_specific_data: dict, fields_in_result: (list, None),
                      changed_fields: (dict, None)) -> dict:
        result = dict(self.__commons)
        result.update(call_specific_data)

        if changed_fields:
            result.update(changed_fields)

        if fields_in_result is not None:
            result = dict((k, v) for k, v in result.items() if k in fields_in_result)

        return result


class ExampleUser(FilterableDict):
    def login(self, username: (str, None)=None, password: (str, None)=None):
        return {"username": username or self["username"], "password": password or self["password"]}


class ExampleUsers(object):
    ADMIN = ExampleUser(commons={"username": "admin", "email": "admin@test.com"},
                        setters={"password": "secret"},
                        getters={"admin": True, "id": 1, "disabled": False})

    USER1 = ExampleUser(commons={"username": "foo", "email": "foo@bar.com"},
                        setters={"password": "bar"},
                        getters={"admin": False, "id": 2, "disabled": False})

    USER2 = ExampleUser(commons={"username": "1f-o_o.2", "email": "foo2@bar.com"},
                        setters={"password": "bar2"},
                        getters={"admin": False, "id": 3, "disabled": False})
