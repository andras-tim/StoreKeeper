from flask import g
from flask.ext.restful import abort

from app.models import Work, WorkItem
from app.modules.base_views import BaseListView, BaseView, BaseNestedListView, BaseNestedModelViewWithDiff
from app.modules.common_helper import any_in
from app.modules.example_data import ExampleWorks, ExampleWorkItems
from app.serializers import WorkSerializer, WorkDeserializer, WorkItemSerializer, WorkItemDeserializer
from app.views.common import api_func


class WorkListView(BaseListView):
    _model = Work
    _serializer = WorkSerializer
    _deserializer = WorkDeserializer

    @api_func('List works', url_tail='/works',
              response=[ExampleWorks.WORK1.get(), ExampleWorks.WORK2.get()])
    def get(self):
        return self._get()

    @api_func('Create work', url_tail='/works',
              request=ExampleWorks.WORK1.set(),
              response=ExampleWorks.WORK1.get())
    def post(self):
        return self._post()


class WorkView(BaseView):
    _model = Work
    _serializer = WorkSerializer
    _deserializer = WorkDeserializer

    @api_func('Get work', item_name='work', url_tail='/works/1',
              response=ExampleWorks.WORK1.get())
    def get(self, id: int):
        return self._get(id)

    @api_func('Update work', item_name='work', url_tail='/works/1',
              request=ExampleWorks.WORK1.set(change={'comment': 'Something are not finished'}),
              response=ExampleWorks.WORK1.get(change={'comment': 'Something are not finished'}))
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete work', item_name='work', url_tail='/works/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)


class WorkItemListView(BaseNestedListView):
    _model = WorkItem
    _parent_model = Work
    _serializer = WorkItemSerializer
    _deserializer = WorkItemDeserializer

    @api_func('List work items', url_tail='/works/1/items',
              response=[ExampleWorkItems.ITEM1.get(), ExampleWorkItems.ITEM2.get()],
              queries={'id': 'ID of work'})
    def get(self, id: int):
        self._initialize_parent_item(id)
        return self._get(work_id=id)

    @api_func('Create work item', url_tail='/works/1/items',
              request=ExampleWorkItems.ITEM1.set(),
              response=ExampleWorkItems.ITEM1.get(),
              status_codes={403: 'can not add new work item after outbound items was closed',
                            422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of work'})
    def post(self, id: int):
        work = self._initialize_parent_item(id)
        item = self._post_populate(work_id=id)

        if work.are_items_frozen():
            abort(403, message='Can not add new item.')

        return self._post_commit(item)


class WorkItemView(BaseNestedModelViewWithDiff):
    _model = WorkItem
    _parent_model = Work
    _serializer = WorkItemSerializer
    _deserializer = WorkItemDeserializer

    @api_func('Get work item', item_name='work item', url_tail='/works/1/items/1',
              response=ExampleWorkItems.ITEM1.get(),
              queries={'id': 'ID of work',
                       'item_id': 'ID of selected work item for get'})
    def get(self, id: int, item_id: int):
        self._initialize_parent_item(id)
        item = self._get(work_id=id, id=item_id)
        return self._serializer(item).data

    @api_func('Update work item', item_name='work item', url_tail='/works/1/items/1',
              request=ExampleWorkItems.ITEM1.set(),
              response=ExampleWorkItems.ITEM1.get(),
              status_codes={403: 'can not change work item after outbound/returned items was closed',
                            422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of work',
                       'item_id': 'ID of selected work item for get'})
    def put(self, id: int, item_id: int):
        work = self._initialize_parent_item(id)

        self._save_original_before_populate(id)
        item = self._put_populate(work_id=id, id=item_id)
        changed_fields = self._get_populate_diff(item).keys()

        if self.__is_tried_to_change_closed(work, changed_fields):
            abort(403, message='Work item was closed.')

        return self._put_commit(item)

    @api_func('Delete work item', item_name='work item', url_tail='/works/1/items/1',
              response=None,
              queries={'id': 'ID of work',
                       'item_id': 'ID of selected work item for get'})
    def delete(self, id: int, item_id: int):
        self._initialize_parent_item(id)
        item = self._delete_get_item(work_id=id, id=item_id)
        return self._delete_commit(item)

    def __is_tried_to_change_closed(self, work, changed_fields):
        if work.are_returned_items_closed():
            return True

        if work.are_outbound_items_closed() and any_in(['item_id', 'outbound_quantity'], changed_fields):
            return True

        return False


class WorkCloseOutboundView(BaseView):
    _model = Work
    _serializer = WorkSerializer
    _deserializer = WorkDeserializer

    @api_func('Close outbound items on work', item_name='work', url_tail='/works/1/close-outbound',
              response=ExampleWorks.WORK1_OUTBOUND_CLOSED.get())
    def put(self, id: int):
        work = self._get_item_by_id(id)
        try:
            work.close_outbound_items(g.user)
        except RuntimeError as e:
            abort(422, message=e.args[0])
        return self._put_commit(work)


class WorkCloseReturnedView(BaseView):
    _model = Work
    _serializer = WorkSerializer
    _deserializer = WorkDeserializer

    @api_func('Close returned items on work', item_name='work', url_tail='/works/1/close-returned',
              response=ExampleWorks.WORK1_RETURNED_CLOSED.get())
    def put(self, id: int):
        work = self._get_item_by_id(id)
        try:
            work.close_returned_items(g.user)
        except RuntimeError as e:
            abort(422, message=e.args[0])
        return self._put_commit(work)
