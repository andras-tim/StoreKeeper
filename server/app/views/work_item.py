from flask.ext.restful import abort

from app.models import WorkItem, Work
from app.modules.base_views import BaseModelListView, BaseViewWithDiff
from app.modules.common_helper import any_in
from app.modules.example_data import ExampleWorkItems
from app.serializers import WorkItemSerializer
from app.views.common import api_func


class WorkItemListView(BaseModelListView):
    _model = WorkItem
    _serializer = WorkItemSerializer
    _deserializer = WorkItemSerializer

    @api_func('List work items', url_tail='work-items',
              response=[ExampleWorkItems.ITEM1.get(), ExampleWorkItems.ITEM2.get()])
    def get(self):
        return self._get()

    @api_func('Create work item', url_tail='work-items',
              request=ExampleWorkItems.ITEM1.set(),
              response=ExampleWorkItems.ITEM1.get(),
              status_codes={403: 'can not add new work item after outbound items was closed',
                            422: '{{ original }} / can not add one item twice'})
    def post(self):
        work_item = self._post_populate()

        work = Work.query.get(work_item.work.id)
        if work.are_items_frozen():
            abort(403, message='Can not add new item.')

        return self._post_commit(work_item)


class WorkItemView(BaseViewWithDiff):
    _model = WorkItem
    _serializer = WorkItemSerializer
    _deserializer = WorkItemSerializer

    @api_func('Get work item', item_name='work item', url_tail='work-items/1',
              response=ExampleWorkItems.ITEM1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update work item', item_name='work item', url_tail='work-items/1',
              request=ExampleWorkItems.ITEM1.set(),
              response=ExampleWorkItems.ITEM1.get(),
              status_codes={403: 'can not change work item after outbound/returned items was closed',
                            422: '{{ original }} / can not add one item twice'})
    def put(self, id: int):
        work = Work.query.get(self._get_item_by_id(id).work_id)

        self._save_original_before_populate(id)
        work_item = self._put_populate(id)
        changed_fields = self._get_populate_diff(work_item).keys()

        if 'work_id' in changed_fields:
            abort(403, message='Can not change work.')

        if self.__is_tried_to_change_closed(work, changed_fields):
            abort(403, message='Work item was closed.')

        return self._put_commit(work_item)

    @api_func('Delete work item', item_name='work item', url_tail='work-items/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)

    def __is_tried_to_change_closed(self, work, changed_fields):
        if work.are_returned_items_closed():
            return True

        if work.are_outbound_items_closed() and any_in(['item_id', 'outbound_quantity'], changed_fields):
            return True

        return False
