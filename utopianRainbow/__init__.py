from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)

app.config['SECRET_KEY']='Thisissecret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # for login required decoed route, redirect to lgoin page
login_manager.login_message_category = 'info' # make the message about in to info bootstrap style

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
# app.config['MAIL_SERVER'] = 'smtp.sina.com'
# app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)

app.config['GOOGLEMAPS_KEY'] = 'AIzaSyCg6SzshqdaxNJX0FupvjX177MX7V71X48'
map = GoogleMaps(app)

from utopianRainbow import routes