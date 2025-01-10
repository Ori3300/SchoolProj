import DButilities 
Db = DButilities.DButilities()

class Comment:
    count = 0

    def __init__(self,user_name, content):
        Comment.count += 1
        self.__id = Comment.count
        self.__username = user_name
        self.__content = content


    def get_id(self):
        return self.__id
    def get_username(self):
        return self.__username
    def get_content(self):
        return self.__content
    

    def add_comment_to_DB(self):
        comment = self.to_dict()
        data = Db.get_data(name="Comments")
        data[len(data)+1] = comment
        Db.update_data(name="Comments", data=data)
    def remove_comment_from_DB(self):
        data = Db.get_data(name="Comments")
        for id in list(data.keys()):
            if data[id]["id"] == self.__id:
                del data[id]
        Db.update_data(name="Comments", data=data)




    def to_dict(self):
        return {
            "id": self.__id,
            "username": self.__username,
            "content": self.__content
        }
    def __str__(self):
        return (
            f"Comment(ID: {self.__id}, Username: {self.__username}, "
            f"Content: {self.__content})"
        )

