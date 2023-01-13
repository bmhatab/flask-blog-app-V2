from flask import Flask
from app.venv import config
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager




db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()




def create_app():
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)
    config.DevelopmentConfig.init_app(app)
    db.init_app(app=app)
    migrate = Migrate(app=app,db=db)
    from app.main import main
    from app.models import Users, Posts
    app.register_blueprint(main)
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(id):
    #replace this with your own user loading function
         return Users.query.get(id)


    login_manager.init_app(app=app)
    login_manager.login_view = 'main.login'
    

    # Add error routes and Custom pages


    return app



