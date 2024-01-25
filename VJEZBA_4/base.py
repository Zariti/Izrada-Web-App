#! python.exe

import translate

def start_html():
    print ("""<!DOCTYPE html>
    <html>
    <body>""")

def finish_html():
    print ("""</body>
    </html>""")

def print_navigation(language): #language se izvlaci kao key iz translations dictionarya
    print ('''
    <div>
    <a href="index.py">''' + translate.make_translation(language, 'index') + '''</a>
    <a href="articles.py">''' + translate.make_translation(language, 'articles') + '''</a>
    <a href="basket.py">''' + translate.make_translation(language, 'basket') + '''</a>
    <a href="contact.py">'''+ translate.make_translation(language, 'contact') + '''</a>	
    </div>''')     

  
    

        
    