from selenium import webdriver
import urllib2
from bs4 import BeautifulSoup
import MySQLdb
from pyquery import PyQuery    
import json
import os
import requests
from html_table_extractor.extractor import Extractor

# db = MySQLdb.connect("directcallconnect.com","admin_default","echomartini","admin_default" )
db = MySQLdb.connect("148.66.136.54","rutherford","rf112233","rythunestham" )

# db = MySQLdb.connect("localhost","krishna","echomartini","krishna" )


## Initialize and load the web page
url = "http://agrimarketing.telangana.gov.in/indexnew.jsp"
driver = webdriver.PhantomJS()
driver.get(url)

html2 = driver.page_source
# print html2

soup = BeautifulSoup(html2)
table = soup.find('table', {'height': '450'})
extractor = Extractor(table)
extractor.parse()
data = extractor.return_list()
# print data
query = ''
print "extracted"
 
for i in data:
    name = i[0]
    minp = i[1]
    maxp = i[2]
    query = query+"('"+str(name)+"','"+str(minp)+"','"+str(maxp)+"'),"
    query = query.replace('\n', '')
    if name=="Comm.":
        query = ''

# print query
sql = "INSERT INTO rates(name, min, max) VALUES "+query[:-1]
# Execute the SQL command
print sql
mycursor = db.cursor()
mycursor.execute(sql)
print "data inserted successfully"
# Commit your changes in the database
db.commit()

# disconnect from server
db.close()
