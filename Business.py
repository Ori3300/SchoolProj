import requests
import os
import base64

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
        self.__img_b64     = None

        # 2) Generate & save the AI image on disk immediately
        self._download_and_encode_image()

    def get_id(self):        return self.__id
    def get_name(self):      return self.__name
    def get_category(self):  return self.__category
    def get_description(self): return self.__description
    def get_location(self):  return self.__location
    def get_owner_name(self):return self.__owner_name
    def get_owner_id(self):  return self.__owner_id
    def get_comments(self):  return list(self.__comments)
    def get_img_b64(self):   return self.__img_b64

    def _download_and_encode_image(self):
        # Download AI‑generated image
        prompt = self.__category
        url = f"https://pollinations.ai/p/{prompt}?width=1024&height=1024&seed=1&model=flux"
        resp = requests.get(url)
        directory = f"Pic/business{self.__id}_{self.__name}"
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, "ai_image.jpg")
        with open(path, "wb") as f:
            f.write(resp.content)

        # Encode to base64 for JSON transport
        with open(path, "rb") as f:
            self.__img_b64 = base64.b64encode(f.read()).decode("utf-8")

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
            "img_b64":      self.__img_b64,
            "comments":     self.__comments
        }

    def add_business_to_DB(self):
        """Tell the server to add this business."""
        payload = self.to_dict()
        response = self._client.send_with_sync("add_business", payload)
        if not response or response.get("status") != "success":
            raise RuntimeError(f"Failed to add business: {response}")

    def remove_business_from_DB(self):
        """Tell the server to remove this business by name & owner."""
        payload = {"name": self.__name, "owner_id": self.__owner_id}
        response = self._client.send_with_sync("remove_business", payload)
        if not response or response.get("status") != "success":
            raise RuntimeError(f"Failed to remove business: {response}")

    def add_comment(self, comment):
        """Attach a Comment object to this business."""
        self.__comments.append(comment.get_id())
        payload = {
            "username":    comment.get_username(),
            "content":     comment.get_content(),
            "business_id": self.__id
        }
        response = self._client.send_with_sync("add_comment", payload)
        if not response or response.get("status") != "success":
            raise RuntimeError(f"Failed to add comment: {response}")

    def remove_comment(self, comment_id):
        """Remove a comment by its ID."""
        # Server side: you would need a 'remove_comment' route to implement this
        payload = {"id": comment_id}
        response = self._client.send_with_sync("remove_comment", payload)
        if not response or response.get("status") != "success":
            raise RuntimeError(f"Failed to remove comment: {response}")
        self.__comments.remove(comment_id)
