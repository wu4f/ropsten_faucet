import sqlite3
import time
conn = sqlite3.connect('./entries.db')
cur = conn.cursor()
cur.execute('SELECT * from users')
res = cur.fetchall()
for entry in res:
    print(entry)
exit()

print(int(time.time()))
cur.execute('UPDATE users set last=0 where email="wuchang@pdx.edu"')
conn.commit()
cur.execute('SELECT * from users')
print(cur.fetchall())
print(int(time.time()))
