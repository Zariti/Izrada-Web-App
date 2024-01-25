#!python.exe

import os
import cgi
from http import cookies

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

def html_start():
    print("""
    <!DOCTYPE html>
    <html>
    <head><title>Ponavljanje opet -.-</title></head>
    <body>
    """)

def html_end():
    print("""
    </body>
    </html>
    """)

def decide_year(year):
    if year == '1st':
        return 1
    elif year == '2nd':
        return 2
    elif year == '3rd':
        return 3
    else:
        return 4

params = cgi.FieldStorage()

year = decide_year(params.getvalue('year', '1st'))

def set_cookies():
    cookie = cookies.SimpleCookie()
    for key in params:
        cookie[key] = params.getvalue(key)
    print(cookie)

def get_cookies(value, subjects_key):
    cookie_str = os.environ.get('HTTP_COOKIE', '')
    cookie_str_obj = cookies.SimpleCookie(cookie_str)
    for key in cookie_str_obj:
        if key:
            if key == subjects_key:
                if cookie_str_obj[key].value == value:
                    return True
                else:
                    return False
    return None

def print_form(year):
    print("""
    <form>
    <input type="submit" name="year" value="1st">
    <input type="submit" name="year" value="2nd">
    <input type="submit" name="year" value="3rd">
    <table border="1">
    """)
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
            if get_cookies('not_selected', key):
                print(f'Not selected: <input type="radio" name="{key}" value="not_selected" checked>')
            else:
                print(f'Not selected: <input type="radio" name="{key}" value="not_selected">')
            if get_cookies('enrolled', key):
                print(f'Enrolled: <input type="radio" name="{key}" value="enrolled" checked>')
            else:
                print(f'Enrolled: <input type="radio" name="{key}" value="enrolled">')
            if get_cookies('passed', key):
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

set_cookies()
print()
html_start()
print_form(year)
html_end()