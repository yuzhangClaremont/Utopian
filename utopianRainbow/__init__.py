from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
# from flask_mysqldb import MySQL
import os
from flask_googlemaps import GoogleMaps, Map

application = Flask(__name__)

application.config['SECRET_KEY']='Thisissecret'
application.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:20021991@localhost/mysqlUTOPIAN'
db = SQLAlchemy(application )
# db = MySQL(app)
bcrypt = Bcrypt(application )
login_manager = LoginManager(application )
login_manager.login_view = 'login' # for login required decoed route, redirect to lgoin page
login_manager.login_message_category = 'info' # make the message about in to info bootstrap style

application.config['MAIL_SERVER'] = 'smtp.googlemail.com'
application.config['MAIL_PORT'] = 587
# app.config['MAIL_SERVER'] = 'smtp.sina.com'
# app.config['MAIL_PORT'] = 25
application.config['MAIL_USE_TLS'] = True
application.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
application.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(application)

application.config['GOOGLEMAPS_KEY'] = 'AIzaSyCg6SzshqdaxNJX0FupvjX177MX7V71X48'
map = GoogleMaps(application)

from utopianRainbow import routes