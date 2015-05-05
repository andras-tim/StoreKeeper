def list_in_list(list1: list, list2: list) -> list:
    return [item in list2 for item in list1]


def any_in(list1: list, list2: list) -> bool:
    return any(list_in_list(list1, list2))
