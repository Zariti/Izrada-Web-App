#!python.exe
import cgi
import cgitb
from http import cookies

cgitb.enable()

# create a cookie object
cookie = cookies.SimpleCookie()

# get form data
form = cgi.FieldStorage()

# get the selected radio value
radio_value = form.getvalue('radio')

# set the cookie value
cookie['radio'] = radio_value

# set the cookie expiration time
cookie['radio']['expires'] = 24 * 60 * 60

# print the content-type header and the cookie
print("Content-Type: text/html")
print(cookie)

# print the response


print("""
<!DOCTYPE html> 
<html>
<head></head>
<body>
<h1>Radio Form</h1>
<form action='' method='post'>
<input type='radio' name='radio' value='option1'>Option 1<br>
<input type='radio' name='radio' value='option2'>Option 2<br>
<input type='radio' name='radio' value='option3'>Option 3<br>
<input type='submit' value='Submit'>
</form>
</body>
</html>
""")