#!python.exe

import os
import cgi
from http import cookies

params = cgi.FieldStorage()

def html_start():       #1 korak (setup)
    print("""
    <!DOCTYPE html>
    <html>
    <head><title>index8</title></head>
    <body>
    """)

def html_end():
    print("""
    </body>
    </html>
    """)

def set_cookie():
    cookie = cookies.SimpleCookie()
    for key in params:
        cookie[key] = params.getvalue(key)
    print(cookie)

cookie_str = os.environ.get('HTTP_COOKIE', '')
cookie_str_obj = cookies.SimpleCookie(cookie_str)

def decide_page(page_str):
    if page_str == '1st':
        return 1
    elif page_str == '2nd':
        return 2
    else:
        return 3

page = decide_page(params.getvalue('page', '1st'))

def print_form(page):
    print("""
    <form>
    <input type="submit" name="page" value="1st">
    <input type="submit" name="page" value="2nd">
    <table border="1">
    """)
    if page == 1:
        print("""
        <tr>
        <td>
        Ime:
        </td>
        <td>
        """)
        if get_cookie('username') != "":
            print('<input type="text" name="username" value="' + get_cookie('username') + '">')
        else:
            print('<input type="text" name="username" value="">')

        print("""
        </td>
        </tr>
        <tr>
        <td>
        Password:
        </td>
        <td>
        """)
        print('<input type="password" name="pswd" value="">')
        print("""
        </td>
        </tr>
        """)
    else:
        print("""
        <tr>
        <td>
        Ime:
        </td>
        <td>
        """)
        print('<input type="text" name="email" value="">')
        print("""
        </td>
        </tr>
        <tr>
        <td>
        Spol:
        </td>
        <td>
        """)
        print('Musko: <input type="radio" name="spol" value="musko">')
        print('Zensko: <input type="radio" name="spol" value="zensko">')
        print('Neodredeno: <input type="radio" name="spol" value="x">')
        print("""
        </td>
        </tr>
        """)

    
    print("""
    </table>
    </form>
    """)

def get_cookie(name):
    cookie_str = os.environ.get('HTTP_COOKIE', '')
    cookie_str_object = cookies.SimpleCookie(cookie_str)
    for key in cookie_str_object:
        if key:
            if key == name:
                return cookie_str_obj[key].value 
    return ""


set_cookie()
print()
html_start()
print_form()
html_end()