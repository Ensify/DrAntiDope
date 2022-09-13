from flask import Blueprint, render_template, request, url_for
from flask_login import current_user
from website.models import User, Post
from website import db
from website.main.news_category import get_news
from sqlalchemy import func
import csv
import random
main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template("home.html", user=current_user)


'''
{'source': {'id': 'vice-news', 'name': 'Vice News'},
 'author': 'Lorenzo Franceschi-Bicchierai, Jason Koebler', 
 'title': 'European Cops Helped 1.5 Million People Decrypt Their Ransomwared Computers', 
 'description': 'The European Union law enforcement agency estimates it has helped around $1.5 million people by providing decryption tools for popular ransomware strains.', 
 'url': 'https://www.vice.com/en/article/y3pv9v/european-cops-helped-15-million-people-decrypt-their-ransomwared-computers',
 'urlToImage': 'https://video-images.vice.com/articles/62dede5c59f358009b60cb32/lede/1658773440206-europol.jpeg?image-resize-opts=Y3JvcD0xeHc6MC44NzA0eGg7MHh3LDAuMDE5NnhoJnJlc2l6ZT0xMjAwOiomcmVzaXplPTEyMDA6Kg', 
 'publishedAt': '2022-07-26T06:00:00Z', 
 'content': 'In the last six years, European cops estimate that they have helped around 1.5 million people and organizations decrypt files that were locked by hackers with ransomware, saving around $1.5 billion.\xa0… [+2464 chars]'
}
'''


@main.route('/news')
def news():
    articles = {}
    if current_user.is_authenticated:
        if current_user.sport:
            news = get_news(current_user.sport)
            articles=news['articles']

    return render_template("news.html", user=current_user, articles=articles)



@main.route('/tue')
def tue():
    return render_template("tue.html", user=current_user)


@main.route('/forum', methods=['GET', 'POST'])
def forum():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    topics = db.session.query(Post.topic, db.func.count(Post.topic)).group_by(
        Post.topic).order_by(db.func.count(Post.topic).desc()).all()
    topics = topics[:10]

    return render_template("forum.html", user=current_user, posts=posts, topics=topics, topic=0)


@main.route("/topic/<string:topic>")
def topic(topic):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(topic=topic).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    topics = db.session.query(Post.topic, db.func.count(Post.topic)).group_by(
        Post.topic).order_by(db.func.count(Post.topic).desc()).all()
    topics = topics[:10]
    return render_template("forum.html", user=current_user, posts=posts, topics=topics, topic=topic)


@main.route('/aware')
def aware():
    listq = ["You are the only one who can limit your greatness.", "Every champion was once a contender that refused to give up.", "Never stop trying. Never stop believing. Never give up. Your day will come", "Believe you can and you’re halfway there", "You have to be at your strongest when you’re feeling at your weakest", "We may encounter many defeats but we must not be defeated.", "It’s not whether you get knocked down. It’s whether you get back up", "Your talent is God’s gift to you. What you do with it is your gift back to God", "Strength does not come from physical capacity. It comes from an indomitable will.",
             "The only person you are destined to become is the person you decide to be.", "Look in the mirror. That’s your competition", "It never gets easier. You just get better", "Success trains. Failure complains", "The sweat. The time. The devotion. It pays off.", "The harder the battle. The sweeter the victory", "It’s not about perfect. It’s about effort", "If you believe it, the mind can achieve it", "Tough times don’t last. Tough people do", "Pain is temporary. Quitting lasts forever", "Focus on your goal. Don’t look in any direction but ahead", "Sports does not build character. They reveal it", "A winner never stops trying", "Champions keep playing until they get it right.", "I’ve never lost a game. I just ran out of time", "A champion is someone who gets up when he can’t.", "Winners never quit and quitters never win.", "Without self-discipline, success is impossible.", "Passion first and everything will fall into place. ", "Kill them with success and bury them with a smile.",
             "A champion needs a motivation above and beyond winning."]

    quote = random.sample(listq, 1)[0]
    return render_template("aware.html", user=current_user, quote=quote)


@main.route('/aware/consequences')
def conseq():
    with open('website/main/sanction.csv') as f:
        reader = csv.reader(f, delimiter=';')
        records = []
        for record in reader:
            records.append(record)
    return render_template("consequences.html", user=current_user, records=records[1:], head=records[0])
