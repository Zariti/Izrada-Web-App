import os
import cgi
from http import cookies
import mysql.connector

mydb = mysql.connector.connect(host="localhost", database = "testing", user="root", password="")

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS sessions (session_id INT AUTO_INCREMENT PRIMARY KEY, data TEXT)")

params = cgi.FieldStorage()
session_id = os.environ.get("HTTP_COOKIE", '')

if session_id:
    mycursor = mydb.cursor()
    mycursor.execute("SELECT data FROM sessions WHERE session_id = %s", (session_id))
    result = mycursor.fetchone()




