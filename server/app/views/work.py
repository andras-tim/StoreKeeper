from flask import g
from flask.ext.restful import abort

from app.models import Work
from app.modules.base_views import BaseModelListView, BaseView
from app.modules.example_data import ExampleWorks
from app.serializers import WorkSerializer, WorkDeserializer
from app.views.common import api_func


class WorkListView(BaseModelListView):
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
