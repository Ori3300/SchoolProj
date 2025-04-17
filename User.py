import DButilities 
Db = DButilities.DButilities()
import hashlib


class User:
    def __init__(self ,username, password, businesses):
        users_data = Db.get_data(name="Users")
        self.__id = len(users_data) + 1
        self.__username = username

        self.__password = password
        if businesses is not None:
            self.__businesses = businesses 
        else:
            self.__businesses = []

    def get_id(self):
        return self.__id
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    def get_businesses(self):
        return self.__businesses


    def add_user_to_DB(self):
        user = self.to_dict()
        data = Db.get_data(name="Users")
        data[len(data)+1] = user
        Db.update_data(name="Users", data=data)
    def remove_user_from_DB(self):
        data = Db.get_data(name="Users")
        for id in list(data.keys()):
            if data[id]["id"] == self.__id:
                del data[id]
        Db.update_data(name="Users", data=data)

    def add_business(self, business):
        self.__businesses.append(business)
        business.add_business_to_DB()
    def remove_business(self, business):
        self.__businesses.remove(business)   
        business.remove_business_from_DB() 


    




    def to_dict(self):
        temp = list()
        for business in self.__businesses:
            temp.append(business.get_id())        
        return{
            "id": self.__id,
            "username": self.__username,
            "password": self.__password,
            "businesses": temp
        }
    def __str__(self):
        return (
            f"User(ID: {self.__id}, Username: {self.__username}, "
            f"Businesses: {self.__businesses})"
        )
        


    

    
