#!python.exe                

import os                   #kao prvo importat sve (osnovno)
import cgi
from http import cookies

params = cgi.FieldStorage()  #pa onda ove paramse (osnovno)


def html_start():       #1 korak (setup)
    print("""
    <!DOCTYPE html>
    <html>
    <head><title>index9</title></head>
    <body>
    """)

def html_end():         #2 korak (setup)
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

            if check("not_selected", key):
                print('Ne upisuje')

            elif check("enrolled", key):
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
                if check("not_selected", key):
                    print(f'Not selected: <input type="radio" name="{key}" value="not_selected" checked>')
                else:
                    print(f'Not selected: <input type="radio" name="{key}" value="not_selected">')
                if check("enrolled", key):
                    print(f'Enrolled: <input type="radio" name="{key}" value="enrolled" checked>')
                else:
                    print(f'Enrolled: <input type="radio" name="{key}" value="enrolled">')
                if check('passed', key):
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

def check(radio_value, subj_key):
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



set_cookie()
print()
html_start()
print_form(year)
html_end()



    