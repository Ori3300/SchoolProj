import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk  # For handling the background image
from tkinter import messagebox
import DButilities 
Db = DButilities.DButilities()
import hashlib
import User


class SignUpPage():
    def __init__(self, root, client):
        self.client = client
        self.root = root
        self.root.title("Sign Up Page")
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

        # Sign-Up Title
        self.signup_label = tk.Label(
            self.root,
            text="Sign Up",
            font=self.title_font,
            bg=None,
            fg="purple"
        )
        self.canvas.create_window(400, 50, window=self.signup_label)

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

        # Sign-Up Button
        self.signup_button = tk.Button(
            self.root,
            text="Sign Up",
            font=self.button_font,
            bg="#D8BFD8",
            fg="purple",
            padx=20,
            pady=10,
            command=self.check_credentials
        )
        self.canvas.create_window(400, 350, window=self.signup_button)

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


        self.root.mainloop()



    def is_password_exist(self, hash_password):
        data = self.client.send_with_sync("fetch_database")["Users"]
        passwords = [user_info['password'] for user_id, user_info in data.items()]
        return hash_password in passwords


    def check_credentials(self):
        from LoginPage import LoginPage
        entered_username = self.username_entry.get().strip()
        entered_password = self.password_entry.get().strip()

        hash_password = hashlib.sha256(entered_password.encode("utf-8")).hexdigest()
        if not self.is_password_exist(hash_password):
            new_user = User.User(entered_username , hash_password, None)
            new_user.add_user_to_DB()

            # Send signup request to server
            response = self.client.send_with_sync(
                "signup",
                {
                    "username": entered_username,
                    "password": hash_password
                }
            )

            print(f"[Client] Sign Up Response: {response}")
            if response.get("status") == "success":
                messagebox.showinfo("Sign Up Success", "Successfully signed up!")
                self.root.destroy()
                root = tk.Tk()
                LoginPage(root, self.client)
            else:
                messagebox.showerror("Sign Up Failed", response.get("message", "Unknown error."))
                self.clear_entries()
                
        else:
            messagebox.showerror("Sign Up failed","Password is already exist")
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

        




