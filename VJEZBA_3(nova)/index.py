#!python.exe
import base
import cgi
import translate
import os

params = cgi.FieldStorage()
language = translate.decide_language(params.getvalue('lang'))

def print_navigation():
    print("""
    <div>
    <a href="index.py">""" + translate.make_translations(language, 'home') + """</a>
    <a href="index.py">""" + translate.make_translations(language, 'articles') + """</a>
    <a href="index.py">""" + translate.make_translations(language, 'cart') + """</a>
    <a href="index.py">""" + translate.make_translations(language, 'contact') + """</a>
    </div>
     """)



base.start_html()
print_navigation()
translate.display_language() #ovde je prikazan izbor jezika (eng, hr, de, es)
base.end_html()
print (params)
#print (os.environ)
