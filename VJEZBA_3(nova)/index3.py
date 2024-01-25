#!python.exe

from http import cookies
import base
#import subjects
import cgi
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

cookie = cookies.SimpleCookie()
params = cgi.FieldStorage()
cookie_value = params.getvalue('year')
#cookie_status_value = params.getvalue('radio')





#cookie_status1 = params.getvalue('radio1')
#cookie_status2 = params.getvalue('radio2')
#cookie_status3 = params.getvalue('radio3')
#cookie_status4 = params.getvalue('radio4')

#cookie['status1'] = cookie_status1
#cookie['status2'] = cookie_status2
#cookie['status3'] = cookie_status3
#cookie['status4'] = cookie_status4






#cookie['year'] = "4"



def decide_year(cookie_value):
    if cookie_value == "1st":
        cookie['year'] = cookie_value
        print(cookie) #OVO JE BITNO JER PRIBACUJE COOKIE NA BROWSER
        return 1
    elif cookie_value == "2nd":
        cookie['year'] = cookie_value
        print(cookie)
        return 2
    elif cookie_value == "3rd":
        cookie['year'] = cookie_value
        print(cookie)
        return 3
    else:
        return 4

def save_status():
    pass


year = decide_year(params.getvalue('year', '1st')) #vraca(int) 1 ili 2 ili 3   
#status = save_status() 


def set_cookies():
    cookie = cookies.SimpleCookie()
    for key in params:
        cookie[key] = params.getvalue(key)
    print(cookie)



radio_values = {}

#OVO JE NAJTEZA FUNKCIJA (!)
def check(value, key_subject): #value od radia
    cookie_str = os.environ.get('HTTP_COOKIE','')  #ovde su value-i odvojeni sa ';'
    cookie_str_obj = cookies.SimpleCookie(cookie_str) #stavljamo ih u cookie_str_obj kako bi lakse odali po njima
    for key in cookie_str_obj:
        if cookie_str_obj.get(key):   #ako key uopce postoji    
            if key == key_subject: 
                status = cookie_str_obj.get(key).value
                if value == status:
                    return True
                else:
                    return False






    


def change_data(year):
    cnt = 0 #za minjat name od radia u svakoj petlji
    if year == 4:
        for key in subjects:
            print("""
            <tr>
            <td>
            """)
            print(subjects.get(key).get('name'))
            print("""
            </td>
            """)
            print("""
            <td>
            """)
            


            if check("not_selected", key):  #usporeduje key i 'not_selected' 
                print('Ne Upisuje')
            elif check("enrolled", key):
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
            
    for key in subjects:
        if (subjects.get(key).get('year') == year):
            cnt += 1
            print("""
            <tr>
            <td>
            """)
            print(subjects.get(key).get('name'))
            print("""
            </td>
            """)
            print("""
            <td>
            """)
            


            if check("not_selected", key):  #usporeduje key i 'not_selected' 
                print('Not selected: <input type="radio" name="' + key + '" value="not_selected" checked>')
            else:
                print('Not selected: <input type="radio" name="' + key + '" value="not_selected">')
            if check("enrolled", key):
                print('Enrolled: <input type="radio" name="' + key + '" value="enrolled" checked>')
            else:
                print('Enrolled: <input type="radio" name="' + key + '"value="enrolled">')
            if check("passed", key):
                print('Passed: <input type="radio" name="' + key + '" value="passed" checked>')
            else:
                print('Passed: <input type="radio" name="' + key + '" value="passed">')
            print("""
            </td>
            </tr>
            """)
    

def save_status(year):
    pass
    




def print_form():
    print("""
    <form>
        <input type="submit" name="year" value="1st">
        <input type="submit" name="year" value="2nd">
        <input type="submit" name="year" value="3rd">
        <input type="submit" name="year" value="upisni list">
        <table border="1">
    """)
    change_data(year)  #daje odreden broj predmeta
    print("""
        </table>
    </form>
    """)




    
set_cookies() #header 
print() #header
base.start_html() #body
print_form() #body
base.end_html() #body