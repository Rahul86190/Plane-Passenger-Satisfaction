import sqlite3 
conn = sqlite3.connect("planedata.db") 

cur = conn.cursor() 
query = "select * from planeDetails"

cur.execute(query) 
for record in cur.fetchall():
    print(record) 

cur.close()
conn.close() 