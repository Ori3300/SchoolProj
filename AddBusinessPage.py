import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk  # For handling the background image
import DButilities 
Db = DButilities.DButilities()
import Business
import MainPage


class AddBusinessPage:
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

    def add_action(self):
        business_name = self.business_name_entry.get()
        category = self.category_entry.get()
        description = self.description_entry.get()


        business1 = Business.Business(business_name, category, description, self.username_user, self.id_user, None)
        business1.add_business_to_DB()

        self.root.destroy()
        root = tk.Tk()
        MainPage.MainPage(root, self.username_user, self.id_user)
        
        



