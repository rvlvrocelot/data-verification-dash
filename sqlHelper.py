import pyodbc as po
import sqlalchemy as sa
import datetime
import dateutil.relativedelta
import numpy as np
import matplotlib.pyplot as plt
import calendar
import time
import collections


cnxn = po.connect('DRIVER={SQL Server Native Client 11.0};SERVER=SIW0085\SIMFUNDWEB;DATABASE=SimfundRelease;Trusted_Connection=yes')
cursor = cnxn.cursor()

def getResearchers():
    researcherList = {}
    cursor.execute("SELECT UserID userId, Name name FROM dbo.VerificationStaff")
    result = cursor.fetchall()
    for row in result:
        researcherList[row.userId] = row.name
    return researcherList

def getProducts():
	productList = {}
	cursor.execute("SELECT ProductId productId,ProductDescription productDescription FROM dbo.CheckProduct")
	result = cursor.fetchall()
	for row in result:
		productList[row.productId] = row.productDescription
	return productList

def getCategory():
	categoryList = {}
	cursor.execute("SELECT CheckCategoryID checkCategoryId,CheckCategoryName checkCategoryName FROM dbo.CheckCategory")
	result = cursor.fetchall()
	for row in result:
		categoryList[row.checkCategoryId] = row.checkCategoryName
	return categoryList	

def getCheck(category):
	checkDict = collections.OrderedDict()
	cursor.execute("SELECT CheckID checkID, CheckTypeID checkTypeID, CheckDescription checkDescription FROM dbo.AllChecks WHERE CheckCategoryID = %d ORDER BY CheckTypeID "%int(category))
	result = cursor.fetchall()
	for row in result:
		 checkDict[str(row.checkID)] = {"checkTypeID":row.checkTypeID, "checkDescription":row.checkDescription} 
	return checkDict

def getCheckType():
	checkTypeDict = {}
	cursor.execute("SELECT c.CheckTypeID checkTypeID, CheckTypeName checkTypeName, a.CheckID checks FROM CheckType c JOIN AllChecks a ON a.CheckTypeID = c.CheckTypeID")
	result = cursor.fetchall()
	for row in result:
		if row.checkTypeID not in checkTypeDict:
			checkTypeDict[row.checkTypeID] = { "name":row.checkTypeName, "checks":[row.checks] }
		else:
			checkTypeDict[row.checkTypeID]["checks"].append(row.checks)
	return checkTypeDict

def getStatusDict():
	statusDict = {}
	cursor.execute("SELECT StatusID statusID, StatusName statusName FROM dbo.CheckStatus")
	result = cursor.fetchall()
	for row in result:
		statusDict[row.statusID] = row.statusName
	return statusDict


