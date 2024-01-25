#!python.exe
import os
from http import cookies
import cgi

#C = cookies.SimpleCookie()
#C['Ime'] = 'Maro'
#C['Prezime'] = 'Ancic'
#C['Godiste'] = 2003

#print(C) 
#ili
#print(C.output())

#C = cookies.SimpleCookie()
#C['Server'] = "Google"
#C['Server']['Path'] = '/nekipath/lmao'
#print(C.output(attrs=[],header='Cookie: '))



cookie = cookies.SimpleCookie()
cookie["input"] = 'test cookie'
print(cookie)

params = cgi.FieldStorage()

cookie['radio'] = params.getvalue("rejdio")
print(cookie)


print("""
<!DOCTYPE html>
<html>
<head><title>COOKIEEEE</title>
<body>
<h1>OVO JE PROTOTIP VJEZBE 3</h1>
<form>
M:
<input type="radio" name="rejdio" value="Musko">
F:
<input type="radio" name="rejdio" value="Zensko">
X:
<input type="radio" name="rejdio" value="X">
<input type="submit" value="SUMBIT">
</form>
<form action="http://www.google.com">
<button>Click Me</button>
</form>
""")
print(cookie["input"].value)
print(cookie["radio"].value)
print("""
</body>
</html>
""")







