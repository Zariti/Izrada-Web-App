#!python.exe
import os
import cgi
from http import cookies

#languages = {
#            'eng':{'Home':'Home', 'Buy':'Buy'},
#             'hr':{'Home':'Pocetna', 'Buy':'Kupi'},
#             'ger':{'Home':'Haus', 'Buy':'Kupenzi'}
#             }

def html_start():
    print("""
    <!DOCTYPE html>
    <html>
    <head><title>Jezici</title></head>
    <body>
    """)

def html_end():
    print("""
    </body> 
    </html>
    """)

#username_correct = 'maro'
#password_correct = 'stalker3451'

params = cgi.FieldStorage()
page = params.getvalue('page')
username = params.getvalue('name')
password = params.getvalue('pswd')

def get_cookies(input_name):
    cookie_str = os.environ.get('HTTP_COOKIE', '')
    cookie_str_obj = cookies.SimpleCookie(cookie_str)
    for key in cookie_str_obj:
        if cookie_str_obj.get(key): #for security   -----  if key in cookie_str_obj:
            if key == input_name:
                return cookie_str_obj[key].value
    return None  #OVDE JE BILA GRESKA STA MI JE ODUZELA VECI DIO ZIVOTA
                 #TRIBA OVAJ 'RETURN NONE' STAVIT NA RAZINU FOR PETLJE NE NA RAZINU IF-OVA
            
        

def print_content():
    
    
    #print(params)
    if params.getvalue('page') == '1st':
        print("""
        <h1>
        """)
        print(cookie['stalker'].value)
        print("""
        </h1>
        <form>
        <table border="1">
        <tr>
        <td>
        Username:
        """)
        my_cookie = get_cookies('name')
        if my_cookie:
            print(f'<input type="text" name="name" value="{my_cookie}">')
        else:
            print('<input type="text" name="name" value="">')
            print(get_cookies('name'))
        print("""
        </td>
        </tr>
        <tr>
        <td>
        Password:
        """)
        my_cookie = get_cookies('pswd')
        if my_cookie:
            print('<input type="password" name="pswd" value="' + my_cookie +'">')
        else:
            print('<input type="password" name="pswd" value="">')
        print("""
        </td>
        </tr>
        </table>
        <input type="submit" name="page" value="1st">
        <input type="submit" name="page" value="2nd">
        </form>
        """)
    elif params.getvalue('page') == '2nd':
        print("""
        <h2>Spol:</h2>
        <form>
        Musko:
        """)
        my_cookie = get_cookies('radio') 
        if my_cookie == 'musko':
            print(f'<input type="radio" name="radio" value="musko" checked>')
        else:
            print('<input type="radio" name="radio" value="musko">') #triba uvik pazit da zatvorin sa '>' tu faljivan
        print("""
        Zensko:
        """)
        if my_cookie == 'zensko':
            print(f'<input type="radio" name="radio" value="zensko" checked>')
        else:
            print('<input type="radio" name="radio" value="zensko">')
        print("""
        X:
        """)
        if my_cookie == 'x':
            print(f'<input type="radio" name="radio" value="x" checked>')
        else:
            print('<input type="radio" name="radio" value="x">')
        print("""
        <input type="submit" name="page" value="1st">
        <input type="submit" name="page" value="2nd">
        </form>
        """)
    else:
        my_cookie = get_cookies('name')
        if my_cookie:
            print(f'<input type="text" name="name" value="{my_cookie}">')
        else:
            print('<input type="text" name="name" value="">')
            print(get_cookies('name'))
        print("""
        </td>
        </tr>
        <tr>
        <td>
        Password:
        """)
        my_cookie2 = get_cookies('pswd')
        if my_cookie2:
            print('<input type="password" name="pswd" value="' + my_cookie2 +'">')
        else:
            print('<input type="password" name="pswd" value="">')
        print("""
        </td>
        </tr>
        </table>
        <input type="submit" name="page" value="1st">
        <input type="submit" name="page" value="2nd">
        </form>
        """)


def set_cookies():
    cookie = cookies.SimpleCookie()
    for key in params:
        cookie[key] = params.getvalue(key)
    print(cookie)




        

            

set_cookies()   #header
cookie = cookies.SimpleCookie()
cookie['stalker'] = 'S.T.A.L.K.E.R'
print(cookie) 
print()         #header
html_start()
print_content()
html_end()

    

