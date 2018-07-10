from flask import  render_template, url_for, flash, redirect, request, abort, jsonify
from utopianRainbow import app, db, bcrypt, mail, map, Map
from utopianRainbow.forms import (RegistrationForm, LoginForm, UpdateAccountForm, PostForm,
    PostCommentForm,RequestResetForm, ResetPasswordForm, NGOForm, NGOCreateForm)
from utopianRainbow.models import User, Post, Comment, City, NGO
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image
from flask_mail import Message
import pygeoip # pip3 install

# gi = pygeoip.GeoIP('GeoIPCity.dat', pygeoip.MEMORY_CACHE)

@app.route("/")
# @app.route("/index")
@app.route("/<username>")
def index(username=None):
    # if username != None:
    # posts = Post.query.all()
    return render_template("index.html",username =username )
    # else:
        # return render_template("index.html")

@app.route("/aboutus/")
@app.route("/aboutus/<username>")
def aboutus(username=None):
    if current_user.is_authenticated:
        # posts = Post.query.all()
        return render_template("aboutus.html",username = username)
    else:
        return render_template("aboutus.html")

@app.route("/ngo/admin/new/<username>", methods=['GET', 'POST'])
@login_required
def ngo_new(username=None):
    form = NGOCreateForm()
    if form.validate_on_submit():
        cityName = form.city.data[0].upper()+form.city.data[1:].lower()
        regName = form.region.data[0].upper()+form.region.data[1:].lower()
        city = City.query.filter_by(name=cityName).first()
        if city:
            ngo = NGO(city_id=city.id, name=form.name.data, intro=form.intro.data,address=form.address.data,website=form.website.data)
            db.session.add(ngo)
            db.session.commit()
        else:
            newCity = City(name = cityName, region = regName )
            db.session.add(newCity)
            db.session.commit()
            ngo = NGO(city_id=newCity.id, name=form.name.data, intro=form.intro.data,address=form.address.data,website=form.website.data)
            db.session.add(ngo)
            db.session.commit()
        flash('Your NGO info has been created!', 'success')
        return redirect(url_for('ngo', username =username))
    return render_template('NGO_create.html', form=form,username=current_user.username,
        legend = 'Create NGO info')

@app.route("/ngo/", methods=['GET','POST'])
@app.route("/ngo/<username>", methods=['GET','POST'])
@app.route('/ngo/show/<city_id>')
def ngo(username=None, city_id=None):
    CHINA_CHOICES = [('0','SELECT'),('1','YUNNAN'),('2','GUANGDONG'),('3','Beijing')]
    USA_CHOICES = [('0','SELECT'),('1','California'),('2','New York')]
    form = NGOForm()
    if form.country.data == 'China':
        form.region.choices = CHINA_CHOICES
    if form.country.data == 'USA':
        form.region.choices = USA_CHOICES
    # id = city_id
    # print(id)
    ngos = NGO.query.all()
    if request.method == 'POST':
        # print(city_id)
        city = City.query.filter_by(id = form.city.data).first()
        # print(city)
        ngos = NGO.query.filter_by(city_id = city.id).all()
        print(ngos,'CITY!!!')
        form.country.data = 0
        return render_template('ngo.html', username=username, form = form, ngos = ngos )
        # return redirect(url_for('ngo', username=username, form = form, ngos = ngos ))
    # c = form.city.data
    # print(c)
    # city = City.query.filter_by(id = city_id).first()
    # ngo = city.ngo
    # print(city)
        
        
    # for i in ngos:

    #     print(i.name)
    print(ngos,'ALL!!!')
    return render_template('ngo.html', username=username, form = form, ngos = ngos )
    # cityOfCountry = City.query.filter_by(country=form.country.data).first
    # form.region.choices = [(city.id, city.region) for city in City.query.filter_by(region=form.country).all()]

    # if request.method == 'POST':
    #     return render_template('ngo.html', username=username, form = form)

        # city = City.query.filter_by(id=form.city.data).first()
        # return '<h1>State: {}, City: {}</h1>'.format(form.state.data, city.name)
    # if username != None:
    # posts = Post.query.all()
    # url = 'http://freegeoip.net/json/{}'.format(request.remote_addr)
    # r = request.get(url)
    # j = json.loads(r.text)
    # city = j['city']

    # print(city)
    # geo_data = gi.record_by_addr(request.remote_addr)
    # print(jsonify(geo_data))
    # return render_template('ngo.html', username=username, form = form, ngos= ngos)
    # else:
        # return render_template("ngo.html")

@app.route('/ngo/select/<country>')
def region(country):
    # cities = City.query.filter_by(state=state).all()
    CHINA_CHOICES = [('0','SELECT'),('Yunnan','Yunnan'),('Guangdong','Guangdong'),('Beijing','Beijing'),('Shanghai','Shanghai')]
    USA_CHOICES = [('0','SELECT'),('California','California'),('New York','New York')]
    
    if country == 'China':
        regions = CHINA_CHOICES
    if country== 'USA':
        regions = USA_CHOICES
    regionArray = []

    for region in regions:
        regObj = {}
        regObj['id'] = region[0]
        regObj['name'] = region[1]
        regionArray.append(regObj)

    return jsonify({'regions' : regionArray})

@app.route('/ngo/select/<country>/<region>')
def city(country,region):
    # cities = City.query.filter_by(state=state).all()
    cities = City.query.filter_by(region = region).all()
    print(cities)
    cityArray = []

    select={}
    select['id']= 0
    select['name']='SELECT'
    cityArray.append(select)

    for city in cities:
        cityObj = {}
        cityObj['id'] = city.id
        cityObj['name'] = city.name
        cityArray.append(cityObj)

    return jsonify({'cities' : cityArray})
        
@app.route("/fellowship/")
@app.route("/fellowship/<username>")
def fellowship(username=None):
    # posts = Post.query.all()
    return render_template("fellowship.html", username = username)

@app.route("/community/")
@app.route("/community/<username>")
@login_required
def community(username=None):
    # if current_user.is_authenticated:
    page = request.args.get('page', 1, type=int) #requst variable from html, default at page 1
    allposts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page = page)
    return render_template("community.html",username = current_user.username, allposts = allposts)
    # else:
    #     return render_template("community.html")


@app.route("/dashboard/<username>")
# @app.route("/dashboard/")
@login_required
def dashboard(username=None):
    # form = UpdateAccountForm()
    # img = save_picture(current_user.image_file.data)
    image_file = url_for('static', filename='image/'+ current_user.image_file)
    posts = Post.query.all()
    return render_template("dashboard.html", username=username, image_file = image_file,
        posts=posts)

@app.route("/profile/<username>")
def profile(username=None):
    user = User.query.filter_by(username=username).first()
    # form = UpdateAccountForm()
    # img = save_picture(current_user.image_file.data)
    image_file = url_for('static', filename='image/'+ user.image_file)
    posts = Post.query.all()
    print(user.username, user.email)
    return render_template("profile.html",username = current_user.username ,name=user.username, image_file = image_file,
        posts=posts, email=user.email)

@app.route("/login", methods=['GET','POST'])
def login():
    # if current_user.is_authenticated: # this is a flask-login object
    #     return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(username=form.username.data).first()
        user = User.query.filter_by(email=form.email.data).first()
        # first result in database, username suppost to be unique
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data) # login user authen
            # if user.password== form.password.data:
            return redirect(url_for('dashboard',username = user.username))
        else:
            flash('the login is unsuccessful, please check username and password', 'danger')
    return render_template("login.html", form=form)

@app.route("/signup", methods=['GET','POST'])
def signup():
    form = RegistrationForm()
    userCount = User.query.filter_by(username=form.username.data).count()
    emailCount = User.query.filter_by(email=form.email.data).count()
        
    if form.validate_on_submit(): # post method
        if (userCount + emailCount) < 1:     
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user= User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('account created!','success')
            return redirect(url_for('dashboard',username = form.username.data))
        else:
            flash('the username or email has been used, please use another one~','danger')
            return render_template("signup.html",form=form, signup_fail=1)

    return render_template("signup.html",form=form)

@app.route('/logout/')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # random hex name to avoid user pic name overlap
    _, f_ext = os.path.splitext(form_picture.filename) # os to save extension, _ is unused variable which is filename
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/image', picture_fn) #save pic as the name
    # form_picture.save(picture_path)

    output_size = (225, 225)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/edit/<username>', methods=['GET','POST'])
@login_required
def edit(username=None):
    form =  UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        if form.username.data != None:
            current_user.username = form.username.data
        if form.email.data != None:
            current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # print(current_user.username, current_user.image_file)
        return redirect(url_for('dashboard',username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("edit.html",username = username, form=form)



@app.route("/post/new/<username>", methods=['GET', 'POST'])
@app.route("/post/new/")
@login_required
def new_post(username=None):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('dashboard',username=current_user.username))
    return render_template('create_post.html', form=form,username=current_user.username,
        legend = 'Create Post')

@app.route("/post/<username>/display/<title>", methods=['GET','POST'])
@login_required
def post_display(username, title):
    thisPost = Post.query.filter_by(title = title).first()
    form = PostCommentForm()
    if form.validate_on_submit():
        comment = Comment(body = form.comment.data,post_id=thisPost.id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comments added!','success')
        return redirect(url_for('post_display', username=username, title=title))
    comments = Comment.query.filter_by(post=thisPost).order_by(Comment.timestamp.desc())
    print(comments, 'the comment list is here')
    return render_template('post_display.html', post=thisPost, username=current_user.username, 
        form=form,comments = comments)

@app.route("/post/<username>/<title>/update",  methods=['GET', 'POST'])
@login_required
def post_update(username, title):
    thisPost = Post.query.filter_by(title = title).first()
    if thisPost.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        thisPost.title = form.title.data
        thisPost.content = form.content.data
        db.session.commit()
        flash('Your post have been updated', 'success')
        return redirect(url_for('post_display',
            username= current_user.username, title= thisPost.title))
    elif request.method == 'GET':
        form.title.data = thisPost.title
        form.content.data = thisPost.content
    # print(thisPost.author, current_user)
    return render_template('create_post.html', title='Update Post', 
        form=form,username=current_user.username, legend='Update Post')

@app.route("/post/<title>/delete", methods=['POST'])
# @app.route("/post/delete", methods=['POST'])
@login_required
def post_delete(title=None):
    post = Post.query.filter_by(title = title).first()
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('dashboard',username=current_user.username))

# @app.route("/post/<int:post_id>")
# def post_display(post_id):
#     post = Post.query.get_or_404(post_id) # if post id exist,find the post, or 404
#     return render_template('post_display.html', title=post.title, post=post)

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    # multi line string, f string 1 {}
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        flash('You are already log in!','success')
        return redirect(url_for('dashboard', username = current_user.username))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.route("/chineseIndex")
def chineseIndex():
    return render_template("chineseIndex.html")

@app.route("/map")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 37.4300,
             'lng': -122.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ]
    )
    return render_template('example.html', mymap=mymap, sndmap=sndmap)


if __name__ == "__main__":
    app.run(debug=True)