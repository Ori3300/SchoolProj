import json
import DButilities as DB

class DButilities:
    def __init__(self):
        pass
    


    def get_path(self, name):
        if name == "Users":
            full_path = "DBes\\Users.json"
        if name == "Businesses":
            full_path = "DBes\\businnesses.json"
        if name == "Comments":
            full_path = "DBes\\Comments.json"
        return full_path

    def get_data(self, name):
        path = self.get_path(name)
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    def update_data(self, name, data):
        path = self.get_path(name)
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)

    def show_DB(self, name):
        if name == "Users":
            data = self.get_data(name)
            for user_id, user_info in data.items():
                print(f"ID: {user_info['id']}, Username: {user_info['username']}, Password: {user_info['password']}, Businesses: {user_info['businesses']}")
        
        if name == "businesses":
            data = self.get_data(name)
            for user_id, user_info in data.items():
                print(f"ID: {user_info['id']}, Name: {user_info['name']},  Category: {user_info['category']}, Description: {user_info['description']}, Owner Name: {user_info['owner_name']}, Owner Id: {user_info['owner_id']}, comments: {user_info['comments']}")
        
        if name == "Comments":
            data = self.get_data(name)
            for user_id, user_info in data.items():
                print(f"ID: {user_info['id']}, Username: {user_info['username']}, Content: {user_info['content']}")