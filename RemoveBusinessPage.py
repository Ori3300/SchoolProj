import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import DButilities
Db = DButilities.DButilities()
import os

class RemoveBusinessPage:
    def __init__(self, root, username_user, id_user):
        self.root = root
        self.root.title("Remove Business")
        self.root.geometry("600x400")
        self.username_user = username_user
        self.id_user = id_user

        # Load background image
        self.bg_image = Image.open("Pic\\cool-background.png")  
        self.bg_image = self.bg_image.resize((800, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        

        data = Db.get_data("Businesses")
        self.businesses = [business_info["name"] for business_id, business_info in data.items() if business_info["owner_id"] == self.id_user]
        print(self.businesses)

        

        # UI Elements on Canvas
        self.title_label = self.canvas.create_text(300, 30, text="REMOVE BUSINESS", font=("Arial", 16), fill="purple")
        self.list_label = self.canvas.create_text(300, 100, text=self.get_business_list(), font=("Arial", 12), fill="black")
        
        self.entry_label = self.canvas.create_text(300, 180, text="the name", font=("Arial", 12), fill="black")
        
        self.entry = tk.Entry(root, font=("Arial", 12))
        self.entry_window = self.canvas.create_window(300, 200, window=self.entry)

        self.remove_button = tk.Button(root, text="remove", font=("Arial", 12), command=self.remove_business)
        self.remove_button_window = self.canvas.create_window(300, 240, window=self.remove_button)

        self.return_button = tk.Button(root, text="Return", font=("Arial", 12), command=self.go_back)
        self.return_button_window = self.canvas.create_window(300, 280, window=self.return_button)
    
    def get_business_list(self):
        return "\n".join(f"{i+1}. {b}" for i, b in enumerate(self.businesses))

    def remove_business(self):
        name = self.entry.get().strip()
        if name in self.businesses:
            self.businesses.remove(name)
            self.canvas.itemconfig(self.list_label, text=self.get_business_list())
            self.entry.delete(0, tk.END)
            data = Db.get_data("Businesses")
            # Find business ID
            id = None
            for _, business_info in data.items():
                if business_info["name"] == name and business_info["owner_id"] == self.id_user:
                    id = str(business_info["id"])
                    break
            # Remove business image directory
            if os.path.exists(f"Pic\\business{id}_{name}\\ai_image.jpg"):
                os.remove(f"Pic\\business{id}_{name}\\ai_image.jpg")
                os.rmdir(f"Pic\\business{id}_{name}")
            # Remove business comments from database
            business_data = Db.get_data("Businesses")
            comments_id = None
            print("business_data", business_data)
            for business_id, business_info in business_data.items():
                if business_info["name"] == name and business_info["owner_id"] == self.id_user:
                    comments_id = business_info["comments"]
                    break
            print(comments_id)
            comments_data = Db.get_data("Comments")

            for comment_id in list(comments_data.keys()):
                if comments_data[comment_id]["id"] in comments_id:
                    del comments_data[comment_id]
            Db.update_data("Comments", comments_data)

            # for comment_id, comment_info in comments_data.items():
            #     if comment_info["id"] in comments_id:
            #         del comments_data[comment_id]
            # Db.update_data("Comments", comments_data)
            # Remove business from user's list
            user_data = Db.get_data("Users")
            for user_id, user_info in user_data.items():
                if user_info["id"] == self.id_user:
                    if int(id) in user_info["businesses"]:
                        user_info["businesses"].remove(int(id))
                        break
            Db.update_data("Users", user_data)
            # Remove business from database
            data = Db.get_data("Businesses")
            for _, business_info in data.items():
                if business_info["name"] == name and business_info["owner_id"] == self.id_user:
                    id = str(business_info["id"])
                    del data[id]
                    break
            Db.update_data("Businesses", data)
            # Show success message
            messagebox.showinfo("Success", f"Business '{name}' removed successfully.")
        else:
            messagebox.showerror("Error", "Business not found")
    
    def go_back(self):
        from MainPage import MainPage
        self.root.destroy()
        root = tk.Tk()
        MainPage(root, self.username_user, self.id_user)

