import os                   #kao prvo importat sve (osnovno)
import cgi
from http import cookies
import db
import mysql.connector

#stvara se tablica u sesiji za pohranu podataka
mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="ducan")
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM ducan")

for i in mycursor:
    print(i)