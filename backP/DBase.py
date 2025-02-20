import sqlite3
from werkzeug.security import generate_password_hash

class DB():
    def __init__(self):
        self.con = sqlite3.connect("DBase.db")
        self.cur = self.con.cursor()

    #<===================================USERS===================================>

    def createUsersTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Users (id_user INTEGER PRIMARY KEY autoincrement, login TEXT, password TEXT);")
        self.con.commit()

    def addUser(self, login, password):
        new_password=generate_password_hash(password)
        self.cur.execute("INSERT INTO Users (login, password) VALUES ( ?, ?);", (login, new_password))
        self.con.commit()

    def getUser(self, id_user):
        userData=self.cur.execute("SELECT * FROM Users WHERE id_user= ?", (id_user,)).fetchone()
        return userData

    def getUsers(self):
        usersData=self.cur.execute("SELECT * FROM Users").fetchall()
        return usersData

    def getUserOnLogin(self, login):
        userData=self.cur.execute("SELECT * FROM Users WHERE login= ?", (login,)).fetchone()
        return userData

    #<===================================MESSAGE_STORY===================================>

    def createMessageTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Messages (id_addressee INTEGER, id_destination TEXT, message TEXT);")
        self.con.commit()

    def addMessage(self, id_addressee, id_destination, message):
        self.cur.execute("INSERT INTO Messages (id_addressee, id_destination, message) VALUES (?,?,?);", (id_addressee, id_destination, message))
        self.con.commit()

    def getChat(self, id_user):
        messageData=self.cur.execute("SELECT * FROM Messages WHERE id_addressee= ? OR id_destination=?", (id_user,)).fetchall()
        return messageData

if __name__ == '__main__':
    DB().createUsersTable()
    DB().createMessageTable()