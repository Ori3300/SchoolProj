import DButilities 
Db = DButilities.DButilities()

class Comment:
    def __init__(self,user_name, content, client):
        self.__client = client
        last_comment_id = 0
        comment_data = self.__client.send_with_sync("fetch_database")["Comments"]
        for _, comment_info in comment_data.items():
            last_comment_id = comment_info["id"]
        self.__id = last_comment_id + 1
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
        last_comment_id = 0
        data = self.__client.send_with_sync("fetch_database")["Comments"]
        for comment_id, _ in data.items():
            last_comment_id = int(comment_id)
        data[last_comment_id+1] = comment
        Db.update_data(name="Comments", data=data)
    def remove_comment_from_DB(self):
        data = self.__client.send_with_sync("fetch_database")["Comments"]
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

