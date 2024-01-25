#!python.exe
import os
import cgi
from http import cookies
import db

def start_html():
    print("""
    <!DOCTYPE html>
    <html>
    <head><title>index1.py</title></head>
    <body>
    """)

def end_html():
    print("""
    </body>
    </html>
    """)



def destroy_session_table(session_id):    #unistava cijeli stupac u student tablici
    query = "DELETE FROM session WHERE session_id = (%s)"
    values = (session_id,)
    mydb = db.get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute(query, values)
    mydb.commit()

def get_session_id():
    http_cookies_str = os.environ.get('HTTP_COOKIE', '')
    get_all_cookies_object = cookies.SimpleCookie(http_cookies_str)
    session_id = get_all_cookies_object.get("session_id").value if get_all_cookies_object.get("session_id") else None
    return session_id

def destroy_session():
    session_id = get_session_id()
    destroy_session_id() #unistava cookie sesiju
    destroy_session_table(session_id) #unistava iz tablice sesiju

def destroy_session_id():
    cookies_object = cookies.SimpleCookie()
    cookies_object["session_id"] = ""
    cookies_object["session_id"]["expires"] = 'Thu, 01 Jan 1970 00:00:00 GMT'
    print (cookies_object.output()) #upisivanje cookie-a u header


destroy_session()
print ("Location:login.py")
print("")
start_html()
end_html()



