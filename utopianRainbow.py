from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# from flask_mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# from passlib.hash import sha256_crypt
app = Flask(__name__)

app.config['SECRET_KEY']='Thisissecret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/yunzhang/Documents/computer Science/UTOPIAN/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(15),unique=True)
    email=db.Column(db.String(50),unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(),Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8,max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email',validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    username = StringField('username', validators=[InputRequired(),Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8,max=80)])
  

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/aboutus/")
def aboutus():
    return render_template("aboutus.html")

@app.route("/ngo/")
def ngo():
    return render_template("ngo.html")

@app.route("/fellowship")
def fellowship():
    return render_template("fellowship.html")

@app.route("/community")
def community():
    return render_template("community.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # first result in database, username suppost to be unique
        if user:
            if check_password_hash(user.password,form.password.data):
            # if user.password== form.password.data:
                return redirect(url_for('dashboard'))
        return 'invalid username or password'
    return render_template("login.html", form=form)

@app.route("/signup", methods=['GET','POST'])
def signup():
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user= User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>'+ form.email.data +'</h1>'

    return render_template("signup.html",form=form)

@app.route("/chineseIndex")
def chineseIndex():
    return render_template("chineseIndex.html")

# https://wtforms.readthedocs.io/en/stable/

# class RegisterForm(Form):
#     username= StringField('username',[validators.Length(min=4,max=25)])
#     email = StringField('Email', [validators.Length(min=6,max=50)])
#     password = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm',message='passwords do not match')
#     ])
#     confirm = PasswordField('confirm password')

# @app.route('/register',methoods=['GET','POST'])
# def register():
#     form = RegisterForm(request.form)
#     if request.method == 'POST' and form.validate():

#         return render_template('register.html',form=form)

if __name__ == "__main__":
    app.run(debug=True)