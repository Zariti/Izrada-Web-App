import mysql.connector # "C:\ProgramData\Anaconda3\python.exe" -m pip install mysql-connector 
import json

db_conf = {
    "host":"localhost",
    "db_name":"maroancic",
    "user":"root",
    "passwd":""
}

def get_DB_connection():
    mydb = mysql.connector.connect(
        host=db_conf["host"],
        user=db_conf["user"],
        passwd=db_conf["passwd"],
        database=db_conf["db_name"]
    )
    return mydb

def create_session():
    query = "INSERT INTO session (data) VALUES (%s)"
    values = (json.dumps({}),)
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute(query, values)
    mydb.commit()
    return cursor.lastrowid 

def get_session(session_id):  # (PROVJERENA)
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM session WHERE session_id=" + str(session_id)) #trazi redak sa odg session_id
    myresult = cursor.fetchone()
    return myresult[0], json.loads(myresult[1]) #vrati id i formatiran data

def replace_session(session_id, data):#replace->prvo izbrisi, a onda ubaci (delete/insert)
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("""
    REPLACE INTO session(session_id,data) 
    VALUES (%s,%s)""",
    (session_id, json.dumps(data)))
    mydb.commit()


# NOVE 
def update_session(session_id, data):#replace-prvo izbrisi, a onda ubaci (delete/insert)
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute('''
    UPDATE session SET data=%s 
    WHERE session_id=%s''', (json.dumps(data),session_id))   
    mydb.commit()

def destroy_session(session_id):
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    query = 'DELETE FROM session WHERE session_id= (%s)'
    values = (session_id, )
    cursor.execute(query, values)
    mydb.commit()
