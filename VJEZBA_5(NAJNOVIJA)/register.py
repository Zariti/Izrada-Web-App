#!python.exe

import os
import cgi
from http import cookies

import mysql.connector
import json

import os
import hashlib
import base64

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

def register():
    print("""
    <form method="POST">
    Ime: <input type="text" name="username" value="">
    E-mail: <input type="text" name="email" value="">
    Lozinka: <input type="password" name="passwd" value="">
    Ponovi lozinku: <input type="password" name="passwd2" value="">
    <input type="submit" value="Register">
    </form>
    """)

def create_user(username, email, password, password2):
    mydb = db.get_DB_connection() # prvo se provjerava jeli vec postoji neki korisnik sa istim username ili emailom
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM user WHERE username = %s OR email = %s', (username, email)) #ovde sam falio jer nisam prosijedio-
    result = mycursor.fetchone()                                                                 #parametre kao tuple. tria zagrade- 
    if result:                                                                                   #stavit
        return None #################### user vec postoji
    if password != password2: # provjerava se jesu li sifre iste
        return None
    query = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
    hashed_password = hash_password(password)
    values = (username, email, hashed_password)
    mydb = db.get_DB_connection()
    cursor = mydb.cursor()
    try:
        cursor.execute(query, values)
        mydb.commit()
    except:
        return None
    return cursor.lastrowid 


def register(username, email, password, password2):
    user_id = create_user(username, email, password, password2)
    if user_id:
        return True
    else:
        return False


def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    hash = salt + key 

    return hash

def verify_password (password, hash):
 
    salt = hash[:32]
    key = hash[32:]

    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'), 
        salt, 
        100000)
    return new_key == key 

########
params = cgi.FieldStorage()

if os.environ['REQUEST_METHOD'].upper() == 'POST':
    username = params.getvalue('username')
    email = params.getvalue('email')
    password = params.getvalue('passwd1') ## ovde sam uzima passwd parametar bez ove jedinice. password je uvik bio prazan zbg toga 
    password2 = params.getvalue('passwd2')
    success = register(username, email, password, password2)
    if success:
        print('Location:login.py')
    
    



def start_html():
    print("""
    <!DOCTYPE html>
    <html>
    <head><title>register.py</title></head>
    <body>
    """)

def end_html():
    print("""
    </body>
    </html>
    """)

def register_start():
    print("""
    <form method="POST">
    Ime: <input type="text" name="username" value="">
    E-mail: <input type="text" name="email" value="">
    Lozinka: <input type="password" name="passwd1" value="">
    Ponovi lozinku: <input type="password" name="passwd2" value="">
    <input type="submit" value="Register">
    </form>
    """)
    #print(os.environ['REQUEST_METHOD'])
    #print(params)


start_html()
register_start()
print('<a href="login.py">Login</a>')
end_html()
