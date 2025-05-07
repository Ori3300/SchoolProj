import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk  
import DButilities 
Db = DButilities.DButilities()
import Business
import MainPage
from tkinter import messagebox


class AddBusinessPage():
    def __init__(self, root, username_user, id_user):
        self.username_user = username_user
        self.id_user = id_user

        self.root = root
        self.root.title("Add Business Page")
        self.root.geometry("800x600")

        # Load and display background image
        self.background_image = Image.open("Pic\\cool-background.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((800, 600)))

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=14)

        # Add Business Title
        self.title_label = tk.Label(
            self.root,
            text="Add Business",
            font=self.title_font,
            bg=None,
            fg="purple"
        )
        self.canvas.create_window(400, 50, window=self.title_label)

        # Business Name Label and Entry
        self.business_name_label = tk.Label(
            self.root,
            text="Business Name:",
            font=self.label_font,
            bg=None,
            fg="purple"
        )
        self.canvas.create_window(200, 150, window=self.business_name_label)

        self.business_name_entry = tk.Entry(self.root, font=self.label_font, bg="yellow")
        self.canvas.create_window(400, 150, window=self.business_name_entry)

        # Category Label and Entry
        self.category_label = tk.Label(
            self.root,
            text="Category:",
            font=self.label_font,
            bg=None,
            fg="purple"
        )
        self.canvas.create_window(200, 200, window=self.category_label)

        self.category_entry = tk.Entry(self.root, font=self.label_font, bg="yellow")
        self.canvas.create_window(400, 200, window=self.category_entry)

        # Description Label and Entry
        self.description_label = tk.Label(
            self.root,
            text="Description:",
            font=self.label_font,
            bg=None,
            fg="purple"
        )
        self.canvas.create_window(200, 250, window=self.description_label)

        self.description_entry = tk.Entry(self.root, font=self.label_font, bg="yellow")
        self.canvas.create_window(400, 250, window=self.description_entry)

        # Location Label and Entry
        self.location_label = tk.Label(
            self.root,
            text="Location:",
            font=self.label_font,
            bg=None,
            fg="purple"
        )
        self.canvas.create_window(200, 300, window=self.location_label)

        self.location_entry = tk.Entry(self.root, font=self.label_font, bg="yellow")
        self.canvas.create_window(400, 300, window=self.location_entry)

        # Add Button
        self.add_button = tk.Button(
            self.root,
            text="Add",
            font=self.button_font,
            bg="#D8BFD8",
            fg="purple",
            padx=20,
            pady=10,
            command=self.add_action
        )
        self.canvas.create_window(400, 350, window=self.add_button)

        # Return Button
        self.return_button = tk.Button(
            self.root,
            text="Back",
            font=self.button_font,
            bg="#D8BFD8",
            fg="purple",
            padx=20,
            pady=10,
            command=self.go_back
        )
        self.canvas.create_window(400, 450, window=self.return_button)

    def add_action(self):
        business_name = self.business_name_entry.get().strip()
        category = self.category_entry.get().strip()
        description = self.description_entry.get().strip()
        location = self.location_entry.get().strip()


        business1 = Business.Business(business_name, category, description, location ,self.username_user, self.id_user, None)
        business1.add_business_to_DB()

        user_data = Db.get_data("Users")
        for _ , user_info in user_data.items():
            if user_info["id"] == self.id_user:
                user_info["businesses"].append(business1.get_id())
                break
        Db.update_data("Users", user_data)
        
        
        messagebox.showinfo("success", "business added successfully")

        self.root.destroy()
        root = tk.Tk()
        MainPage.MainPage(root, self.username_user, self.id_user)
        

    def go_back(self):
        from MainPage import MainPage
        self.root.destroy()
        root = tk.Tk()
        MainPage(root, self.username_user, self.id_user)
        



