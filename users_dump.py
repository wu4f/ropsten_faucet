import sqlite3
import time
conn = sqlite3.connect('./entries.db')
cur = conn.cursor()
#cur.execute('SELECT last from users where ip="" or email="" or wallet="" ORDER BY last DESC LIMIT 1')
cur.execute('SELECT * from users order by last desc limit 30000')
res = cur.fetchall()
if len(res) == 0:
    print("No entry for address")
else:
    for entry in res:
        print(f'{entry[0]:4},{entry[1]},{entry[2]},{time.ctime(entry[3])},{entry[4]}')

cur.execute('DELETE from users where email="wuchang@pdx.edu"')
#cur.execute('DELETE from users where email="sodamdondoa@gmail.com"')
conn.commit()
