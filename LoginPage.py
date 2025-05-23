import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk  # For handling the background image
from tkinter import messagebox
import DButilities 
Db = DButilities.DButilities()
import hashlib
from PIL import ImageTk, Image
import MainPage

class LoginPage():
    def __init__(self, root, client):
        self.root = root
        self.client = client
        self.root.title("Login Page")
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

        # LOGIN Title
        self.login_label = tk.Label(
            self.root,
            text="Login",
            font=self.title_font,
            bg=None,
            fg="purple"
        )
        self.canvas.create_window(400, 50, window=self.login_label)

        # Username Label and Entry
        self.username_label = tk.Label(
            self.root,
            text="Username:",
            font=self.label_font,
            bg=None,
            fg="purple"
        )
        self.canvas.create_window(250, 200, window=self.username_label)

        self.username_entry = tk.Entry(
            self.root,
            font=self.label_font,
            bg="yellow",
            fg="black"
        )
        self.canvas.create_window(400, 200, window=self.username_entry, width=200)

        # Password Label and Entry
        self.password_label = tk.Label(
            self.root,
            text="Password:",
            font=self.label_font,
            bg=None,
            fg="purple"
        )
        self.canvas.create_window(250, 250, window=self.password_label)

        self.password_entry = tk.Entry(
            self.root,
            font=self.label_font,
            bg="yellow",
            fg="black",
            show="*"
        )
        self.canvas.create_window(400, 250, window=self.password_entry, width=200)

        # Login Button
        self.login_button = tk.Button(
            self.root,
            text="LOGIN",
            font=self.button_font,
            bg="#D8BFD8",
            fg="purple",
            padx=20,
            pady=10,
            command=self.check_credentials
        )
        self.canvas.create_window(400, 350, window=self.login_button)


        # Back Button
        self.back_button = tk.Button(
            self.root,
            text="Back",
            font=self.button_font,
            bg="#D8BFD8",
            fg="purple",
            padx=20,
            pady=10,
            command=self.back_action
        )
        self.canvas.create_window(400, 450, window=self.back_button)

        self.number_of_tries = 0

    

    def check_credentials(self):        
        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()
        hashed_pass = hashlib.sha256(entered_password.encode("utf-8")).hexdigest()


        if self.number_of_tries < 5:
            response = self.client.send_with_sync(
                "login",
                {
                    "username": entered_username,
                    "password": hashed_pass
                }
            )
            if response["status"] == "success":
                # Successful login
                self.username_user = entered_username
                self.id_user = response["id"]
                self.root.destroy()
                root = tk.Tk()
                MainPage.MainPage(root, self.client, self.username_user, self.id_user)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
                self.number_of_tries += 1
        else:
            messagebox.showerror("Login Failed", "You have exceeded the maximum number of login attempts. Your access has been denied.")
            self.clear_entries()
        
    
    def clear_entries(self):
        # Clear the username and password fields after successful login
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def back_action(self):
        self.root.destroy()
        root = tk.Tk()
        from HomePage import HomePage
        HomePage(root, self.client)



