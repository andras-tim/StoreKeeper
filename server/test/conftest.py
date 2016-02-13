# Pytest config for this test directory
import pytest
from _pytest.main import Node


def pytest_itemcollected(item: Node):
    if item.get_marker('skip'):
        __skip_item(item)


def pytest_collection_modifyitems(items: list):
    if __has_only_marked_item(items):
        __skip_not_only_marked_items(items)


def __has_only_marked_item(items: list) -> bool:
    for item in items:
        if item.get_marker('only'):
            return True
    return False


def __skip_not_only_marked_items(items: list):
    for item in items:
        if not item.get_marker('only'):
            __skip_item(item, reason='Skipped by only mark(s)')


def __skip_item(item: Node, reason: (str, None)=None):
    item.add_marker(pytest.mark.skipif(True, reason=reason))


# Enable test mode
import app
app.test_mode = True


# Pre-load server module for preserve import order
import app.server
