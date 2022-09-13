from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path
from flask_login import LoginManager
from pymongo import MongoClient  

db=SQLAlchemy()
DB_NAME = "database.db"

client = MongoClient("mongodb+srv://SarumathyPrabakaran:sarumathy@cluster0.lbdvmf4.mongodb.net/?retryWrites=true&w=majority") #host uri    
mdb = client['Dr-Dope']   
tabl = mdb['drug']

def create_app():
    global bcrypt
    app=Flask(__name__)
    app.config["SECRET_KEY"] = "623b6dae5e5c8b81e1e1da071971b46b8eaefbcf"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    bcrypt =Bcrypt(app)

    from website.users.routes import users
    from website.main.routes import main
    from website.drug.routes import drug
    from website.posts.routes import posts

    app.register_blueprint(users,url_prefix="/")
    app.register_blueprint(main,url_prefix="/")
    app.register_blueprint(drug,url_prefix="/")
    app.register_blueprint(posts,url_prefix="/")

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.login_message_category="info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print('Created Database')