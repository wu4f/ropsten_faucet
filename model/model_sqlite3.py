"""
Per-user faucet access to rate limit requests
+------------------+------------+
| Email            | last       |
+==================+============+
| jdoe@example.com | 123456789  |
+------------------+------------+

This can be created with the following SQL (see bottom of this file):

    create table users (email text, last integer);

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
            cursor.execute("create table users (email text, last integer)")
        cursor.close()

    def select(self, email):
        """
        Gets all rows from the database
        Each row contains: email, last
        :return: 0 if not in database, last value otherwise
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT last FROM users WHERE email=?", (email,))
        res = cursor.fetchall()
        if res:
            last = res.pop()[0]
        else:
            last = 0
        return last

    def insert(self, email):
        """
        Inserts entry into database
        :param email: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        last = int(time.time())
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into users VALUES (?,?)", (email,last))
        #cursor.execute("insert into users (email, last) VALUES (:email, :last)", params)
        connection.commit()
        cursor.close()
        return True

    def update(self, email):
        """
        Updates entry in database
        :param email: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        last = int(time.time())
        params = {'email':email, 'last':last}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("update users set last=? where email=?",(last, email))
        connection.commit()
        cursor.close()
        return True
