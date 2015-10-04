

class ConfigMock:
    def __init__(self, used_config: str='ProductionConfig'):
        self.used_config = used_config

    def config_reader(self, *args, **kwargs)-> str:
        config = """USED_CONFIG: {!s}


DefaultConfig:
  DebugId: Default
  App:
    UTF8_VALUE: 'Több hűtőházból kértünk színhúst'

    MIGRATE_REPO_PATH: $BASEDIR/db_repository

  Flask:
    # http://flask.pocoo.org/docs/0.10/config/
    SERVER_NAME: 0.0.0.0:8000
    STATIC_FOLDER: /test
    DEBUG: False
    TESTING: False

  SqlAlchemy:
    # https://pythonhosted.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_DATABASE_URI: sqlite://$BASEDIR/app.sqlite


ProductionConfig:
  Base: DefaultConfig
  DebugId: Production

  SqlAlchemy:
    SQLALCHEMY_DATABASE_URI: mysql+mysqlconnector://tasks:a@localhost/tasks


DevelopmentConfig:
  Base: DefaultConfig
  DebugId: Development

  Flask:
    DEBUG: True


TestingConfig:
  Base: DefaultConfig
  DebugId: Testing

  Flask:
    TESTING: True


DependencyTopConfig:
  Base: DependencyMiddleConfig
  DebugId: DependencyTop

  DependencyLevel:
    1: Top


DependencyMiddleConfig:
  Base: DependencyBottomConfig
  DebugId: DependencyMiddle

  DependencyLevel:
    1: Middle
    2: Middle


DependencyBottomConfig:
  DebugId: DependencyBottom

  DependencyLevel:
    1: Bottom
    2: Bottom
    3: Bottom


MinimalCircularConfig:
  Base: MinimalCircularConfig
  DebugId: MinimalCircular


MultiCircularConfigTop:
  Base: MultiCircularConfigMiddle
  DebugId: MultiCircularTop


MultiCircularConfigMiddle:
  Base: MultiCircularConfigBottom
  DebugId: MultiCircularBottom


MultiCircularConfigBottom:
  Base: MultiCircularConfigTop
  DebugId: MultiCircularBottom

"""
        return config.format(self.used_config)
