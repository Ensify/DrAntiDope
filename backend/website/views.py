from flask import Blueprint,render_template

views =  Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/forum')
def forum():
    return render_template("forum.html")




@views.route('/news')
def news():
    return render_template("news.html")


@views.route('/drug')
def find_drug():
    #return render_template("drug.html")
    return "Hello   THis is drug page...."


@views.route('/expertsupport')
def expert_support():
    # return render_template("expertsupport.html")
    return "THis is export support page....thankyou..visit again"


@views.route('/tue')
def tue():
    #return render_template("tue.html")
    return "</h1 style = 'color : blue; text-align: center;' >AZURE IMMORTALS</h1>"














