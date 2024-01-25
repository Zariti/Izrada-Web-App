#! python.exe

import base
import translate
import model
import session
import os
import cgi

params = cgi.FieldStorage()
language = translate.decide_language(params.getvalue("lang", None))
if (os.environ["REQUEST_METHOD"].upper() == "POST"):
    session.add_to_session(params)
print()
base.start_html()
base.print_navigation(language) 
translate.display_language()
articles = model.get_articles()
print ('<form action="" method="post">')
for key, article in articles.items():
    model.display_article_checkbox(key, article)
print ('<input type="submit" value="Add"></form>')
    
base.finish_html()


