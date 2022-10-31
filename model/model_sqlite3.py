import time
from .Model import Model
import sqlite3
DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from users")
        except sqlite3.OperationalError:
            cursor.execute("create table users (email text, ip text, wallet text, last integer, eth real)")
        cursor.close()

    def select(self, email, ip, wallet):
        """
        Gets most recent timestamp the email, ip, or wallet address got ETH
        :param email: String
        :param ip: String
        :param wallet: String
        :return: 0 if email, ip, or wallet is in database, last value otherwise
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT last FROM users WHERE email=? or ip=? or wallet=? ORDER BY last DESC LIMIT 1", (email,ip,wallet))
        res = cursor.fetchall()
        if len(res) > 0:
            last = res.pop()[0]
        else:
            last = 0
        return last

    def select_all(self, sort):
        """
        Gets all rows from the database
        :return: Rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        #cursor.execute("SELECT email,ip,wallet,last FROM users ORDER BY last DESC LIMIT 200")
        if (sort == "ip"):
            cursor.execute("SELECT s.* FROM (SELECT email,ip,wallet,last,eth FROM users ORDER BY last DESC LIMIT 300) s ORDER BY s.ip ASC")
        else:
            cursor.execute("SELECT email,ip,wallet,last,eth FROM users ORDER BY last DESC LIMIT 300")
        res = cursor.fetchall()
        return res

    def select_last_ip(self, number):
        """
        Gets recent requests from the database
        :param: number of requests
        :return: List of /16 IP prefixes for previous number of requests
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor() 
        cursor.execute(f'SELECT ip from users ORDER BY last DESC limit {number}')
        res = cursor.fetchall() 
        ips = []
        if len(res):
            for entry in res:
                chop = entry[0].split('.')[:2]
                chop_addr = '.'.join(chop)
                ips.append(chop_addr)
        return ips

    def insert(self, email, ip, wallet, eth):
        """
        Inserts entry into database
        :param email: String
        :param ip: String
        :param wallet: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        last = int(time.time())
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into users VALUES (?,?,?,?,?)", (email,ip,wallet,last,eth))
        connection.commit()
        cursor.close()
        return True
