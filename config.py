from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))



class BaseConfiguration(object):
    HASH_ROUNDS = 100000
    SECRET_KEY = 'flask-session-insecure-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'flask-tracking.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False



class DevelopmentConfiguration(BaseConfiguration):
    DEBUG = True
    ENV = 'Development'
    ERROR_LOG_PATH = 'errors_log_dev.txt'



class TestConfiguration(BaseConfiguration):
    DEBUG = False
    ENV = "Testing"
    ERROR_LOG_PATH = 'errors_log_test.txt'
    HASH_ROUNDS = 1000
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # + join(_cwd, 'testing.db')
    TESTING = True



class ProductionConfiguration(BaseConfiguration):
    ENV = "Production"
    ERROR_LOG_PATH = 'errors_log_prod.txt'