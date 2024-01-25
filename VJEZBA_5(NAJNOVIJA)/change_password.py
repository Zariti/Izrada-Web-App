#!python.exe

import os
import cgi
#import mysql.connector
from http import cookies
import base
import db
import password_utils

def change_password(password_old, password1, password2):
    mydb = db.get_DB_connection()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM user WHERE user_id=%s', (user_id,))
    result = mycursor.fetchone()
    stored_password = result[3]
    success = password_utils.verify_password(password_old, stored_password)
    if success:
        if password1 == password2:
            password_new_hashed = password_utils.hash_password(password1)
            mycursor.execute('REPLACE INTO user (password) VALUES (%s)', (password_new_hashed,))
            mydb.commit()
            base.start_html()
            print("""
            Lozinka uspijesno promijenjena!
            <form method="POST">
            Stara lozinka: <input type="password" name="pswd_old">
            Nova lozinka: <input type="password" name="pswd1">
            Ponovi novu lozinku: <input type="password" name="pswd2">
            <input type="submit" value="Change password">
            </form>
            """)
            base.finish_html()
            exit()
        else:
            base.start_html()
            print("""
            Nove lozinke se ne podudaraju!
            <form method="POST">
            Stara lozinka: <input type="password" name="pswd_old">
            Nova lozinka: <input type="password" name="pswd1">
            Ponovi novu lozinku: <input type="password" name="pswd2">
            <input type="submit" value="Change password">
            </form>
            """)
            base.finish_html()
            exit()
    else:
        base.start_html()
        print("""
        Stara lozinka je pogresna!
        <form method="POST">
        Stara lozinka: <input type="password" name="pswd_old">
        Nova lozinka: <input type="password" name="pswd1">
        Ponovi novu lozinku: <input type="password" name="pswd2">
        <input type="submit" value="Change password">
        </form>
        """)
        base.finish_html()
        exit()

cookie_str = os.environ.get('HTTP_COOKIE', '')
cookie_str_obj = cookies.SimpleCookie(cookie_str)

if 'user_id' in cookie_str_obj:
    user_id = cookie_str_obj['user_id'].value


params = cgi.FieldStorage()

if os.environ['REQUEST_METHOD'].upper() == 'POST':
    password_old = params.getvalue('pswd_old')
    password1 = params.getvalue('pswd1')
    password2 = params.getvalue('pswd2')
    change_password(password_old, password1, password2)



base.start_html()
print("""
<form method="POST">
Stara lozinka: <input type="password" name="pswd_old">
Nova lozinka: <input type="password" name="pswd1">
Ponovi novu lozinku: <input type="password" name="pswd2">
<input type="submit" value="Change password">
</form>
""")
base.finish_html()
