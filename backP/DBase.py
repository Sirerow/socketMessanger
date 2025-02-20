import sqlite3
from werkzeug.security import generate_password_hash

class DB():
    def __init__(self):
        self.con = sqlite3.connect("DBase.db", check_same_thread=False)
        self.cur = self.con.cursor()

    # Создание таблиц
    def createTables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id_user INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL
            );
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Messages (
                id_addressee INTEGER,
                id_destination INTEGER,
                message TEXT
            );
        """)
        self.con.commit()

    # Работа с пользователями
    def addUser(self, login):
        self.cur.execute("INSERT INTO Users (login) VALUES (?);", (login,))
        self.con.commit()

    def getUser(self, id_user):
        return self.cur.execute("SELECT * FROM Users WHERE id_user=?", (id_user,)).fetchone()

    def getUserOnLogin(self, login):
        return self.cur.execute("SELECT * FROM Users WHERE login=?", (login,)).fetchone()

    def getUsers(self):
        return self.cur.execute("SELECT * FROM Users").fetchall()

    # Работа с сообщениями
    def addMessage(self, id_addressee, id_destination, message):
        self.cur.execute("INSERT INTO Messages (id_addressee, id_destination, message) VALUES (?, ?, ?);",
                         (id_addressee, id_destination, message))
        self.con.commit()

    def getChat(self, id_user1, id_user2):
        return self.cur.execute("""
            SELECT * FROM Messages 
            WHERE (id_addressee=? AND id_destination=?) OR (id_addressee=? AND id_destination=?)
            ORDER BY rowid ASC
        """, (id_user1, id_user2, id_user2, id_user1)).fetchall()

if __name__ == '__main__':
    db = DB()
    db.createTables()
