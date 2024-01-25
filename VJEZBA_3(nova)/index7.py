#!python.exe

import os
import cgi
from http import cookies

params = cgi.FieldStorage()

def decide_page(page_str):
    if page_str == '1st':
        return 1
    elif page_str == '2nd':
        return 2
    
page = decide_page(params.getvalue('page'))

def print_page(page):
    if page == 1:
        print("""
        <!DOCTYPE html>
        <html>
        <head><title>VJEZBANJE 7</title></head>
        <body>
        <form>
        <table border="1">
        <tr>
        <td>
        Ime: 
        </td>
        <td>
        """)
        print('<input type="text" name="ime" value="' + get_cookie('ime') + '">')
        print("""
        </td>
        </tr>
        <tr>
        <td>
        Sifra:
        </td>
        <td>
        """)
        print('<input type="password" name="pswd" value="' + get_cookie('pswd') + '">')
        print("""
        </td>
        </tr>
        <tr>
        <td>
        Spol:
        </td>
        <td>
        Male:
        """)
        if get_cookie('radio') == 'male':
            print('<input type="radio" name="radio" value="male" checked>')
        else:
            print('<input type="radio" name="radio" value="male">')
        print('Female:')
        if get_cookie('radio') == 'female':
            print('<input type="radio" name="radio" value="female" checked>')
        else:
            print('<input type="radio" name="radio" value="female">')
        print('Undefined:')
        if get_cookie('radio') == 'undefined':
            print('<input type="radio" name="radio" value="undefined" checked>')
        else:
            print('<input type="radio" name="radio" value="undefined">')

        print("""
        </td>
        </tr>
        </table>
        <input type="submit" name="page" value="1st">
        <input type="submit" name="page" value="2nd">
        </form>
        </body>
        </html>
        """)
    else:
        print("""
        <!DOCTYPE html>
        <html>
        <head><title>VJEZBANJE 7</title></head>
        <body>
        <form>
        <table border="1">
        <tr>
        <td>
        E-mail: 
        </td>
        <td>
        """)
        print('<input type="text" name="mail" value="' + get_cookie('mail') + '">')
        print("""
        </td>
        </tr>
        </table>
        <input type="submit" name="page" value="1st">
        <input type="submit" name="page" value="2nd">
        </form>
        </body>
        </html>
        """)

def set_cookie():
    cookie = cookies.SimpleCookie()
    for key in params:
        cookie[key] = params.getvalue(key)
    print(cookie)

def get_cookie(name):
    cookie_str = os.environ.get('HTTP_COOKIE', '')
    cookie_str_obj = cookies.SimpleCookie(cookie_str)
    for key in params:
        if key:
            if key == name:
                return params.getvalue(key)
    for key in cookie_str_obj:
        if key:
            if key == name:
                return cookie_str_obj[key].value
    return ""
            

set_cookie()
print()
print_page(page)


