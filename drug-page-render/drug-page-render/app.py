from flask import Flask, request, render_template,session, redirect, url_for
from pymongo import MongoClient  

app = Flask(__name__)

app.secret_key = "azureimmortals"


client = MongoClient("mongodb+srv://SarumathyPrabakaran:sarumathy@cluster0.lbdvmf4.mongodb.net/?retryWrites=true&w=majority") #host uri    
db = client['Dr-Dope']   
tabl = db['drug']
#print(tabl.distinct('drug'))

@app.route("/", methods=["POST", "GET"])
def home():
	session['search_name']=''
	if request.method == "GET":	
		return render_template("index.html", drugs=tabl.distinct('drug'))

@app.route("/search",methods=["POST","GET"])
def searchresult():
	drug_name = request.form["search"]
	return redirect(url_for('drugSearchResult',drug=drug_name))

@app.route("/<drug>",methods=["GET","POST"])
def drugSearchResult(drug):
	drug1 = drug
	dic = tabl.find_one({"drug":drug})
	print(dic)
	return render_template('drug.html',drug = dic)

if __name__ == '__main__':
	app.run(debug=True)
