import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox
import requests
import Comment

class BusinessInfoPage:
    def __init__(self, root, username_user, id_user, business, business_img, client):
        self.root = root
        self.root.title("Business Details")
        self.root.geometry("800x650")

        self.business = business   
        self.username_user = username_user
        self.id_user = id_user
        self.client = client
        self.business_img = business_img.resize((200, 150))
        self.business_photo = ImageTk.PhotoImage(self.business_img)

        # Business Name
        self.title_label = tk.Label(root, text=self.business["name"], font=("Arial", 20), fg="lightblue")
        self.title_label.pack(pady=10)

        # Back Button
        self.back_button = tk.Button(root, text="Back", font=("Arial", 12), command=self.go_back)
        self.back_button.pack(pady=10)

        # Info Frame
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=20)

        self.category_label = tk.Label(self.info_frame, text=f"Category: {self.business['category']}", font=("Arial", 14), fg="blue")
        self.category_label.grid(row=0, column=0, sticky="w", padx=20, pady=5)

        self.desc_label = tk.Label(self.info_frame, text=f"Description: {self.business['description']}", font=("Arial", 14), fg="blue")
        self.desc_label.grid(row=1, column=0, sticky="w", padx=20, pady=5)

        self.loc_label = tk.Label(self.info_frame, text=f"Location: {self.business['location']}", font=("Arial", 14), fg="blue")
        self.loc_label.grid(row=2, column=0, sticky="w", padx=20, pady=5)

        # Weather
        weather_info = self.get_weather(self.business['location'])
        self.weather_label = tk.Label(self.info_frame, text=f"Weather: {weather_info}", font=("Arial", 14), fg="blue")
        self.weather_label.grid(row=3, column=0, sticky="w", padx=20, pady=5)

        # Image
        self.image_label = tk.Label(self.info_frame, image=self.business_photo)
        self.image_label.grid(row=0, column=1, rowspan=2, padx=20)

        # Comments Title
        self.comments_label = tk.Label(root, text="Comments Section", font=("Arial", 18, "bold"))
        self.comments_label.pack(pady=10)

        # Refresh Comments
        self.refresh_comment_button = tk.Button(root, text="Refresh", font=("Arial", 12), command=self.refresh_comment_action)
        self.refresh_comment_button.pack(pady=5)

        # Entry for new comment
        self.comment_entry = tk.Entry(root, font=("Arial", 12), width=50)
        self.comment_entry.pack(pady=5)

        # Submit Button
        self.submit_button = tk.Button(root, text="Submit Comment", font=("Arial", 12), command=self.submit_comment)
        self.submit_button.pack(pady=5)

        # Comments display list
        self.comments_frame = tk.Frame(root)
        self.comments_frame.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.comments_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.comments_listbox = tk.Listbox(self.comments_frame, width=70, height=5, font=("Arial", 12), yscrollcommand=self.scrollbar.set)
        self.comments_listbox.pack()

        self.scrollbar.config(command=self.comments_listbox.yview)

        self.comments = []

        # Load existing comments from the server
        self.load_comments()

    def submit_comment(self):
        given_comment = self.comment_entry.get().strip()
        if given_comment:
            if len(given_comment) > 500:
                messagebox.showerror("Error", "Comment is too long! Max 500 characters.")
                return

            # Create Comment and add to DB
            comment1 = Comment.Comment(self.username_user, content=given_comment, client=self.client)
            comment1.add_comment_to_DB()

            # Update Businesses table
            business_data = self.client.send_with_sync("fetch_database", {"name": "Businesses"})
            for _, business_info in business_data.items():
                if business_info['id'] == self.business['id']:
                    if comment1.get_id() not in business_info['comments']:
                        business_info['comments'].append(comment1.get_id())
                    break
            self.client.send_with_sync(["UPDATE", "Businesses", business_data])

            # Update UI
            listbox_content = f"{comment1.get_username()}: {comment1.get_content()}"
            self.comments_listbox.insert(tk.END, listbox_content)
            self.comment_entry.delete(0, tk.END)

    def load_comments(self):
        self.comments_listbox.delete(0, tk.END)

        business_data = self.client.send_with_sync("fetch_database", {"name": "Businesses"})
        comments_id = []
        print(f"")
        for _, business_info in business_data.items():
            print(f"business_info type: {type(business_info)}")
            print(f"self.business type: {type(self.business)}")
            if business_info["id"] == self.business["id"]:
                comments_id = business_info["comments"]
                break

        comment_data = self.client.send_with_sync("fetch_database", {"name": "Comments"})
        self.comments = [comment_info for _, comment_info in comment_data.items() if comment_info["id"] in comments_id]

        for comment in self.comments:
            self.comments_listbox.insert(tk.END, f"{comment['username']}: {comment['content']}")

    def go_back(self):
        from MainPage import MainPage
        self.root.destroy()
        root = tk.Tk()
        MainPage(root, self.username_user, self.id_user, self.client)

    def refresh_comment_action(self):
        self.load_comments()

    def get_weather(self, city_name):
        api_key = "6e585d25ed0d9a950169e66253bdbdc5"
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=en"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                return f"{desc}, {temp}°C"
            else:
                return "Weather unavailable"
        except:
            return "Weather fetch error"
