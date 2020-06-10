from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))



class BaseConfiguration(object):
    ENV = 'Development'
    SECRET_KEY = 'flask-session-insecure-secret-key'
    HASH_ROUNDS = 100000
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'flask-tracking.db')
    SQLALCHEMY_ECHO = False
    SQALCHEMY_TRACK_MODIFICATIONS = True



class TestConfiguration(BaseConfiguration):
    TESTING = True
    WTF_CSRF_ENABLED = False
    HASH_ROUNDS = 1000
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # + join(_cwd, 'testing.db')



class DebugConfiguration(BaseConfiguration):
    DEBUG = True
    ERROR_LOG_PATH = 'errors_log.txt'

