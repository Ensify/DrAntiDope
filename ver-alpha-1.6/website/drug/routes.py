from flask import Blueprint, render_template, request,session, url_for,redirect, Flask
from flask_login import current_user
from website.models import User, Post
from website.drug.forms import DrugSearchForm
from website import db
from sqlalchemy import func
from website import tabl

from pymongo import MongoClient  
import numpy as np

drug = Blueprint('drug', __name__)

# from flask import Flask, request, render_template,session, redirect, url_for
# from pymongo import MongoClient  
# import numpy as np

# app = Flask(__name__)

# app.secret_key = "azureimmortals"


client = MongoClient("mongodb+srv://SarumathyPrabakaran:sarumathy@cluster0.lbdvmf4.mongodb.net/?retryWrites=true&w=majority") #host uri    
db = client['Dr-Dope']   
tabl = db['drug']
nested=tabl.distinct('conditions')
cond = [x for sublist in nested for x in sublist]

@drug.route("/drugs", methods=["POST", "GET"])
def home():
	session['search_name']=''
	if request.method == "GET":	
		return render_template("search.html", drugs=tabl.distinct('drug'),brand=tabl.distinct('brand_list'),condition=cond)

@drug.route("/search",methods=["POST","GET"])
def searchresult():
    print(request.form['search-list'])
    if(request.form['search-list'])== 'brand':
        brand1 = request.form["search"]
        print("hello*********")
        return redirect(url_for('drug.drugSearchResult',drug=brand1,name='brand_list'))

    if((request.form['search-list'])== 'condition'):
        condition = request.form["search"]
        return redirect(url_for('drug.drugSearchResult',drug=condition,name='conditions'))

    if (request.form['search-list']) == 'drug-name':
        drug_name = request.form["search"]
        return redirect(url_for('drug.drugSearchResult',drug=drug_name,name='drug'))


# @app.route("/<drug>/<name>",methods=["GET","POST"])
# def drugSearchResult(drug,name):
#     drug=drug
#     name=name
#     arr=[]
#     if(name=="conditions"):
#         for i in tabl.distinct('conditions'):
#             if drug in i:
#                 dic = tabl.find_one({name:i})

#     else:
#         dic = tabl.find_one({name:drug})
#     print(dic)
#     return render_template('drugs.html',drug = dic)



@drug.route("/<drug>/<name>",methods=["GET","POST"])
def drugSearchResult(drug,name):
    drug=drug
    name=name
    arr=[]
    if(name=="conditions"):
        for i in tabl.distinct('conditions'):
            if drug in i:
                dics = tabl.find({name: i})
                for dic in dics:
                    print(dic)

    else:
                dics = tabl.find({name: drug },{'_id':0})
    for dic in dics:
        print(dic)
    return render_template('drugs.html',user = current_user,drug = dic)







# @app.route("/search",methods=["POST","GET"])
# def searchresult():
# 	drug_name = request.form["search"]
# 	return redirect(url_for('drugSearchResult',drug=drug_name))








if __name__ == '__main__':
	app.run(debug=True,port=5004)


# @drug.route("/<drug>/<name>",methods=["GET","POST"])
# def drugSearchResult(drug,name):
#     drug=drug
#     name=name
#     arr=[]
#     if(name=="conditions"):
#         for i in tabl.distinct('conditions'):
#             if drug in i:
#                 dics = tabl.find({name: i})
#                 for dic in dics:
#                     print(dic)

#     else:
#                 dics = tabl.find({name: drug },{'_id':0})
#     for dic in dics:
#         print(dic)
#     return render_template('drug.html',drug = dic)



