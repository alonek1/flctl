
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#make a column of user
class User(db.Model):
    #primary ID
    id = db.Column(db.Integer, primary_key=True)
    #Username of auth
    username = db.Column(db.String(20), index=True, unique=True)
    #Password for auth
    password = db.Column(db.String(120), index=True, unique=False)

    def __init__(self , username ,password):
        self.username = username
        self.password = password

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)  # python 3

    #this part is for debuging
    def __repr__(self):
        return '<User %r>' % (self.username)

