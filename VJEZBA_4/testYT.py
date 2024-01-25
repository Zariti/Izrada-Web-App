#!python.exe
import mysql.connector
print('Content-Type text/html\n')

conn = mysql.connector.connect(host='localhost', user='root', password='', database='ducan')
cursor = conn.cursor()
selectquery = 'select * from ducan'
cursor.execute(selectquery)
records = cursor.fetchall()

print('No. of students', cursor.rowcount)

for row in records:
    print('session id', row[0])
    print('data', row[1])
    print()

cursor.close()
conn.close()
