from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# 这种foreign key只用在一对多的情况下。
class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))# foreign里面放primary_key

class User(db.Model,UserMixin):
    # 需要一个标记，区分不同用户，就是id
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True) # unique指的是不能有相同的邮箱。每个邮箱是唯一的
    password = db.Column(db.String(250))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')