from crypt import methods
from flask import Blueprint,render_template,request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


auth = Blueprint('auth',__name__)

@auth.route('/signin',methods =['GET','POST'])
def signin():
    data = request.form
    print(data)

    return render_template("signin.html",boolean = True)

@auth.route('/register',methods =['GET','POST'])
def register():  
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')


        if len(email) < 4:
            flash("The email you entered is invalid.",category ='error')
        elif len(password) < 4:
            flash("Your password should have atleast 5 characters.",category = 'error')
        elif password != confirm:
            flash("Passwords don't match. Try Again.")
        else:
            new_user = User(email = email, password =generate_password_hash(password , method = 'sha256') )
                                           #hasing algorithm

            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!',category = "success")   
            return redirect(url_for('views.home'))
    return   render_template("register.html",boolean = True)

@auth.route('/logout')
def logout():
    return "<p>Logged out successfully..</p>"
        





