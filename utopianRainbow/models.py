from datetime import datetime
from utopianRainbow import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader # get user by id decorater
def load_user(user_id):
    return User.query.get(int(user_id))

# friendship = Table(
#     'friendships', Base.metadata,
#     Column('user_id', Integer, ForeignKey('users.id'), index=True),
#     Column('friend_id', Integer, ForeignKey('users.id')),
#     UniqueConstraint('user_id', 'friend_id', name='unique_friendships'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    # notification = db.relationship('Nolification', backref='user',lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    # friends = relationship('User',
    #                        secondary=friendship,
    #                        primaryjoin=id==friendship.c.user_id,
    #                        secondaryjoin=id==friendship.c.friend_id)


    def befriend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
            friend.friends.append(self)

    def unfriend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            friend.friends.remove(self)

    def __repr__(self):
        return '<User(name=|%s|)>' % self.name

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# class Nolification(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(20), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     content = db.Column(db.Text, nullable=False)
#     receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     sender = db.relationship('User', backref='noli', lazy='dynamic')
    # comments = db.relationship('Comment', backref='post', lazy='dynamic')

    # def __repr__(self):
    #     return f"Nolification('{self.title}', '{self.date_posted}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    # body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

   

    def __repr__(self):
        return f"Comment('{self.body}','{self.author}', '{self.timestamp}')"

class NGO(db.Model):
    __tablename__='ngo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # city = db.Column(db.String(30), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    website = db.Column(db.String(150), nullable=False)
    rate = db.Column(db.Integer, default=0)
    intro = db.Column(db.String(500))
    activities = db.relationship('Activities', backref='organizer', lazy=True)
    jobs = db.relationship('Jobs', backref='employers', lazy=True)
   

    def __repr__(self):
        return f"NGO('{self.name}','{self.city_id}')"

class Activities(db.Model):
    __tablename__='activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # city = db.Column(db.String(30), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    time = db.Column(db.DateTime,  nullable = False)
    intro = db.Column(db.String(500), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('ngo.id'), nullable=False)

    def __repr__(self):
        return f"Activities('{self.name}','{self.city}')"

class Jobs(db.Model):
    __tablename__='jobs'
    id = db.Column(db.Integer, primary_key=True)
    hirePos = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    time = db.Column(db.DateTime,  nullable = False)
    hireReq  = db.Column(db.String(500), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('ngo.id'), nullable=False)

    def __repr__(self):
        return f"Jobs('{self.hirePos}','{self.city}')"

class City(db.Model):
    __tablename__='city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    ngo = db.relationship('NGO', backref='city', lazy=True)
    activities = db.relationship('Activities', backref='city', lazy=True)
    jobs = db.relationship('Jobs', backref='city', lazy=True)
    def __repr__(self):
        return f"city('{self.name}','{self.ngo}')"