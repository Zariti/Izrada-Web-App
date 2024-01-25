#!python.exe
import os
import cgi
from http import cookies



subjects = {
            'ip' : {'name':'Introduction to Programming', 'year':1},
            'c1' : {'name':'Calculus 1', 'year':1},
            'dmt': {'name':'Digital math', 'year':3},
            'sql': {'name':'Data Bases', 'year':2},
            'c2' : {'name':'Calculus 2', 'year':2},
            'cds': {'name':'Computer and Data security', 'year':3}
            }


def change_data(year):
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
            if check("not_selected", key):
                print('Not selected: <input type="radio" name="' + key + '" value="not_selected" checked>')
            else:
                print('Not selected: <input type="radio" name="' + key + '" value="not_selected">')
            if check("enrolled", key):
                print('Enrolled: <input type="radio" name="' + key + '" value="enrolled" checked>')
            else:
                print('Enrolled: <input type="radio" name="' + key + '" value="enrolled">')
            if check("passed", key):
                print('Passed: <input type="radio" name="' + key + '" value="passed" checked>')
            else:
                print('Passed: <input type="radio" name="' + key + '" value="passed">')
            print("""
            </td>
            </tr>
            """)

def check(value, key_subj):
    cookie_str = os.environ.get('HTTP_COOKIE', '')  #PAZIT OVDE DA NE STAVIS HTTP_COOKIE'S' bez ovoga S
    cookie_str_obj = cookies.SimpleCookie(cookie_str)
    for key in cookie_str_obj:
        if cookie_str_obj.get(key):
            if key == key_subj:
                status = cookie_str_obj.get(key).value
                if status == value:
                    return True
                else:
                    return False


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
year = decide_year(params.getvalue('year', '1st')) #1 ili 2 ili 3 (integers)

def print_form():
    print("""
    <form>
    <input type="submit" name="year" value="1st">
    <input type="submit" name="year" value="2nd">
    <input type="submit" name="year" value="3rd">
    <input type="submit" name="year" value="upisni_list">
    <table border="1">
    """)
    change_data(year)
    print("""
    </table>
    </form>
    """)

def html_start():
    print("""
    <!DOCTYPE html>
    <html>
    <head><title>Upisni list</title></head>
    <body>
    """)

def html_end():
    print("""
    </body>
    </html>
    """)

def set_cookies():
    cookie = cookies.SimpleCookie()
    for key in params:
        cookie[key] = params.getvalue(key)
    print(cookie)

set_cookies()
print()
html_start()
print_form()
html_end()