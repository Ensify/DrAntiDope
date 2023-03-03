from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),unique=True,nullable=False)
    password =db.Column(db.String(100),nullable=False)
    username=db.Column(db.String(30),nullable=False)
    profile_pic=db.Column(db.String(20),nullable=False,default='default.jpg')
    sport=db.Column(db.String(50))
    #drugs= db.relationship('SearchedDrug')
    posts= db.relationship('Post',backref='author',lazy=True)

    def __repr(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

# class SearchedDrug(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String(50))
#     user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

# class Threads_created(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     title=db.Column(db.String(50))
#     thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
#     user_id=db.Column(db.Integer, db.ForeignKey('user.id'))

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr(self):
        return f"User('{self.title}','{self.date_posted}')"
    