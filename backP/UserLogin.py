class UserLogin():
    def fromDB(self, id_user, DB):
        self.__user = DB.getUser(id_user)
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonnymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])

    def get_user(self):
        return self.__user

    def createUser(self, user):
        self.__user = user
        return self