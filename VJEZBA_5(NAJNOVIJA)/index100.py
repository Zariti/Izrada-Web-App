#!python.exe

import os
import cgi
from http import cookies

import mysql.connector
import json

import db
#import login
#import register - ovo crasha skriptu 



params = cgi.FieldStorage()




# DOBAVLJANJE session_id-a
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

session_id = get_or_create_session_id()

# PUNJENJE TABLICE SA PARAMETRIMA
mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='maroancic')
mycursor = mydb.cursor()
mycursor.execute('SELECT * FROM session WHERE session_id=' + str(session_id))
result = mycursor.fetchone()
data_json = result[1]
data_dict = json.loads(data_json)
for key in params:
    data_dict[key] = params.getvalue(key)

data_json_upd = json.dumps(data_dict)

mycursor.execute('REPLACE INTO session(session_id, data) VALUES (%s,%s)', (session_id, data_json_upd))
mydb.commit() #OVDE SAN FALIO ZADNJI PUT JER NISAM COMMITA CHANGES NA TABLICU

###################################

# DOBAVLJANJE VRIJEDNOSTII IZ TABLICE I USPOREDIVANJE PODACIMA
mycursor.execute('SELECT * FROM session WHERE session_id=' + str(session_id))
result = mycursor.fetchone()
data_json = result[1]
data_dict = json.loads(data_json)

############################








def decide_year(value):
    if value == '1st':
        return 1
    elif value == '2nd':
        return 2
    elif value == '3rd':
        return 3
    else:
        return 4

year = decide_year(params.getvalue('year', '1st'))


subjects = {        

    'ip' : { 'name' : 'Introduction to programming' , 'year' : 1, 'ects' : 6 },

    'c1' : { 'name' : 'Calculus 1' , 'year' : 1, 'ects' : 7 },
    'cu' : { 'name' : 'Computer usage' , 'year' : 1, 'ects' : 5 },
    'dmt' : { 'name' : 'Digital and microprocessor technology', 'year' : 1, 'ects' : 6 },
    'db' : { 'name' : 'Databases' , 'year' : 2, 'ects' : 6 },
    'c2' : { 'name' : 'Calculus 2' , 'year' : 2, 'ects' : 7 },
    'dsa' : { 'name' : 'Data structures and alghoritms' , 'year' : 2, 'ects' : 5 },
    'ca' : { 'name' : 'Computer architecture', 'year' : 2, 'ects' : 6 },
    'isd' : { 'name' : 'Information systems design' , 'year' : 3, 'ects' : 5 },
    'c3' : { 'name' : 'Calculus 3' , 'year' : 3, 'ects' : 7 },
    'sa' : { 'name' : 'Server Architecture' , 'year' : 3, 'ects' : 6 },
    'cds' : { 'name' : 'Computer and data security', 'year' : 3, 'ects' : 6 }
    }

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

def broj_bodova():
    br_bodova = 0
    for key in subjects:
        if check_data("enrolled", key):
            br_bodova += int(subjects.get(key).get('ects'))
    return br_bodova


def print_form(year): 

    print("""
    <form>
    <input type="submit" name="year" value="1st">
    <input type="submit" name="year" value="2nd">
    <input type="submit" name="year" value="3rd">
    <input type="submit" name="year" value="upisni">
    <table border="1">
    """)

    if year == 4:
        for key in subjects:
            print("""
            <tr>
            <td>
            """)
            print(subjects.get(key).get('name'))
            print("""
            </td>
            <td>
            """)

            if check_data("not_selected", key):
                print('Ne upisuje')

            elif check_data("enrolled", key):
                print('Upisuje')

            else:
                print('Polozen')

            print("""
            </td>
            <td>
            """)
            print(subjects.get(key).get('ects'))
            print("""
            </td>
            </tr>
            """)
        print("""
        <tr>
        <td>
        </td>
        <td>
        Ukupno:
        </td>
        <td>
        """)
        print(broj_bodova())
        print("""
        </td>
        </tr>
        """)

    else:
        for key in subjects:
            if subjects.get(key).get('year') == year:
                print("""
                <tr>
                <td>
                """)
                print(subjects.get(key).get('name'))
                print("""
                </td>
                <td>
                """)
                if check_data("not_selected", key):
                    print(f'Not selected: <input type="radio" name="{key}" value="not_selected" checked>')
                else:
                    print(f'Not selected: <input type="radio" name="{key}" value="not_selected">')
                if check_data("enrolled", key):
                    print(f'Enrolled: <input type="radio" name="{key}" value="enrolled" checked>')
                else:
                    print(f'Enrolled: <input type="radio" name="{key}" value="enrolled">')
                if check_data('passed', key):
                    print(f'Passed: <input type="radio" name="{key}" value="passed" checked>')
                else:
                    print(f'Passed: <input type="radio" name="{key}" value="passed">')
                
                print("""
                </td>
                </tr>
                """)
    print("""
    </table>
    </form>
    """)










#replacing  --> json.dumps() koristimo kad saljemo podatke iz pythona u bazu podataka kako bi baza razumila te podatke
#           --> json.loads() koristimo kad dobavljamo podatke iz baze te ih prevodimo u python kod pomocu json.loads

#updatanje baze

def get_session_id():
    http_cookies_str = os.environ.get('HTTP_COOKIE', '')
    get_all_cookies_object = cookies.SimpleCookie(http_cookies_str)
    session_id = get_all_cookies_object.get("session_id").value if get_all_cookies_object.get("session_id") else None
    return session_id

def check_data(value_radio, subj_key):
    for key, value in data_dict.items():
        if key:
            if key == subj_key:
                if value == value_radio:
                    return True
                else:
                    return False
        else:
            return False


    

session_id = get_session_id()
mydb = db.get_DB_connection()#spajanje sa bazom
mycursor = mydb.cursor()
mycursor.execute('SELECT * FROM session WHERE session_id=' + str(session_id)) #dohvaca redak iz tablice student/sessions
result = mycursor.fetchone()
#print(result[1])
data = json.loads(result[1]) #pretvaramo u dict
user_name_id = data["user_id"]
#print(user_name_id)
mycursor.execute('SELECT * FROM user WHERE user_id=' + str(user_name_id))
result = mycursor.fetchone()
#user_name_name = json.loads(result[1])
#print(result[1])
user_id = result[1] #ovo cemo spremit u cookie u slucaju promjene lozinke
cookie = cookies.SimpleCookie()
cookie['user_id'] = user_id
print(cookie)

start_html()
print(f'Pozdrav {result[1]}')
print('<a href="logout.py">Log-out</a>')
print('<a href="change_password.py">Change password</a>')
print_form(year)
end_html()

#dobavit vrijednost cookie-a 
#otic u bazu student(sessions) i dobavit data di je user_id jednak vrijednosti cookie-a
#i sad iz data dobavit vrijednost key-a 'user-id'
#usporedivat priko query-a di je 'user_id' value jednak user_id-ju iz tab users