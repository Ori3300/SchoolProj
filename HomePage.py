import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk 
import SignUpPage
import LoginPage


class HomePage():
    def __init__(self, root, client):
        self.root = root
        self.client = client
        self.root.title("Home Page")
        self.root.geometry("800x600")

        # Load and display background image
        self.background_image = Image.open("Pic\\cool-background.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((800, 600)))

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=14)

        # Welcome Message
        self.welcome_label = tk.Label(
            self.root,
            text="Welcome To \"יד לעסק\"",
            font=self.title_font,
            bg=None,
            fg="black"
        )
        self.canvas.create_window(400, 100, window=self.welcome_label)

        # Buttons
        self.sign_up_button = tk.Button(
            self.root,
            text="Sign Up",
            font=self.button_font,
            bg="#D8BFD8",
            fg="black",
            padx=20,
            pady=10,
            command=self.show_signup_page
        )
        self.canvas.create_window(300, 300, window=self.sign_up_button)

        self.login_button = tk.Button(
            self.root,
            text="Login",
            font=self.button_font,
            bg="#D8BFD8",
            fg="black",
            padx=20,
            pady=10,
            command=self.show_login_page
        )
        self.canvas.create_window(500, 300, window=self.login_button)

    def show_signup_page(self):
        self.root.destroy()
        root = tk.Tk()
        SignUpPage.SignUpPage(root, self.client)

    def show_login_page(self):
        self.root.destroy()
        root = tk.Tk()
        LoginPage.LoginPage(root, self.client)
