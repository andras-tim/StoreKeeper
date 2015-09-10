def list_in_list(list1: list, list2: list) -> list:
    return [item in list2 for item in list1]


def any_in(list1: list, list2: list) -> bool:
    return any(list_in_list(list1, list2))


def filter_dict(dictionary: dict, fields: (list, set)) -> dict:
    return dict((k, v) for k, v in dictionary.items() if k in fields)
