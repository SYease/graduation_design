"""
Flask应用工厂
============================================================
思路说明：
使用Flask的"应用工厂"模式（Application Factory Pattern）。
这是Flask官方推荐的项目组织方式，好处是：
1. 避免循环导入问题
2. 方便创建多个应用实例（如测试时）
3. 延迟初始化扩展（db等），更灵活

create_app() 函数负责：
1. 创建Flask实例
2. 加载配置
3. 初始化数据库扩展
4. 注册所有蓝图（Blueprint）
5. 创建数据库表
============================================================
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 在模块级别创建db实例，但不绑定到任何app
# 这样其他模块可以 from app import db 来使用
db = SQLAlchemy()


def create_app(config_name='default'):
    """
    应用工厂函数

    参数:
        config_name: 配置名称，可选 'development'/'production'/'default'
    返回:
        配置好的Flask应用实例
    """
    # 创建Flask实例，指定模板和静态文件目录
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')

    # 从配置对象加载配置
    from config import config as config_dict
    app.config.from_object(config_dict[config_name])

    # 初始化扩展
    db.init_app(app)          # 数据库ORM
    CORS(app)                 # 跨域支持

    # 注册蓝图（Blueprint）
    # 蓝图是Flask组织路由的方式，类似于Django的app
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    app.register_blueprint(main_bp)                    # 主页面路由
    app.register_blueprint(api_bp, url_prefix='/api')  # API路由，统一加 /api 前缀

    # 在应用上下文中创建所有数据库表
    with app.app_context():
        from app import models  # 确保模型被导入，这样db才知道要创建哪些表
        db.create_all()

    return app
