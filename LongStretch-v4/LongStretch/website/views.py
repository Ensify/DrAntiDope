from turtle import title
from venv import create
from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for, abort
from .models import User,Post
from .forms import RegistrationForm,LoginForm,PostForm
from . import db,bcrypt
from flask_login import login_user, login_required, logout_user, current_user

views=Blueprint('views',__name__)


@views.route('/')
def home():
    return render_template("home.html",user=current_user)


@views.route('/news')
def news():
    return render_template("news.html",user=current_user)


@views.route('/drugs')
def drugs():
    return render_template("drugs.html",user=current_user)


@views.route('/tue')
def tue():
    return render_template("tue.html",user=current_user)


@views.route('/forum',methods=['GET','POST'])
def forum():
    page= request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template("forum.html",user=current_user,posts=posts)

@views.route('/aware')
def aware():
    return render_template("aware.html",user=current_user)

@views.route('/account/<string:username>')
def account(username):
    page = request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename='images/profile_pic/'+user.profile_pic)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template("account.html",user=current_user,img=image_file,page_user=user,posts = posts)

@views.route('/register',methods=['GET','POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password,sport=form.sport.data)
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=False)
        flash(f'Your account has been created!','success')
        return redirect(url_for('views.home'))
    errors = [{'field': key, 'messages': form.errors[key]} for key in form.errors.keys()] if form.errors else []
    
    return render_template("register.html",user=current_user,form=form,errors=errors)


@views.route('/login', methods=['GET', 'POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            flash(f'Logged in!','success')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash("Login Unsuccessful. Please Check email and Password",'error')
    
    errors = [{'field': key, 'messages': form.errors[key]} for key in form.errors.keys()] if form.errors else []
    return render_template("login.html",user=current_user,form=form,errors=errors)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Signed out",category='success')
    return redirect(url_for('views.login'))

@views.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post= Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('views.forum'))
    return render_template("create_post.html",user=current_user,form=form,legend ="New Post")

@views.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',post=post,user=current_user)

@views.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Updated!","success")
        return redirect(url_for('views.post', post_id=post.id))
    elif request.method =='GET':
        form.title.data= post.title
        form.content.data = post.content
    return render_template("create_post.html",user=current_user,form=form,legend="Update post")

@views.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('views.forum'))