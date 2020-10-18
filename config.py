import os


# FLASK CONFIG
class Config:
    # FLASK CONFIG
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_ENGINE_OPTIONS = {'max_identifier_length': 128}
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


config = {"production_config": ProductionConfig,
          "default": ProductionConfig}
