import requests
import os


class Business:
    def __init__(self, name, category, description, location,
                 owner_name, owner_id, comments, client):
        self._client = client

        # 1) Fetch current Businesses to determine next ID
        businesses = self._client.send_with_sync("fetch_database", {"name": "Businesses"})
        max_id = max((int(b["id"]) for b in businesses.values()), default=0)
        self.__id = max_id + 1

        self.__name        = name
        self.__category    = category
        self.__description = description
        self.__location    = location
        self.__owner_name  = owner_name
        self.__owner_id    = owner_id
        self.__comments    = comments or []
        self.__img_url = f"https://pollinations.ai/p/{self.__category}?width=1024&height=1024&seed=1&model=flux"


    def get_id(self):        return self.__id
    def get_name(self):      return self.__name
    def get_category(self):  return self.__category
    def get_description(self): return self.__description
    def get_location(self):  return self.__location
    def get_owner_name(self):return self.__owner_name
    def get_owner_id(self):  return self.__owner_id
    def get_comments(self):  return list(self.__comments)
    def get_img_b64(self):   return self.__img_b64



    def to_dict(self):
        """Return exactly the shape the server's add_business route expects."""
        return {
            "id":           self.__id,
            "name":         self.__name,
            "category":     self.__category,
            "description":  self.__description,
            "location":     self.__location,
            "owner_name":   self.__owner_name,
            "owner_id":     self.__owner_id,
            "img_url":      self.__img_url,
            "comments":     self.__comments
        }

  