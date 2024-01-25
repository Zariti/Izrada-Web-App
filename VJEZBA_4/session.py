import db
import os
from http import cookies

def get_or_create_session_id():
    http_cookies_str = os.environ.get('HTTP_COOKIE', '')
    get_all_cookies_object = cookies.SimpleCookie(http_cookies_str)
    session_id = get_all_cookies_object.get("session_id").value if get_all_cookies_object.get("session_id") else None
    if session_id is None: #ako ne postoji session_id u cookie-ima, stvori ga 
        session_id = db.create_session()
        cookies_object = cookies.SimpleCookie()
        cookies_object["session_id"] = session_id
        print (cookies_object.output()) #upisivanje cookie-a u header
    return session_id

def add_to_session(params):
    session_id = get_or_create_session_id()
    _, data = db.get_session(session_id)#vracanje do sada odabranih podataka
    for article_id in params.keys():
        data[article_id] = data.get(article_id, 0) + 1
    db.replace_session(session_id, data)



