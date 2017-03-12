import os
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import User
#@logina ezafe kon bebin javab mide
#from app import *

app = Flask(__name__)
#for adding the ability of loading static files !
app._static_folder = os.path.abspath("static")
app.config.from_object('app.config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app import views, models
#sh i d ?
@login_manager.user_loader
def load_user(id):
    try :
        return User.query.get(int(id))
    except:
        pass

#@app.before_first_request
#def create_database():
#     db.create_all()