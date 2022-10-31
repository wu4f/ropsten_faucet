import sqlite3
import time
from collections import Counter
import sys

number = sys.argv[1]
conn = sqlite3.connect('./entries.db')
cur = conn.cursor()

#now = int(time.time()) - 100000
#qcur.execute('SELECT last from users where ip="" or email="" or wallet="" ORDER BY last DESC LIMIT 1')
#cur.execute(f'SELECT ip from users where last > {now}')
cur.execute(f'SELECT ip from users ORDER BY last DESC limit {number}')
res = cur.fetchall()

ips = dict()

for entry in res:
    chop = entry[0].split('.')[:2]
    chop_addr = '.'.join(chop)
    if chop_addr in ips:
        ips[chop_addr] = ips[chop_addr] + 1;
    else:
        ips[chop_addr] = 1

top_ips = dict(Counter(ips).most_common(15))
for k in top_ips:
    print(f'{top_ips[k]} : {k}')

ips = dict()
print("----------------------")
for entry in res:
    chop_addr = entry[0].split('.')[0]
    if chop_addr in ips:
        ips[chop_addr] = ips[chop_addr] + 1;
    else:
        ips[chop_addr] = 1

top_ips = dict(Counter(ips).most_common(10))
for k in top_ips:
    print(f'{top_ips[k]} : {k}')
