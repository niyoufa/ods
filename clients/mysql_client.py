#coding=utf-8

import MySQLdb

# test MySQLdb
db = mysql_client.connect("localhost","root","dhui123","demosite")
cr = db.cursor()
cr.execute("select * from demosite_links")
data = cr.fetchone()
print data
db.close()