#! python.exe

import base
import translate
import cgi
import os

params = cgi.FieldStorage()
language = translate.decide_language(params.getvalue("lang", None))  #vratit ce (en, hr, il de)
print ()
base.start_html()
base.print_navigation(language) #uzima jezik(en, hr il de (u parametar)) i ispisuje prijevode. ukratko.
translate.display_language()  #samo uzima keyeve iz translationsa i stavlja ih u hyperlink. ukratko.
base.finish_html()

#print(os.environ)
print()
print(params)



# def print_navigation(language): #language se izvlaci kao key iz translations dictionarya
#    print ('''
#    <div>
#    <a href="index.py">''' + translate.make_translation(language, 'index') + '''</a>
#    <a href="articles.py">''' + translate.make_translation(language, 'articles') + '''</a>
#    <a href="basket.py">''' + translate.make_translation(language, 'basket') + '''</a>
#    <a href="contact.py">'''+ translate.make_translation(language, 'contact') + '''</a>	
#    </div>''')     
