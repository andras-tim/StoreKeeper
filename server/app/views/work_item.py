from app.models import WorkItem
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleWorkItems
from app.serializers import WorkItemSerializer
from app.server import config, api
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
              status_codes={422: '{{ original }} / can not add one item twice'})
    def post(self):
        return self._post()


class WorkItemView(BaseView):
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
              status_codes={422: '{{ original }} / can not add one item twice'})
    def put(self, id: int):
        return self._put(id)

    @api_func('Delete work item', item_name='work item', url_tail='work-items/1',
              response=None)
    def delete(self, id: int):
        return self._delete(id)


api.add_resource(WorkItemListView, '/{!s}/api/work-items'.format(config.App.NAME), endpoint='work_items')
api.add_resource(WorkItemView, '/{!s}/api/work-items/<int:id>'.format(config.App.NAME), endpoint='work_item')
