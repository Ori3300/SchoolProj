import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import base64


class MainPage:
    def __init__(self, root, client, username_user, id_user):
        self.client = client
        self.username_user = username_user
        self.id_user = id_user
        self.root = root
        self.root.title("יד לעסק")
        self.root.geometry("900x600")

        self.images = []

        # Main Frame (holds everything)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Canvas (for scrolling)
        self.canvas = tk.Canvas(self.main_frame, width=900, height=600)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)

        # Scrollable Frame inside Canvas
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=900)

        # Configure scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold", underline=True)
        self.button_font = font.Font(family="Helvetica", size=12)
        self.label_font = font.Font(family="Helvetica", size=14, weight="bold")

        # Header title
        self.title_label = tk.Label(self.scrollable_frame, text="יד לעסק", font=self.title_font, fg="purple", bg="white")
        self.title_label.pack(pady=10)

        self.welcome_label = tk.Label(self.scrollable_frame, text=f"welcome: {self.username_user}", font=self.label_font, fg="purple", bg="white")
        self.welcome_label.pack(pady=10)

        # Buttons
        self.logout_button = tk.Button(self.scrollable_frame, text="log out", font=self.button_font, bg="lightgray", command=self.logout_action)
        self.logout_button.pack(pady=10)

        self.add_business_button = tk.Button(self.scrollable_frame, text="add business", font=self.button_font, bg="lightgray", command=self.add_business_action)
        self.add_business_button.pack(pady=10)

        self.remove_business_button = tk.Button(self.scrollable_frame, text="remove business", font=self.button_font, bg="lightgray", command=self.remove_business_action)
        self.remove_business_button.pack(pady=10)

        self.refresh_button = tk.Button(self.scrollable_frame, text="refresh", font=self.button_font, bg="lightgray", command=self.refresh_action)
        self.refresh_button.pack(pady=10)

        # Load and show all businesses
        self.show_all_businesses()

        # Enable mouse scrolling
        self.root.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def show_all_businesses(self):
        """Fetch and display all businesses."""
        try:
            response = self.client.send_with_sync("fetch_database")["Businesses"]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load businesses: {e}")
            return

        businesses = [info for _, info in response.items()]
        if not businesses:
            self.scrollable_frame.config(height=600)
        else:
            for business in businesses:
                self.make_business_frame(business)

        self.root.after(100, lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def make_business_frame(self, business):
        """Create a visual block for a single business."""
        business_frame = tk.Frame(self.scrollable_frame, bg="white", width=620, height=300, highlightbackground="black", highlightthickness=2)
        business_frame.pack(pady=10)

        # Load business image
        image_path = f"Pic\\business{business['id']}_{business['name']}\\ai_image.jpg"
        if os.path.exists(image_path):
            business_img = Image.open(image_path)
        else:
            business_img_b64 = business["img_b64"]
            business_img = base64.b64decode(business_img_b64)
            directory = f'Pic\\business{business['id']}_{business['name']}'
            os.makedirs(directory, exist_ok=True)
            with open(f"Pic\\business{business['id']}_{business['name']}\\ai_image.jpg", "wb") as image_file:
                image_file.write(base64.b64decode(business_img))
            business_img = Image.open(image_path)

        business_img = business_img.resize((600, 150))
        business_photo = ImageTk.PhotoImage(business_img)
        self.images.append(business_photo)

        img_label = tk.Label(business_frame, image=business_photo)
        img_label.pack()

        business_name = tk.Label(business_frame, text=business["name"], font=self.label_font, fg="black", bg="white")
        business_name.pack()

        owner_name = tk.Label(business_frame, text=f"Owner: {business['owner_name']}", font=self.button_font, fg="black", bg="white")
        owner_name.pack()

        business_info_button = tk.Button(business_frame, text="Business Info", font=self.button_font, bg="lightgray", command=lambda: self.business_button(business, business_img))
        business_info_button.pack()

    def logout_action(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if confirm:
            self.root.destroy()
            from HomePage import HomePage
            root = tk.Tk()
            HomePage(root, self.client)

    def add_business_action(self):
        from AddBusinessPage import AddBusinessPage
        self.root.destroy()
        root = tk.Tk()
        AddBusinessPage(root, self.client, self.username_user, self.id_user)

    def remove_business_action(self):
        from RemoveBusinessPage import RemoveBusinessPage
        self.root.destroy()
        root = tk.Tk()
        RemoveBusinessPage(root, self.client, self.username_user, self.id_user)

    def business_button(self, business, business_img):
        from BusinessInfoPage import BusinessInfoPage
        self.root.destroy()
        root = tk.Tk()
        BusinessInfoPage(root, self.client, self.username_user, self.id_user, business, business_img)

    def refresh_action(self):
        self.root.destroy()
        root = tk.Tk()
        MainPage(root, self.client, self.username_user, self.id_user)
