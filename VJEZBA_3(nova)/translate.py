#!python.exe
from http import cookies
import os


translations = {
    "eng":{'home':'home', 'articles':'articles', 'cart':'cart', 'contact':'contact'},
    "hr":{'home':'pocetna', 'articles':'artikli', 'cart':'kosarica', 'contact':'kontakt'},
    "de":{'home':'Haus', 'articles':'Artikeln', 'cart':'Verkaufstasche', 'contact':'Kontakt'},
    "es":{'home':'Casa', 'articles':'Arti', 'cart':'Bolsa', 'contact':'Kontacto'}
}

def decide_language(lang=None): #u parametru je umisto 'lang' zapravo params.getvalue(lang), u params se stavlja ono sta kliknes
    cookies_string = os.environ.get('HTTP_COOKIE', '')  #trazi se iz os params??
    all_cookies_object = cookies.SimpleCookie(cookies_string) #te ga sprema u cookie na serveru pod imenom 'all_cookies_object'
    if lang is not None: #ako se lang nalazi u params odnosno ako je lang odabram
        cookie = cookies.SimpleCookie() #stvara se cookie varijabla na serveru
        cookie['lang'] = lang  #cookie-u dajemo ime 'lang' i vrijednost koja se nalazi u params.getvalue('lang')/salje ga browseru
        print (cookie.output())  #ovo je zapravo Set-Cookie: (sa svim atributima) koji se salju u http header
    elif all_cookies_object.get('lang'): #pri drugom posjetu stranici?? tjst ako je cookie vec na kompu uzece ga
        lang = all_cookies_object.get('lang').value
    else: #ako prvi put udemo u stranicu
        lang = 'eng' 
    return lang




def display_language(): #prikazuje jezike sve ispod (en hr de ..) kad kliknemo oni salju info o jeziku kojeg smo kliknuli
    for key in translations: #hoda po svim keyevima od translations (eng, hr, de...) i printa ih redon
        print ('<a href="?lang=' + key + '">' + key + '</a>') #ovo su zapravo get-ovi (?lang=xyz)


def make_translations(language, key): #sluzi za promjenu naziva u navigaciji
    return translations.get(language, translations['eng']).get(key, 'prazno')   ##ovo tu koristimo za nav medu godinama 
# more se i bez ovog 'prazno'

# --> .get(language, translations['eng']) daje kljuc od npr 'hr', a  .get(key) daje vrijednost 
# --> .get(language) more i bez ovog translations['eng']
# alt verzija jednostavnija i jasnija u svakom pogledu
def make_translations2(language, key):
    return translations.get(language).get(key)

# .get(key, value)

# language je zap value od npr 'hr' a to je {home : pocetna, article : artikli...}
# translations['eng'] je zap value od 'eng' a to je {home : home, article : article...}
                                                                                