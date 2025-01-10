import DButilities 
Db = DButilities.DButilities()
import User

class Business:
    count = 0

    def __init__(self, name, category, description,owner_name ,owner_id, comments):
        Business.count += 1 
        self.__id = Business.count
        self.__name = name
        self.__description = description
        self.__category = category 
        self.__owner_name = owner_name
        self.__owner_id = owner_id
        if comments is not None:
            self.__comments = comments 
        else:
            self.__comments = []



    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_description(self):
        return self.__description
    def get_category(self):
        return self.__category
    def get_owner_name(self):
        return self.__owner_name
    def get_owner_id(self):
        return self.__owner_id
    def get_comments(self):
        return self.__comments
    
    def add_business_to_DB(self):
        Business = self.to_dict()
        data = Db.get_data(name="Businesses")
        data[len(data)+1] = Business
        Db.update_data(name="Businesses", data=data)
    def remove_business_from_DB(self):
        data = Db.get_data(name="Businesses")
        for id in list(data.keys()):
            if data[id]["id"] == self.__id:
                del data[id]
        Db.update_data(name="Businesses", data=data)

    def add_comment(self, comment):
        self.__comments.append(comment)
        comment.add_comment_to_DB()
    def remove_comment(self, comment):
        self.__comments.remove(comment)
        comment.remove_comment_from_DB()
    
    def to_dict(self):
        temp = list()
        for comment in self.__comments:
            temp.append(comment.get_id())
        return {
            "id": self.__id,
            "name": self.__name,
            "category": self.__category,
            "description": self.__description,
            "owner_name": self.__owner_name,
            "owner_id": self.__owner_id,
            "comments": temp
        }
    def __str__(self):
        return (
            f"Business(ID: {self.__id}, Name: {self.__name}, "
            f"Description: {self.__description}, Category: {self.__category}, "
            f"Owner: {self.__owner}, Comments: {self.__comments})"
        )






    

