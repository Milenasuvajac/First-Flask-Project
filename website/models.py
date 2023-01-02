from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


tasks = db.Table('tags',
db.Column('user_id',db.Integer,db.ForeignKey("user.id"), primary_key = True),
db.Column('note_id',db.Integer,db.ForeignKey("note.id"), primary_key = True))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone = True),default = func.now())
    user_id = db.relationship('User',secondary = tasks,backref = "notes")
    finish = db.Column(db.Boolean, default = False, nullable = False)
    dailytask = db.Column(db.Boolean, default = False)
    duration = db.Column(db.Integer)
    
    def __repr__(self):
        return f'Task: "{self.data}"'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(50))

    def __repr__(self):
        return f'{self.name}'

