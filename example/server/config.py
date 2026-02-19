"""
配置文件
============================================================
思路说明：
将应用配置集中管理，区分开发/生产/测试环境。
数据库使用SQLite，简单轻量，适合毕业设计演示。
============================================================
"""
import os

# 获取当前文件所在目录的绝对路径，用于构建其他路径
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """基础配置，所有环境共享"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'quicksort-learning-system-2024')
    # SQLite数据库文件放在instance目录下
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'learning.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 知识图谱数据文件路径
    KNOWLEDGE_GRAPH_FILE = os.path.join(basedir, 'data', 'knowledge_graph.json')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


# 配置映射字典，通过字符串名称选择配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
