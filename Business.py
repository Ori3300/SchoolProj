import DButilities 
Db = DButilities.DButilities()
import User
import requests
from PIL import Image
from io import BytesIO
import os

class Business:
    def __init__(self, name, category, description, location, owner_name ,owner_id, comments):
        last_business_id = 0
        business_data = Db.get_data(name="Businesses")
        for _, business_info in business_data.items():
            last_business_id = business_info["id"]

        self.__id = last_business_id + 1 
        self.__name = name
        self.__description = description
        self.__category = category 
        self.__location = location
        self.__owner_name = owner_name
        self.__owner_id = owner_id
        if comments is not None:
            self.__comments = comments 
        else:
            self.__comments = []

        self.generate_ai_image()



    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_description(self):
        return self.__description
    def get_category(self):
        return self.__category
    def get_location(self):
        return self.__location
    def get_owner_name(self):
        return self.__owner_name
    def get_owner_id(self):
        return self.__owner_id
    def get_comments(self):
        return self.__comments
    
    def generate_ai_image(self):
       # Image details
        prompt = self.__category
        width = 1024
        height = 1024
        seed = 1 # Each seed generates a new image variation
        model = 'flux' # Using 'flux' as default if model is not provided

        image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
    
        self.download_image(image_url)
    def download_image(self, image_url):
        # Fetching the image from the URL
        response = requests.get(image_url)
        # Writing the content to a file named 'image.jpg'
        directory = f'Pic\\business{self.__id}_{self.__name}'
        os.makedirs(directory, exist_ok=True)
        file_path = f"{directory}\\ai_image.jpg"


        with open(file_path, 'wb') as file:
            file.write(response.content)
        # Logging completion message
        print('Download Completed')


    def add_business_to_DB(self):
        Business = self.to_dict()
        last_business_id = 0
        data = Db.get_data(name="Businesses")
        for Business_id, _ in data.items():
            last_business_id = int(Business_id)
        data[last_business_id+1] = Business
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
            "location": self.__location,
            "owner_name": self.__owner_name,
            "owner_id": self.__owner_id,
            "comments": temp
        }






    

