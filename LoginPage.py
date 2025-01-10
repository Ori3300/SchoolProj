import tkinter as tk
from tkinter import messagebox

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("600x400")
        
        # Username label and entry
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        
        # Password label and entry
        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        # Login button
        self.login_button = tk.Button(self.root, text="Login", command=self.check_credentials)
        self.login_button.pack(pady=20)
    
    def check_credentials(self):
        # Hardcoded username and password for demonstration
        correct_username = "admin"
        correct_password = "password123"
        
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()
        
        # Check if the entered credentials are correct
        if entered_username == correct_username and entered_password == correct_password:
            messagebox.showinfo("Login Success", "Welcome to the system!")
            self.clear_entries()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    
    def clear_entries(self):
        # Clear the username and password fields after successful login
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

# Creating the Tkinter window
root = tk.Tk()
login_page = LoginPage(root)
root.mainloop()
