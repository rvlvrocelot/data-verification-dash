# all the imports
import sqlite3
import json
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flask_bootstrap import Bootstrap
import hashlib
import sqlHelper
import datetime

# configuration
# the database is not in tmp on the deployed verson
DATABASE = 'C:\\Users\\amahan\\My Documents\\GitHub\\data-verification-dash\\dataVerificationDash.db'
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
    g.periodID = sqlHelper.getPeriodID()
    researcherList = sqlHelper.getResearchers()
    productList = sqlHelper.getProducts()
    categoryList = sqlHelper.getCategory()
    periodIDList = sqlHelper.getPeriodID()
    print periodIDList
    return render_template("home.html", productList = productList, categoryList=categoryList, periodIDList=periodIDList)

@app.route('/generateform',  methods=['POST'])
def generateform():
    g.periodID = sqlHelper.getPeriodID()
    #researcher =  request.form['researcher']
    researcher = "Andrew"
    product =  request.form['product']
    category =  request.form['category']
    periodID = request.form['periodID']

    checkDict = sqlHelper.getCheck(category)
    checkTypeDict = sqlHelper.getCheckType()
    statusDict = sqlHelper.getStatusDict()

    keyList =  [int(key) for key in checkDict.keys()]
    for checkType in checkTypeDict:
        checkTypeDict[checkType]["checks"] = list( set(checkTypeDict[checkType]["checks"]) & set(keyList))
    for checkType in checkTypeDict:
        for index, checks in enumerate(checkTypeDict[checkType]["checks"]):
            checkTypeDict[checkType]["checks"][index] = str(checks)
    return render_template("form.html", researcher=researcher, product=product,checkDict=checkDict,checkTypeDict =checkTypeDict, statusDict =statusDict, periodID=periodID, category=category )

@app.route('/form')
def form():
    g.periodID = sqlHelper.getPeriodID()
    return render_template("form.html")

@app.route('/submitForm', methods=['POST'])
def submitForm():
    g.periodID = sqlHelper.getPeriodID()
    submitList = []
    for key in request.form:
        if key[0] == 'n':
            number = key[1:]
            dataSource =  sqlHelper.getDataSource(number)
            checkTypeID = sqlHelper.getCheckTypeID(number)
            time = datetime.datetime.now()
            notes = str(request.form[key])
            notes = notes.replace("'","''")
            sqlHelper.submitData(number, time, request.form['researcher'], request.form['periodID'], dataSource, request.form['category'], checkTypeID, request.form['product'], request.form['c'+str(number)], notes )
           
    return redirect("report/" +request.form['periodID'] )


@app.route('/report/<periodID>')
def report(periodID):
    g.periodID = sqlHelper.getPeriodID()
    data = sqlHelper.getReportData(periodID)
    return render_template("report.html",data=data, periodID=periodID)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')

