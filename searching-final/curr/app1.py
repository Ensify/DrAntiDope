from flask import Flask, request, render_template,session, redirect, url_for
from pymongo import MongoClient  
import numpy as np

app = Flask(__name__)

app.secret_key = "azureimmortals"


client = MongoClient("mongodb+srv://SarumathyPrabakaran:sarumathy@cluster0.lbdvmf4.mongodb.net/?retryWrites=true&w=majority") #host uri    
db = client['Dr-Dope']   
tabl = db['drug']
nested=tabl.distinct('conditions')
cond = [x for sublist in nested for x in sublist]

@app.route("/", methods=["POST", "GET"])
def home():
	session['search_name']=''
	if request.method == "GET":	
		return render_template("index.html", drugs=tabl.distinct('drug'),brand=tabl.distinct('brand_list'),condition=cond)

@app.route("/search",methods=["POST","GET"])
def searchresult():
    print(request.form['search-list'])
    if(request.form['search-list'])== 'brand':
        brand1 = request.form["search"]
        print("hello*********************")
        return redirect(url_for('drugSearchResult',drug=brand1,name='brand_list'))

    if((request.form['search-list'])== 'condition'):
        condition = request.form["search"]
        return redirect(url_for('drugSearchResult',drug=condition,name='conditions'))

    if (request.form['search-list']) == 'drug-name':
        drug_name = request.form["search"]
        return redirect(url_for('drugSearchResult',drug=drug_name,name='drug'))


@app.route("/<drug>/<name>",methods=["GET","POST"])
def drugSearchResult(drug,name):
    drug=drug
    name=name
    arr=[]
    if(name=="conditions"):
        for i in tabl.distinct('conditions'):
            if drug in i:
                dic = tabl.find_one({name:i})

    else:
        dic = tabl.find_one({name:drug})
    print(dic)
    return render_template('drug.html',drug = dic)







# @app.route("/search",methods=["POST","GET"])
# def searchresult():
# 	drug_name = request.form["search"]
# 	return redirect(url_for('drugSearchResult',drug=drug_name))








if __name__ == '__main__':
	app.run(debug=True)