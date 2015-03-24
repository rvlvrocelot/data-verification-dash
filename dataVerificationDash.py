# all the imports
import sqlite3
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask_bootstrap import Bootstrap
import hashlib
import sqlHelper

# configuration
# the database is not in tmp on the deployed verson
DATABASE = 'C:\\Users\\hjiang\\My Documents\\Github\\data-verification-dash\\dataVerificationDash.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def runScript(scriptName):
    with closing(connect_db()) as db:
        with app.open_resource('scripts/' + scriptName, mode='r') as f:
            db.cursor().executescript(f.read()) 
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    researcherList = sqlHelper.getResearchers()
    productList = sqlHelper.getProducts()
    categoryList = sqlHelper.getCategory()
    return render_template("home.html", researcherList = researcherList, productList = productList, categoryList=categoryList)

@app.route('/generateform',  methods=['POST'])
def generateform():
    researcher =  request.form['researcher']
    product =  request.form['product']
    category =  request.form['category']

    checkDict = sqlHelper.getCheck(category)
    checkTypeDict = sqlHelper.getCheckType()
    statusDict = sqlHelper.getStatusDict()

    keyList =  [int(key) for key in checkDict.keys()]
    for checkType in checkTypeDict:
        checkTypeDict[checkType]["checks"] = list( set(checkTypeDict[checkType]["checks"]) & set(keyList))
    for checkType in checkTypeDict:
        for index, checks in enumerate(checkTypeDict[checkType]["checks"]):
            checkTypeDict[checkType]["checks"][index] = str(checks)
        print checkTypeDict[checkType]["checks"]


    return render_template("form.html", researcher=researcher, product=product,checkDict=checkDict,checkTypeDict =checkTypeDict, statusDict =statusDict )

@app.route('/form')
def form():
    return render_template("form.html")

@app.route('/submitForm')
def submitForm():
    #return render_template("test.html")
    pass

@app.route('/report')
def report():
    return render_template("report.html")

if __name__ == '__main__':
    app.run(host = '0.0.0.0')

