from app.models import Item
from test.e2e.base_session_test import CommonSessionTest


class CommonSessionTestWithItemManipulation(CommonSessionTest):
    def _set_item_quantity(self, *change_list: list):
        for change in change_list:
            item = Item.query.get(change['item_id'])
            item.quantity = change['quantity']
        self._db_commit()
