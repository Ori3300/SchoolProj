import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import shutil

class RemoveBusinessPage:
    def __init__(self, root, client, username_user, id_user):
        self.client = client
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

        # Load businesses from server
        data = self.client.send_with_sync("fetch_database", {"name": "Businesses"})
        self.business_data = data
        self.businesses = [info["name"] for _, info in data.items() if info["owner_id"] == self.id_user]

        # UI Elements
        self.title_label = self.canvas.create_text(300, 30, text="REMOVE BUSINESS", font=("Arial", 16), fill="purple")
        self.list_label = self.canvas.create_text(300, 100, text=self.get_business_list(), font=("Arial", 12), fill="black")

        self.canvas.create_text(300, 180, text="Enter Business Name:", font=("Arial", 12), fill="black")
        self.entry = tk.Entry(root, font=("Arial", 12))
        self.canvas.create_window(300, 200, window=self.entry)

        self.remove_button = tk.Button(root, text="Remove", font=("Arial", 12), command=self.remove_business)
        self.canvas.create_window(300, 240, window=self.remove_button)

        self.return_button = tk.Button(root, text="Return", font=("Arial", 12), command=self.go_back)
        self.canvas.create_window(300, 280, window=self.return_button)

    def get_business_list(self):
        return "\n".join(f"{i+1}. {b}" for i, b in enumerate(self.businesses))

    def remove_business(self):
        name = self.entry.get().strip()
        if name not in self.businesses:
            messagebox.showerror("Error", "Business not found")
            return

        self.client.send_with_sync("remove_business", {"name": name, "owner_id": self.id_user})


        # Locate business ID
        business_id = None
        for b_id, b_info in self.business_data.items():
            if b_info["name"] == name and b_info["owner_id"] == self.id_user:
                business_id = b_id
                break

        if not business_id:
            messagebox.showerror("Error", "Business not found in database")
            return

        # Delete image folder
        folder_path = f"Pic\\business{business_id}_{name}"
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
        except Exception as e:
            print(f"Error removing image folder: {e}")

        

        

        self.businesses.remove(name)
        self.canvas.itemconfig(self.list_label, text=self.get_business_list())
        self.entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Business '{name}' removed successfully.")

    def go_back(self):
        from MainPage import MainPage
        self.root.destroy()
        root = tk.Tk()
        MainPage(root, self.client, self.username_user, self.id_user)
