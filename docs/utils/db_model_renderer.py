#!../../server/flask/bin/python3
import sys
import os
import sadisplay
import graphviz
from operator import attrgetter
from flask_sqlalchemy import _BoundDeclarativeMeta as ModelType


class DbModelRenderer:
    def __init__(self, output_filename: str, output_directory: str='.', show_indexes: bool=False,
                 show_active_components: bool=False):
        self.__output_directory = output_directory
        self.__output_filename = output_filename
        self.__show_indexes = show_indexes
        self.__show_active_components = show_active_components
        self.__graphviz_data = None

    def load_db_models(self) -> 'DbModelRenderer':
        models = self.__fetch_db_models()
        dot_file_content = self.__generate_graphviz_dot_file_content(models)
        self.__graphviz_data = graphviz.Source(dot_file_content)
        return self

    def __fetch_db_models(self) -> list:
        from app import models

        db_models = [obj for name, obj in models.__dict__.items() if type(obj) == ModelType]
        db_models.sort(key=attrgetter('__name__'))

        return db_models

    def __generate_graphviz_dot_file_content(self, db_models) -> str:
        desc = sadisplay.describe(db_models,
                                  show_indexes=self.__show_indexes,
                                  show_simple_indexes=False,
                                  show_columns_of_indexes=False,
                                  show_methods=self.__show_active_components,
                                  show_properties=self.__show_active_components)
        return sadisplay.dot(desc)

    def render_image(self, format: str, last_output_file: bool=False) -> 'DbModelRenderer':
        sys.stdout.write('Rendering DB model file {path}.{format}... '.format(
            path=os.path.join(self.__output_directory, self.__output_filename),
            format=format
        ))
        sys.stdout.flush()

        self.__graphviz_data.format = format
        self.__graphviz_data.render(self.__output_filename, self.__output_directory, cleanup=last_output_file)

        sys.stdout.write('done\n')
        return self


def __initialize_application():
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    sys.path.insert(0, os.path.join(basedir, 'server'))
    import app
    app.doc_mode = True

    # have to load before loading models
    import app.server


if __name__ == '__main__':
    filename = 'model'
    if len(sys.argv[1:]):
        filename = sys.argv[1]

    __initialize_application()

    DbModelRenderer(filename, output_directory=os.path.abspath('.'), show_indexes=True, show_active_components=True)\
        .load_db_models()\
        .render_image(format='png', last_output_file=True)
