#! python.exe

import base
import os 
import cgi
import translate #
import model    #
import session  #

params = cgi.FieldStorage()
language = translate.decide_language(params.getvalue("lang", None)) #vraca en, hr il de
if (os.environ["REQUEST_METHOD"].upper() == "POST"):
    session.add_to_session(params)
print()
base.start_html()
base.print_navigation(language) 
translate.display_language()
articles = model.get_articles()             #dobavlja cijeli dictionary 'articles'
print ('<form action="" method="post">')    #salje se na samu sebe metodom POST
for key, article in articles.items():       #hoda po 'articles' dict     
    model.display_article_checkbox(key, article)    #ispisuje checkbox opcije, uzima (key=>neki int) i (article=>ime artikla) 
print ('<input type="submit" value="Add"></form>')  #submit button koji salje paramse (key=ime) npr. ('1'='CPU')
    
base.finish_html()

# def print_navigation(language): #language se izvlaci kao key iz translations dictionarya
#    print ('''
#    <div>
#    <a href="index.py">''' + translate.make_translation(language, 'index') + '''</a>
#    <a href="articles.py">''' + translate.make_translation(language, 'articles') + '''</a>
#    <a href="basket.py">''' + translate.make_translation(language, 'basket') + '''</a>
#    <a href="contact.py">'''+ translate.make_translation(language, 'contact') + '''</a>	
#    </div>''')     



