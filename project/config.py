import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

#基础配置
class Config:
    #密匙
    SECRET_KEY = 'default-key'
    #数据库设置
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    #知识图谱推荐系统
    KNOWLEDGE_GRAPH_FILE = os.path.join('data', 'knowledge_graph.json')
    RECOMMENDATION_algorithm = 'cognitive_diagnosis'
    MAX_RECOMMENDATIONS = 5

    #邮箱登录系统
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True

#开发环境
class DevelopmentConfig(Config):
    #调试
    DEBUG=True
    #数据库配置
    SQLALCHEMY_DATABASE_URI='sqlite:///instance/algo_learning_sys.db'
    #开发环境使用推荐算法
    RECOMMENDATION_algorithm = 'mock'

#生产环境
class ProductionConfig(Config):
    #数据库配置
    SQLALCHEMY_DATABASE_URI='sqlite:///instance/algo_learning_sys.db'

    RECOMMENDATION_algorithm = 'cognitive_diagnosis'

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

class TestingConfig(Config):
    TESTING=True
    #数据库配置
    SQLALCHEMY_DATABASE_URI='sqlite:///instance/algo_learning_sys.db'

    RECOMMENDATION_algorithm = 'simple'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
