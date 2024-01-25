#!python.exe

from http import cookies

cookie_string = "cookie_name=cookie_value; another_cookie=another_value"
cookie = cookies.SimpleCookie()
cookie.load(cookie_string)

cookie_value = cookie.get("cookie_name").value
print(cookie_value)