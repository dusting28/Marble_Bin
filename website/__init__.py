from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cheatdragon'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = path.join('website','static','uploads')
    db.init_app(app)

    from .views_home import views_home
    from .views_auth import views_auth
    from .views_marbles import views_marbles
    from .views_tournaments import views_tournaments

    app.register_blueprint(views_home, url_prefix='/')
    app.register_blueprint(views_auth, url_prefix='/')
    app.register_blueprint(views_marbles, url_prefix='/')
    app.register_blueprint(views_tournaments, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'views_auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
