from flask import Blueprint,render_template,request,redirect,flash,url_for
from flask_login import login_user, login_required, logout_user, current_user
from website.models import User,Post
from website.users.forms import RegistrationForm,LoginForm
from website import bcrypt,db

users=Blueprint('users',__name__)


@users.route('/account/<string:username>')
def account(username):
    page = request.args.get('page',1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    image_file = url_for('static', filename='images/profile_pic/'+user.profile_pic)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=3)
    return render_template("account.html",user=current_user,img=image_file,page_user=user,posts = posts)

@users.route('/register',methods=['GET','POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password,sport=form.sport.data)
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=False)
        flash(f'Your account has been created!','success')
        return redirect(url_for('main.home'))
    errors = [{'field': key, 'messages': form.errors[key]} for key in form.errors.keys()] if form.errors else []
    
    return render_template("register.html",user=current_user,form=form,errors=errors)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            flash(f'Logged in!','success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful. Please Check email and Password",'error')
    
    errors = [{'field': key, 'messages': form.errors[key]} for key in form.errors.keys()] if form.errors else []
    return render_template("login.html",user=current_user,form=form,errors=errors)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Signed out",category='success')
    return redirect(url_for('main.login'))