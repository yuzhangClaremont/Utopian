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

git push heroku master

heroku open

echo "python-3.6.5" > runtime.txt

### launch on AWS

## Elastic Beanstalk

IAM

YUN
programatic access

permission
wselasticbeanstalkfullaccess

pip3 install awscli
pip3 install awsebcli
eb init -i

Enter same passphrase again: 
Your identification has been saved in /Users/yunzhang/.ssh/prototyping4.
Your public key has been saved in /Users/yunzhang/.ssh/prototyping4.pub.
The key fingerprint is:
SHA256:jOwv3AXvKhDbkXiASPaOUQRX9l+ry4+uYrB2+/zHcQ0 prototyping4
The key's randomart image is:
20021991

```
eb create utopist
```


Environment details for: utopist
  Application name: UTOPIAN
  Region: us-west-2
  Deployed Version: app-a836-180723_220904
  Environment ID: e-pbm967ufmf
  Platform: arn:aws:elasticbeanstalk:us-west-2::platform/Python 3.6 running on 64bit Amazon Linux/2.7.1
  Tier: WebServer-Standard-1.0
  CNAME: UNKNOWN
  Updated: 2018-07-23 14:11:17.448000+00:00
Printing Status:
2018-07-23 14:11:16    INFO    createEnvironment is starting.
2018-07-23 14:11:17    INFO    Using elasticbeanstalk-us-west-2-743248756403 as Amazon S3 storage bucket for environment data.
2018-07-23 14:11:44    ERROR   Stack named 'awseb-e-pbm967ufmf-stack' aborted operation. Current state: 'CREATE_FAILED'  Reason: The following resource(s) failed to create: [AWSEBLoadBalancer, AWSEBSecurityGroup]. 
2018-07-23 14:11:44    INFO    Created security group named: sg-06972d5b5d9488328
2018-07-23 14:11:44    ERROR   Creating load balancer failed Reason: API: elasticloadbalancing:CreateLoadBalancer User: arn:aws:iam::743248756403:user/YUN is not authorized to perform: iam:CreateServiceLinkedRole on resource: arn:aws:iam::743248756403:role/aws-service-role/elasticloadbalancing.amazonaws.com/AWSServiceRoleForElasticLoadBalancing
2018-07-23 14:11:44    ERROR   Creating security group named: awseb-e-pbm967ufmf-stack-AWSEBSecurityGroup-RP769GWP2UWV failed Reason: Resource creation cancelled
2018-07-23 14:11:45    INFO    Launched environment: utopist. However, there were issues during launch. See event log for details.
                                
```
eb open utopist
```

https://aws.amazon.com/getting-started/tutorials/update-an-app/