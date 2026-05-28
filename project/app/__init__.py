from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()


def create_app(config_name='default'):
    # 工厂函数：按配置名创建Flask实例，注册3个Blueprint，初始化数据库
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    CORS(app, resources={r'/api/*': {'origins': app.config.get('CORS_ORIGINS', '*')}})
    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp)

    with app.app_context():
        from app import models  # noqa: F401

        db.create_all()

    return app
