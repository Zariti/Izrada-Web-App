#!python.exe                

import os                   #kao prvo importat sve (osnovno)
import cgi
from http import cookies
import db
import mysql.connector
import session
import json

#stvara se tablica u sesiji za pohranu podataka
#mydb = mysql.connector.connect(host="localhost", database="session", user="root", passwd="")
#mycursor = mydb.cursor()
#mycursor.execute("CREATE TABLE IF NOT EXISTS studenti (session_id INT AUTO_INCREMENT PRIMARY KEY, data TEXT)")
########

def add_to_session(params):  #izmijenjena 
    #session_id = session.get_or_create_session_id()     ->ne triba ovde
    _, data = db.get_session(session_id)  #data je ovde vec dobro formatiran 
    for key in params.keys():
        data[key] = params.getvalue(key)
    db.replace_session(session_id, data)


params = cgi.FieldStorage()  #pa onda ove paramse (osnovno)
session_id = session.get_or_create_session_id() #ovde se connecta na bazu i daje vrijednost session_id-ju
add_to_session(params)  #dodaju se parametri u session (bazu)

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="ducan")
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM ducan WHERE session_id=" + str(session_id))
myresult = mycursor.fetchone()

data_str = myresult[1]  #[1] - prvi stupac --> [0][1][2]...  data_str je string i po njemu ne mozemo iterirat

my_dict = json.loads(data_str) #formatira ih da bude dict objekt (moze se iterirat)


#json_data = json.dumps(data_str)


def html_start():       #1 korak (setup)
    print("""
    <!DOCTYPE html>
    <html>
    <head><title>index8</title></head>
    <body>
    """)

def html_end():         #2 korak (setup)
    print("""
    """)
    #print(data_str)
    print(my_dict)
    print("""
    </body>
    </html>
    """)

subjects = {        #3 korak (setup)

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


def set_cookie():                      #4 korak (setup)
    cookie = cookies.SimpleCookie()
    for key in params:
        cookie[key] = params.getvalue(key)
    print(cookie)

def decide_year(year_str):              #za odredit godinu iz stringa + stavlja u cookie
    cookie = cookies.SimpleCookie()
    if year_str == '1st':
        return 1
    elif year_str == '2nd':
        return 2
    elif year_str == '3rd':
        return 3
    else:   #u ovom sluc upisni list
        return 4
    
year = decide_year(params.getvalue('year', '1st')) #year = 1 li 2 il 3 il 4  || Drugi parametar je default value ako nema 'year'




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

            if check2("not_selected", key):
                print('Ne upisuje')

            elif check2("enrolled", key):
                print('Upisuje')

            else:
                print('Polozen')

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
                if check2("not_selected", key):
                    print(f'Not selected: <input type="radio" name="{key}" value="not_selected" checked>')
                else:
                    print(f'Not selected: <input type="radio" name="{key}" value="not_selected">')
                if check2("enrolled", key):
                    print(f'Enrolled: <input type="radio" name="{key}" value="enrolled" checked>')
                else:
                    print(f'Enrolled: <input type="radio" name="{key}" value="enrolled">')
                if check2('passed', key):
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

def check2(radio_value, subj_key):
    #cookie_str = os.environ.get('HTTP_COOKIE', '')    
    #cookie_str_obj = cookies.SimpleCookie(cookie_str) 
    #if json_data == '': #ovde sam popravio problem sa prikazivanjem tablice
    #    return False  
    
    #if value == params.getvalue('year'):  #prva provjera 
    #    for key in params:
    #        if key:
    #            if key == subj_key:
    #                if params.getvalue(key) == radio_value:
    #                    return True
    #                else:
    #                    return False

    for key, value in my_dict.items():                      
        if key:   
            if key == subj_key:
                if value == radio_value:
                    return True
                else:
                    return False
        else:
            return False



def check(radio_value, subj_key): #ova funkcija cita iz cookie-a
    cookie_str = os.environ.get('HTTP_COOKIE', '')    #spranca
    cookie_str_obj = cookies.SimpleCookie(cookie_str) #spranca
    if cookie_str == '': #ovde sam popravio problem sa prikazivanjem tablice
        return False  
    
    if cookie_str_obj['year'].value == params.getvalue('year'):  #prva provjera 
        for key in params:
            if key:
                if key == subj_key:
                    if params.getvalue(key) == radio_value:
                        return True
                    else:
                        return False

    for key in cookie_str_obj:                        #spranca
        if key:    #jel uopce cookie postoji          #spranca
            if key == subj_key:
                if cookie_str_obj[key].value == radio_value:
                    return True
                else:
                    return False
        else:
            return False



#set_cookie()
#print()
html_start()
print_form(year)
html_end()



    