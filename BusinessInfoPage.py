import tkinter as tk
from PIL import ImageTk
import DButilities
Db = DButilities.DButilities()
import Comment
from tkinter import messagebox
import requests

class BusinessInfoPage:
    def __init__(self, root, username_user, id_user, business, business_img):
        self.root = root
        self.root.title("Business Details")
        self.root.geometry("800x650")

        self.business = business   
        self.username_user = username_user
        self.id_user = id_user
        
        self.business_img = business_img
        self.business_img = self.business_img.resize((200, 150))
        self.business_photo = ImageTk.PhotoImage(self.business_img)


        
        # Business Name
        self.title_label = tk.Label(root, text=self.business["name"], font=("Arial", 20), fg="lightblue")
        self.title_label.pack(pady=10)
        
        # Back Button
        self.back_button = tk.Button(root, text="back", font=("Arial", 12), command=self.go_back)
        self.back_button.pack(pady=10)

        # category and Description
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=20)
        
        self.category_label = tk.Label(self.info_frame, text=f"category: {self.business["category"]}", font=("Arial", 14), fg="blue")
        self.category_label.grid(row=0, column=0, sticky="w", padx=20, pady=5)
        
        self.desc_label = tk.Label(self.info_frame, text=f"description: {self.business["description"]}", font=("Arial", 14), fg="blue")
        self.desc_label.grid(row=1, column=0, sticky="w", padx=20, pady=5)

        self.loc_label = tk.Label(self.info_frame, text=f"location: {self.business['location']}", font=("Arial", 14), fg="blue")
        self.loc_label.grid(row=2, column=0, sticky="w", padx=20, pady=5)

        # מזג אוויר
        weather_info = self.get_weather(self.business["location"])
        self.weather_label = tk.Label(self.info_frame, text=f"weather: {weather_info}", font=("Arial", 14), fg="blue")
        self.weather_label.grid(row=3, column=0, sticky="w", padx=20, pady=5)

        
        # Image Display
        self.image_label = tk.Label(self.info_frame, image=self.business_photo)
        self.image_label.grid(row=0, column=1, rowspan=2, padx=20)
        
        # Comments Section
        self.comments_label = tk.Label(root, text="comments section", font=("Arial", 18, "bold"))
        self.comments_label.pack(pady=10)

        # refresh comment Button
        self.refresh_comment_button = tk.Button(root, text="refresh", font=("Arial", 12), command=self.refresh_comment_action)
        self.refresh_comment_button.pack(pady=5)

        # Comments Entry Box
        self.comment_entry = tk.Entry(root, font=("Arial", 12), width=50)
        self.comment_entry.pack(pady=5)
        
        # Submit Comment Button
        self.submit_button = tk.Button(root, text="Submit Comment", font=("Arial", 12), command=self.submit_comment)
        self.submit_button.pack(pady=5)

        # Comments Display Box with Scrollbar
        self.comments_frame = tk.Frame(root)
        self.comments_frame.pack(pady=10)
        
        self.scrollbar = tk.Scrollbar(self.comments_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.comments_listbox = tk.Listbox(self.comments_frame, width=70, height=5, font=("Arial", 12), yscrollcommand=self.scrollbar.set)
        self.comments_listbox.pack()
        
        self.scrollbar.config(command=self.comments_listbox.yview)
        
        self.comments = []

        # Load existing comments from the database
        self.load_comments()

        
    
    def submit_comment(self):
        given_comment = self.comment_entry.get().strip()
        if given_comment:
            if len(given_comment) > 100:  # Limit comment length to 500 characters
                messagebox.showerror("Error", "Comment is too long! Max length is 500 characters.")
                return
            
            self.comments.append(given_comment)
            # Save comment to the database
            comment1 = Comment.Comment(self.username_user, content=given_comment)
            comment1.add_comment_to_DB()

            # Update the business' comments
            business_data = Db.get_data("Businesses")
            for _, business_info in business_data.items():
                if business_info["id"] == self.business["id"]:
                    business_info["comments"].append(comment1.get_id())
                    Db.update_data("Businesses", business_data)
                    break

            # Update the comments listbox
            listbox_content = f"{comment1.get_username()}: {comment1.get_content()}"
            self.comments_listbox.insert(tk.END, listbox_content)
            self.comment_entry.delete(0, tk.END)


            

    def load_comments(self):
        # Fetch comments from the database
        business_data = Db.get_data("Businesses")
        for _, Business_info in business_data.items():
            if Business_info["id"] == self.business["id"]:
                comments_id = Business_info["comments"]
                break
        comment_data = Db.get_data("Comments")
        self.comments = [comment_info for _, comment_info in comment_data.items() if comment_info["id"] in comments_id]
        # Display comments in the listbox
        for comment in self.comments:
            self.comments_listbox.insert(tk.END, f"{comment['username']}: {comment['content']}")
        
    
    def go_back(self):
        from MainPage import MainPage
        self.root.destroy()
        root = tk.Tk()
        MainPage(root, self.username_user, self.id_user)

    def refresh_comment_action(self):
        self.comments_listbox.delete(0, tk.END)  # Clear existing comments
        self.load_comments()  # Reload comments from the database


  

    def get_weather(self, city_name):
        api_key = "6e585d25ed0d9a950169e66253bdbdc5"  # שים כאן את המפתח האישי שלך מאתר OpenWeatherMap
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=en"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                return f"{desc}, {temp}°C"
            else:
                return "מזג האוויר לא זמין"
        except:
            return "שגיאה בשליפת תחזית"



