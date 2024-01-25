#! python.exe
import os
from http import cookies


translations = {
    'hr': { 'index' : 'Kuci', 'articles' : 'Proizvodi', 'contact' : 'Kontakt', 'basket' : 'Kosarica' },
    'eng':{ 'index' : 'Home', 'articles' : 'Articles', 'contact' : 'Contact', 'basket' : 'Basket' },
    'de' : {'index' : 'Haus', 'articles' : 'Artikeln', 'contact' : 'Kontakt', 'basket' : 'Verkaufstasche' }
    }

def decide_language(lang=None):  
    http_cookies_str = os.environ.get('HTTP_COOKIE', '')
    get_all_cookies_object = cookies.SimpleCookie(http_cookies_str)    
    if lang is not None:
        cookie = cookies.SimpleCookie()
        cookie['lang']= lang
        print (cookie.output())#printanje cookie-a u header

    elif get_all_cookies_object.get("lang"):        
        lang = get_all_cookies_object.get("lang").value

    else:
        lang = 'eng'
    return lang




def display_language():
    global translations

    for language in sorted (translations, reverse=True):
        print ('<a href="?lang=' + language + '">' + language + '</a>')

def make_translation(language, key):
    return translations.get(language, translations['eng']).get(key, "prazno")

