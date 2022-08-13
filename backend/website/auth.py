from flask import Blueprint

auth = Blueprint('auth',__name__)

@auth.route('news')
def news_page():
    return "<p>NEWS</p>"




