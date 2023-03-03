from flask import Blueprint,render_template,request
from flask_login import current_user
from website.models import Post
from website import db
from sqlalchemy import func
main=Blueprint('main',__name__)



@main.route('/')
def home():
    return render_template("home.html",user=current_user)


@main.route('/news')
def news():
    return render_template("news.html",user=current_user)


@main.route('/drugs')
def drugs():
    return render_template("drugs.html",user=current_user)


@main.route('/tue')
def tue():
    return render_template("tue.html",user=current_user)


@main.route('/forum',methods=['GET','POST'])
def forum():
    page= request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    topics = db.session.query(Post.topic, db.func.count(Post.topic)).group_by(Post.topic).order_by(db.func.count(Post.topic).desc()).all()
    topics=topics[:10]

    return render_template("forum.html",user=current_user,posts=posts,topics=topics,topic=0)

@main.route("/topic/<string:topic>")
def topic(topic):
    page= request.args.get('page',1,type=int)
    posts = Post.query.filter_by(topic=topic).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    topics = db.session.query(Post.topic, db.func.count(Post.topic)).group_by(Post.topic).order_by(db.func.count(Post.topic).desc()).all()
    topics=topics[:10]
    return render_template("forum.html",user=current_user,posts=posts,topics=topics,topic=topic)

@main.route('/aware')
def aware():
    return render_template("aware.html",user=current_user)