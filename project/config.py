import os

try:
    from dotenv import load_dotenv  # type: ignore
except ModuleNotFoundError:
    def load_dotenv():
        return False

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(INSTANCE_DIR, 'algo_learning_sys.db')}")

    KNOWLEDGE_GRAPH_FILE = os.path.join(BASE_DIR, 'data', 'knowledge_graph.json')
    MAX_RECOMMENDATIONS = int(os.environ.get('MAX_RECOMMENDATIONS', 5))

    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True

    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'rule_based')
    AI_MODEL = os.environ.get('AI_MODEL', '')
    AI_API_KEY = os.environ.get('AI_API_KEY', '')
    AI_BASE_URL = os.environ.get('AI_BASE_URL', '')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
