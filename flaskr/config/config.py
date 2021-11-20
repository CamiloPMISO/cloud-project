class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass_flask@db:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = 'frase-secreta'
    broker_url = 'redis://broker_redis:6379/0'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    

class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass_flask@db:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_SECRET_KEY = 'frase-secreta'
    broker_url = 'redis://broker_redis:6379/0'


cfg = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig
}