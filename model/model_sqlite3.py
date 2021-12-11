"""
Per-user faucet access to rate limit requests
+------------------+----------------+-------------+-----------+
| Email            | ip             | wallet      | last      |
+==================+================+=============+===========+
| jdoe@example.com | 131.252.220.66 | 0xAbC123... | 123456789 |
+------------------+----------------+-------------+-----------+

This can be created with the following SQL (see bottom of this file):

    create table users (email text, ip text, wallet text, last integer)

"""
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
            cursor.execute("create table users (email text, ip text, wallet text, last integer)")
        cursor.close()

    def select(self, email, ip, wallet):
        """
        Returns the most recent timestamp the email, ip, or wallet address got ETH
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

    def select_all(self):
        """
        Gets all rows from the database
        Each row contains: email, last
        :return: 0 if not in database, last value otherwise
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users ORDER BY last DESC LIMIT 50")
        res = cursor.fetchall()
        return res

    def insert(self, email, ip, wallet):
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
        cursor.execute("insert into users VALUES (?,?,?,?)", (email,ip,wallet,last))
        connection.commit()
        cursor.close()
        return True

    def update(self, email, ip, wallet):
        """
        Updates entry in database
        :param email: String
        :param ip: String
        :param wallet: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        last = int(time.time())
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("update users set ip=?, wallet=?, last=? where email=?",(ip, wallet, last, email))
        connection.commit()
        cursor.close()
        return True
