import sqlite3
import time
import re
import model

def match(expr, item):
    return re.match(expr,item) is not None

def poison_wallet(cur, wallet):
    now = int(time.time()) + 31536000
    cur.execute("update users set last=? where wallet=?",(now, wallet))
    cur.execute(f'SELECT * from users where wallet="{wallet}"')
    res = cur.fetchall()
    for entry in res:
        print(f'{entry[0]:4},{entry[1]},{entry[2]},{time.ctime(entry[3])}')

def poison_ip(cur, prefix):
    cur.execute(f'SELECT * from users where ip REGEXP "^{prefix}"')
    res = cur.fetchall()
    now = int(time.time()) + 31536000
    for entry in res:
        ip = entry[1]
        cur.execute("update users set last=? where ip=?",(now, ip))
    cur.execute(f'SELECT * from users where ip REGEXP "^{prefix}"')
    res = cur.fetchall()
    for entry in res:
        print(f'{entry[0]:4},{entry[1]},{entry[2]},{time.ctime(entry[3])}')

conn = sqlite3.connect('./entries.db')
conn.create_function('regexp', 2, lambda x,y: 1 if re.search(x,y) else 0)
cur = conn.cursor()
poison_ip(cur, "173.245.203")
poison_ip(cur, "103.129.255")
poison_ip(cur, "45.14.195")
poison_ip(cur, "217.114.38")
poison_ip(cur, "192.145.116")
poison_ip(cur, "45.14.195")
poison_ip(cur, "118.235")
poison_ip(cur, "211.246")
poison_ip(cur, "223.38")
poison_ip(cur, "223.62")
poison_ip(cur, "23.249")
poison_ip(cur, "39.7")
conn.commit()
#poison_wallet(cur, "0x913c9fdb2140b57aaf2206be006ca2e5de62d646")
#cur.execute('SELECT last from users where ip="" or email="" or wallet="" ORDER BY last DESC LIMIT 1')
