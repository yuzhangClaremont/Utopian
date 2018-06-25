
from datetime import datetime
from utopianRainbow import db


class User(UserMixin, db.Model):
    __tablename___ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(15))
    email=db.Column(db.String(50))
    password = db.Column(db.String(80))
    headshot = db.Column(db.String(20),nullable=False, default='default.png')
    posts = db.relationship('Post', backref='author', lazy=True) #backref add another col to post, use this attribute to find author of post, lazy can post all post of a user

    # print method
    def __repr__(self):
        return "user('{self.username}','{self.email}','{self.headshot}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Test)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "user('{self.title}','{self.date_posted}')"