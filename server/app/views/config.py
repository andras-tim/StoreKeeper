from flask.ext import restful

from app.modules.example_data import ExampleConfigs
from app.serializers import ConfigSerializer
from app.server import config
from app.views.common import api_func


class ConfigView(restful.Resource):
    @api_func('Get server settings', url_tail='config',
              login_required=False,
              response=ExampleConfigs.CONFIG1.get())
    def get(self):
        client_related_config = {
            'app_name': config.App.NAME,
            'app_title': config.App.TITLE,
        }
        return ConfigSerializer(client_related_config).data
