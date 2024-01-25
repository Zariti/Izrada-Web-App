#!python.exe
from http import cookies
import os

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

status_names = {
    'not' : 'Not selected',
    'enr' : 'Enrolled',
    'pass' : 'Passed',
}

year_names = {
        1 : '1st Year',
        2 : '2nd Year',
        3 : '3rd Year'
    }

year_ids = {
        '1st Year' : 1,
        '2nd Year' : 2,
        '3rd Year' : 3
}

def display_years():
    for key in year_ids:
        print('<a href=?year=' + key + '">' + key + '</a>')





def decide_year(year=None):   #ovde se izvlaci iz params vrijednost od 'year'
    cookies_string = os.environ.get('HTTP_COOKIE', '')  #trazi se cookie na browseru i upisuje se u obliku stringa        
    all_cookies_object = cookies.SimpleCookie(cookies_string)   #vrijdnost stringa se sprema u serverski cookie 
    if year is not None:  #ako se bira neka nova godina?
        cookie = cookies.SimpleCookie() #stvara se cookie varijabla na serveru
        cookie['year'] = year  #cookie-u dajemo ime 'year' i vrijednost koja se nalazi u params.getvalue('year')
        print(cookie.output())
    elif all_cookies_object.get('year'):  #pri drugom posjetu stranici?? tjst ako je cookie vec na kompu uzece ga
        year = all_cookies_object.get('year').value
    else:   #ako prvi put udemo u stranicu
        year = '1st Year'
    return year

def change_data(year, key): #make_translations()
    for key in subjects:
        #if (subjects.get(key).get('year') != year):
        #    continue
        #elif (subjects.get(key).get('year') == year):
        #    return subjects.get(key).get() 
        if (subjects.get(key).get('year') == year):
            pass
            
            

