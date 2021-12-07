import sqlite3
import time
conn = sqlite3.connect('./entries.db')
cur = conn.cursor()
cur.execute('SELECT * from users')
res = cur.fetchall()
for entry in res:
    print(entry[0],entry[1],entry[2],time.ctime(entry[3]))

cur.execute('DELETE from users where email="wuchang@pdx.edu"')
conn.commit()
