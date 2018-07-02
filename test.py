from flask import Flask, render_template, url_for, redirect, request, send_file
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
# from flask_mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from io import BytesIO # convert data from database into bytes
from datetime import datetime
import os
import secrets
from PIL import Image



# from passlib.hash import sha256_crypt
app = Flask(__name__)

app.config['SECRET_KEY']='Thisissecret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/yunzhang/Documents/computer Science/UTOPIAN/database.db'
Bootstrap(app)
db = SQLAlchemy(app)

# from models import User, Post
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "user('{self.title}','{self.date_posted}')"

class User(UserMixin, db.Model):
    __tablename___ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(15))
    email=db.Column(db.String(50))
    password = db.Column(db.String(80))
    headshot = db.Column(db.String(200),nullable=False, default='default.png')
    posts = db.relationship('Post', backref='author', lazy=True) #backref add another col to post, use this attribute to find author of post, lazy can post all post of a user

    # print method
    def __repr__(self):
        return "user('{self.username}','{self.email}','{self.headshot}')"



    # def __init__(self, id, username, email, password, headshot):
    #     self.id = id
    #     self.username=username
    #     self.email = email
    #     self.password = password
    #     self.headshot = headshot

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
# @app.route("/index")
@app.route("/<username>")
def index(username=None):
    # if username != None:
        return render_template("index.html",username =username )
    # else:
        # return render_template("index.html")

@app.route("/aboutus/")
@app.route("/aboutus/<username>")
def aboutus(username=None):
    return render_template("aboutus.html",username = username)

@app.route("/ngo/")
@app.route("/ngo/<username>")
def ngo(username=None):
    # form = LoginForm()
    # if username != None:
    return render_template('ngo.html', username=username)
    # else:
        # return render_template("ngo.html")
        
@app.route("/fellowship")
@app.route("/fellowship/<username>")
def fellowship(username=None):
    return render_template("fellowship.html", username = username)

@app.route("/community")
@app.route("/community/<username>")
def community(username=None):
    return render_template("community.html", username=username)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/dashboard/<username>")
# @app.route("/dashboard/")
@login_required
def dashboard(username=None):
    img = save_picture(current_user.headshot.data)
    image_file = url_for('static', filename='image/'+img)
    return render_template("dashboard.html", username=current_user.username, image_file=image_file)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # first result in database, username suppost to be unique
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user, remember=form.remember.data)
            # if user.password== form.password.data:
                return redirect(url_for('dashboard',username = form.username.data))
        return render_template("login.html", form=form, login_fail = 1)
    return render_template("login.html", form=form, username = form.username.data)

@app.route("/signup", methods=['GET','POST'])
def signup():
    form=RegisterForm()
    userCount = User.query.filter_by(username=form.username.data).count()
    emailCount = User.query.filter_by(email=form.email.data).count()
        
    if form.validate_on_submit() and (userCount + emailCount) < 1:
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user= User(username=form.username.data, email=form.email.data, password=hashed_password, headshot=None)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('dashboard',username = form.username.data))
    else:
        return render_template("signup.html",form=form, signup_fail=1)

    return render_template("signup.html",form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/edit/<username>')
def edit(username=None):
    return render_template("edit.html",username = username)

@app.route('/headshot', methods=['POST'])
def headshot():
    file = request.files['inputFile']
    user = User.query.filter_by(username = current_user.username).first()
    user.headshot = file.read()

    # db.session.delete(user) # delete a row

    # newFile = User(headshot=file.read())
    # db.session.add(newFile)
    db.session.commit()
    # return redirect(url_for('dashboard',username=username))

    # headData = FileContents.query.filter_by(username=current_user.username).first()
    # return send_file(BytesIO(file_data.data),attachment_filename="flask.pdf",as_attachment=True)
    user_image = url_for('static', filename='current_user.headshot') 
    return render_template("dashboard.html", username=current_user.username, user_image = user_image)

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