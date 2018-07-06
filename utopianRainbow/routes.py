from flask import  render_template, url_for, flash, redirect, request, abort
from utopianRainbow import app, db, bcrypt
from utopianRainbow.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from utopianRainbow.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

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

@app.route("/ngo/")
@app.route("/ngo/<username>")
def ngo(username=None):
    # form = LoginForm()
    # if username != None:
    # posts = Post.query.all()
    return render_template('ngo.html', username=username)
    # else:
        # return render_template("ngo.html")
        
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

@app.route("/post/<username>/display/<title>")
@login_required
def post_display(username, title):
    thisPost = Post.query.filter_by(title = title).first()
    return render_template('post_display.html', post=thisPost, username=current_user.username)

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
    print(thisPost.author, current_user)
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

    
@app.route("/chineseIndex")
def chineseIndex():
    return render_template("chineseIndex.html")


if __name__ == "__main__":
    app.run(debug=True)