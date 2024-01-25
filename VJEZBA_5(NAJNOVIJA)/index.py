#! python.exe

import base
import translate
import cgi
import os

params = cgi.FieldStorage()
language = translate.decide_language(params.getvalue("lang", None)) 
print ()
base.start_html()
base.print_navigation(language)
translate.display_language()
base.finish_html()

#print(os.environ)
