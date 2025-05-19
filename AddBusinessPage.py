import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from tkinter import messagebox
import Business
import MainPage

class AddBusinessPage:
    def __init__(self, root, client, username_user, id_user):
        self.client = client
        self.username_user = username_user
        self.id_user = id_user

        self.root = root
        self.root.title("Add Business Page")
        self.root.geometry("800x600")

        # Background
        self.background_image = Image.open("Pic\\cool-background.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((800, 600)))

        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=14)

        # Title
        self.title_label = tk.Label(self.root, text="Add Business", font=self.title_font, fg="purple", bg=None)
        self.canvas.create_window(400, 50, window=self.title_label)

        # Fields
        self._add_label_entry("Business Name:", 150)
        self.business_name_entry = self._last_entry

        self._add_label_entry("Category:", 200)
        self.category_entry = self._last_entry

        self._add_label_entry("Description:", 250)
        self.description_entry = self._last_entry

        self._add_label_entry("Location:", 300)
        self.location_entry = self._last_entry

        # Buttons
        self.add_button = tk.Button(self.root, text="Add", font=self.button_font, bg="#D8BFD8", fg="purple", padx=20, pady=10, command=self.add_action)
        self.canvas.create_window(400, 350, window=self.add_button)

        self.return_button = tk.Button(self.root, text="Back", font=self.button_font, bg="#D8BFD8", fg="purple", padx=20, pady=10, command=self.go_back)
        self.canvas.create_window(400, 450, window=self.return_button)

    def _add_label_entry(self, label_text, y):
        label = tk.Label(self.root, text=label_text, font=self.label_font, fg="purple", bg=None)
        self.canvas.create_window(200, y, window=label)

        entry = tk.Entry(self.root, font=self.label_font, bg="yellow")
        self.canvas.create_window(400, y, window=entry)

        self._last_entry = entry

    def add_action(self):
        business_name = self.business_name_entry.get().strip()
        category = self.category_entry.get().strip()
        description = self.description_entry.get().strip()
        location = self.location_entry.get().strip()

        if not all([business_name, category, description, location]):
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        business = Business.Business(
            business_name, category, description, location,
            self.username_user, self.id_user, None, self.client
        )

        # Add business to DB via server
        try:
            # Add the business
            self.client.send_with_sync(
                "add_business",
                business.to_dict()
            )

            # Update user's business list
            # users_data  = self.client.send_with_sync("fetch_database")["Users"]
            # for _, user_info in users_data.items():
            #     if user_info["id"] == self.id_user:
            #         user_info["businesses"].append(business.get_id())
            #         break

            # self.client.send_with_sync(
            #     "update_data",
            #     {"name": "Users",
            #     "data": users_data}
            # )

            messagebox.showinfo("Success", "Business added successfully.")

            self.root.destroy()
            root = tk.Tk()
            MainPage.MainPage(root, self.client, self.username_user, self.id_user)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add business: {e}")

    def go_back(self):
        self.root.destroy()
        root = tk.Tk()
        MainPage.MainPage(root, self.client, self.username_user, self.id_user)
