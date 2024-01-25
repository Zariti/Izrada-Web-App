#! python.exe

import base
import translate
import model
import session
import os
import cgi
import db

params = cgi.FieldStorage()
language = translate.decide_language(params.getvalue("lang", None))

if (os.environ["REQUEST_METHOD"].upper() == "POST"):
    session.remove_from_session(params)

session_id = session.get_or_create_session_id()
_,session_data = db.get_session(session_id)

print()
base.start_html()
base.print_navigation(language) 
translate.display_language()
articles = model.get_articles()
print ('<form action="" method="post">')
for key, article in session_data.items():
    model.display_basket_checkbox(key, article)
print ('<input type="submit" value="Remove"></form>')
    
base.finish_html()

print()
print(params)
print('---')
print('---')
print('---')
print(session_data)


