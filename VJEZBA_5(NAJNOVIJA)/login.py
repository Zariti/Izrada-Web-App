#!python.exe

import os
import cgi

import hashlib
import db

import json

from http import cookies
import mysql.connector

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



def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    hash = salt + key 

    return hash

def verify_password(password, hash): #hash je hashiran passwd iz baze  (PROVJERENA)
 
    salt = hash[:32]  #prvih 32 char (0-32)
    key = hash[32:]   #od 32 nadalje (32-...)

    new_key = hashlib.pbkdf2_hmac(  #hashira se unesena lozinka
        'sha256',
        password.encode('utf-8'), 
        salt, 
        100000)
    return new_key == key.encode('utf-8')       #usporeduju se hashirana lozinka iz unosa i hashirana lozinka iz baze(vrati true ako su iste)

def verify_password2(password_plain_text, stored_password_hash):  #ako sifre koriste isti salt onda ce dobit isti hash na kraju!!!!
    salt = stored_password_hash[:32]
    key = stored_password_hash[32:]
    new_hash = hashlib.pbkdf2_hmac('sha256', password_plain_text.encode('utf-8'), salt, 100000)
    return (key == new_hash)

#def verify_password2(password, hash):
#    salt = hash[:32]  # Extract the salt from the hashed password
#    key = hash[32:]   # Extract the key from the hashed password
#
#    # Hash the plain-text password using the same salt and number of iterations
#    new_key = hashlib.pbkdf2_hmac(
#        'sha256',
#        password.encode('utf-8'),
#        salt.encode('utf-8'),  # Ensure the salt is a bytes-like object
#        100000
#    )
#
#    # Compare the hashed plain-text password with the stored hashed password
#    return new_key == key.encode('utf-8')  # Ensure the key is a bytes-like object

def get_user_by_username(username):  # (provjerena)
    mydb = db.get_DB_connection()
    cursor = mydb.cursor()
    query = "SELECT * FROM user where username='" + username + "'"
    cursor.execute(query)
    myresult = cursor.fetchone()
    return myresult          #funkc. koja vraca redak odg usera iz baze

def login(username, password):  # (PROVJERENA)
    user = get_user_by_username(username) #trazi po bazi usera sa istim username-om, vraca cili redak  (PROVJERENA)
    if user and verify_password2(password, user[3]): #ako postoji user(neki broj) i ako su password i user[2](passw iz baze) jednaki vrati true
        return True, user[0]
    return False, None

def create_session():     #ispod je zamjena (2)
    mydb = db.get_DB_connection() 
    cursor = mydb.cursor()
    query = "INSERT INTO session (data) VALUES (%s)"
    values = (json.dumps({}),)
    cursor.execute(query, values)  #stvara novi redak u tablici student(sesije) i stavlja prazan data '{}'
    mydb.commit()  #save changes
    return cursor.lastrowid  #vrati id od sesija (broj redka)

def create_session_new():
    session_id = db.create_session() #ovde je bila greska unutar funkcije, gledala je sessions umisto student tab
    cookies_object = cookies.SimpleCookie()
    cookies_object["session_id"] = session_id
    print (cookies_object.output()) #upisivanje cookie-a u header
    return session_id


def get_or_create_session_id():  #samo kreira cookie session_id ili dobavlja njegovu vrijednost
    cookie_str = os.environ.get('HTTP_COOKIE', '')
    cookie_str_obj = cookies.SimpleCookie(cookie_str)
    for key in cookie_str_obj:
        if key == 'session_id':
            session_id = cookie_str_obj[key].value
            return session_id
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='maroancic')
    mycursor = mydb.cursor()
    values = (json.dumps({}),) #default value prilikom stvaranja sessiona
    mycursor.execute('INSERT INTO session (data) VALUES (%s)', values)
    mydb.commit()
    session_id = mycursor.lastrowid
    cookie_session = cookies.SimpleCookie()
    cookie_session['session_id'] = session_id
    print(cookie_session)
    return session_id

def get_session_id():
    http_cookies_str = os.environ.get('HTTP_COOKIE', '')
    get_all_cookies_object = cookies.SimpleCookie(http_cookies_str)
    session_id = get_all_cookies_object.get("session_id").value if get_all_cookies_object.get("session_id") else None
    return session_id

def get_session(session_id):
    mydb = db.get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM session WHERE session_id=" + str(session_id)) #trazi redak sa odg session_id
    myresult = cursor.fetchone()
    return myresult[0], json.loads(myresult[1]) #vrati id i formatiran data

def add_to_session(user_id, session_id=None): # npr user_id = 'user_id'=1 i npr. session_id = 4
    if session_id is None:
        session_id = get_session_id() #dohvaca session_id iz cookiea  (PROVJEREN)
    _, data = get_session(session_id)#vracanje do sada odabranih podataka (PROVJEREN)
    for key, value in user_id.items():
        data[key] = value  #ubacuje u stupac data npr. 'user_id':1
    db.replace_session(session_id, data)    #u stupac di je session_id odgovarajuc ubacuje data kojeg prije svega formatira za bazu


###########################
params = cgi.FieldStorage()

if os.environ['REQUEST_METHOD'].upper() == 'POST':
    username = params.getvalue('username')
    password = params.getvalue('passwd')
    success, user_id = login(username, password) #ako je success=true i user_id neki broj (ako vec postoji taj korisnik u bazi) (provjereno)
    if success:
        session_id = create_session_new() #stvara se session(stvara novi redak u tablici student)   (PROVJERENO)
        add_to_session({"user_id":user_id}, session_id) #dodaje npr 'user_id':1 u odg redak di je session_id 
        print('Location:index100.py')
        
    





start_html()
print("""
<form method="POST">
Username: <input type="text" name="username" value="">
Lozinka: <input type="password" name="passwd" value="">
<input type="submit" value="Login">
</form>
""")
print('<a href="register.py">Registriraj se!</a>')
#print(params)
#print(os.environ['REQUEST_METHOD'])
end_html()