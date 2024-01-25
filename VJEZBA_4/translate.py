#! python.exe
import os
from http import cookies


translations = {
    'hr': { 'index' : 'Kuci', 'articles' : 'Proizvodi', 'contact' : 'Kontakt', 'basket' : 'Kosarica' },
    'eng':{ 'index' : 'Home', 'articles' : 'Articles', 'contact' : 'Contact', 'basket' : 'Basket' },
    'de' : {'index' : 'Haus', 'articles' : 'Artikeln', 'contact' : 'Kontakt', 'basket' : 'Verkaufstasche' }
    }

def decide_language(lang=None):  #ovde ide params.getvalue('lang')
    http_cookies_str = os.environ.get('HTTP_COOKIE', '')
    get_all_cookies_object = cookies.SimpleCookie(http_cookies_str)    
    if lang:    #ako je lang vec u parametrima (klikli smo na neki lang)
        cookie = cookies.SimpleCookie()
        cookie['lang']= lang
        print (cookie.output())#printanje cookie-a u header

    elif get_all_cookies_object.get("lang"):    #ako vec postoji lang u cookie-ima uzmi njegovu vrijednost (ako klikcemo izmedu izbora)   
        lang = get_all_cookies_object.get("lang").value

    else:         #ako je lang = None stavi ga default eng
        lang = 'eng'
    return lang


def display_language():
    global translations
    #language se uzima iz translations (hr , eng, ili de)
    for language in sorted (translations, reverse=True): #alt code: for language in translations. Oda po translacijama i ispisuje ih obrnuto abecedno (reverse=True) 
        print ('<a href="?lang=' + language + '">' + language + '</a>')  #

def make_translation(language, key):
    return translations.get(language, translations['eng']).get(key, "prazno") 
    #npr. ako je language=hr i key='articles' onda ce vratit => 'artikli'

