from flask.ext.restful import abort

from app.models import Work, WorkItem
from app.views.base_views import BaseListView, BaseView
from app.modules.common import any_in
from app.modules.example_data import ExampleWorks, ExampleWorkItems
from app.serializers import WorkSerializer, WorkDeserializer, WorkItemSerializer, WorkItemDeserializer
from app.views.common import api_func


class WorkListView(BaseListView):
    _model = Work
    _serializer = WorkSerializer()
    _deserializer = WorkDeserializer()

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
    _serializer = WorkSerializer()
    _deserializer = WorkDeserializer()

    @api_func('Get work', item_name='work', url_tail='/works/1',
              response=ExampleWorks.WORK1.get())
    def get(self, id: int):
        return self._get(id=id)

    @api_func('Update work', item_name='work', url_tail='/works/1',
              request=ExampleWorks.WORK1.set(change={'comment': 'Something are not finished'}),
              response=ExampleWorks.WORK1.get(change={'comment': 'Something are not finished'}))
    def put(self, id: int):
        return self._put(id=id)

    @api_func('Delete work', item_name='work', url_tail='/works/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id=id)


class WorkItemListView(BaseListView):
    _model = WorkItem
    _parent_model = Work
    _serializer = WorkItemSerializer()
    _deserializer = WorkItemDeserializer()

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


class WorkItemView(BaseView):
    _model = WorkItem
    _parent_model = Work
    _serializer = WorkItemSerializer()
    _deserializer = WorkItemDeserializer()

    @api_func('Get work item', item_name='work item', url_tail='/works/1/items/1',
              response=ExampleWorkItems.ITEM1.get(),
              queries={'id': 'ID of work',
                       'item_id': 'ID of selected work item for get'})
    def get(self, id: int, item_id: int):
        self._initialize_parent_item(id)
        return self._get(work_id=id, id=item_id)

    @api_func('Update work item', item_name='work item', url_tail='/works/1/items/1',
              request=ExampleWorkItems.ITEM1.set(),
              response=ExampleWorkItems.ITEM1.get(),
              status_codes={403: 'can not change work item after outbound/returned items was closed',
                            422: '{{ original }} / can not add one item twice'},
              queries={'id': 'ID of work',
                       'item_id': 'ID of selected work item for get'})
    def put(self, id: int, item_id: int):
        work = self._initialize_parent_item(id)

        original_item = self._get_item_by_id(item_id)
        self._save_original_before_populate(original_item)

        modified_item = self._put_populate(work_id=id, id=item_id)
        changed_fields = self._get_populate_diff(modified_item).keys()

        if self.__is_tried_to_change_closed(work, changed_fields):
            abort(403, message='Work item was closed.')

        return self._put_commit(modified_item)

    @api_func('Delete work item', item_name='work item', url_tail='/works/1/items/1',
              response=None,
              status_codes={403: 'can not delete work item after outbound/returned items was closed'},
              queries={'id': 'ID of work',
                       'item_id': 'ID of selected work item for get'})
    def delete(self, id: int, item_id: int):
        work = self._initialize_parent_item(id)

        if work.are_items_frozen():
            abort(403, message='Can not delete item.')

        return self._delete(work_id=id, id=item_id)

    def __is_tried_to_change_closed(self, work, changed_fields):
        if work.are_returned_items_closed():
            return True

        if work.are_outbound_items_closed() and any_in(['item_id', 'outbound_quantity'], changed_fields):
            return True

        return False


class WorkCloseOutboundView(BaseView):
    _model = Work
    _serializer = WorkSerializer()
    _deserializer = WorkDeserializer()

    @api_func('Close outbound items on work', item_name='work', url_tail='/works/1/close-outbound',
              response=ExampleWorks.WORK1_OUTBOUND_CLOSED.get(),
              status_codes={422: '{{ original }} / outbound items have been closed /'
                                 'insufficient quantities for close the outbound work items'})
    def put(self, id: int):
        work = self._get_item_by_id(id)

        if work.are_outbound_items_closed():
            abort(422, message='Outbound items have been closed.')

        work_items = WorkItem.query.filter_by(work_id=work.id).all()
        self._apply_item_changes(
            model_items=work_items,
            insufficient_quantity_error_message='insufficient quantities for close the outbound work items',
            item_quantity_field='outbound_quantity',
            multiplier_for_sign=-1,
        )

        self._close_items(work.close_outbound_items)
        return self._put_commit(work)


class WorkCloseReturnedView(BaseView):
    _model = Work
    _serializer = WorkSerializer()
    _deserializer = WorkDeserializer()

    @api_func('Close returned items on work', item_name='work', url_tail='/works/1/close-returned',
              response=ExampleWorks.WORK1_RETURNED_CLOSED.get(),
              status_codes={422: '{{ original }} / outbound items have not been closed / '
                                 'returned items have been closed /'
                                 'insufficient quantities for close the returned work items'})
    def put(self, id: int):
        work = self._get_item_by_id(id)

        if not work.are_outbound_items_closed():
            abort(422, message='Outbound items have not been closed.')
        elif work.are_returned_items_closed():
            abort(422, message='Returned items have been closed.')

        work_items = WorkItem.query.filter_by(work_id=work.id).all()
        self._apply_item_changes(
            model_items=work_items,
            insufficient_quantity_error_message='insufficient quantities for close the returned work items',
            item_quantity_field='returned_quantity',
        )

        self._close_items(work.close_returned_items)
        return self._put_commit(work)
