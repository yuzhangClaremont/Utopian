Utopian Rainbow

cmd + shift + r (hard refresh)

# User registration
https://www.youtube.com/watch?v=8aTnmsDMldY

## intro to Flask-login
pip install flask-login

### setup database
pip install Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

## install Flask-WTF
http://flask-wtf.readthedocs.io/en/stable/install.html
$ pip install Flask-WTF

## install flask-bootstrap
pip install flask-bootstrap 

# SQLite
sqlite3 test.db
create table employees(id integer primary key, name text);

.help
.databases
.tables
.exit
ctrl+d exit

python in virtualenv
>>> from utopianRaibow import db
>>> db.create_all() 

sqlite3 database.db
.tables
sqlite> select * from user;

# upload file to database 
pretty print

>>> from utopianRainbow import db
>>> from utopianRainbow import User
>>> newuser = User(1,'username1', 'email@email.com',' password', 'heashot')
>>> db.session.add(newuser)
 db.session.commit()

 ### sqalchemy
 User.query.all()
 User.query.filter_by(username='xxx')
 user = User.query.get(1)
 user.posts

 db.drop_all() # drop all table and rows

 ## errors

 ### method not allowed
post request or get request
```
@app.route(..., methods=['GET', 'POST'])
```

## flash

from flask import flash

@app...
    if form.validate_on_submit():
        flash(f'account created for {form.username.data}')

## deploy on heroku

pip freeze > requirements.txt

heroku login

pip3 install gunicorn

touch Procfile

heroku apps:destroy appname

heroku apps

heroku --help

Creating app... done, ⬢ pure-garden-35230
https://pure-garden-35230.herokuapp.com/ | https://git.heroku.com/pure-garden-35230.git