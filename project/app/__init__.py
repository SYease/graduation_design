from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def create_app():
    app=Flask(__name__)

    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()
    
    from app.routes.main import main_db
    app.register_blueprint(main_db)

    return app
