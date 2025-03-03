import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import DButilities
Db = DButilities.DButilities()
#import HomePage
import AddBusinessPage

class MainPage:
    def __init__(self, root, username_user, id_user):
        self.username_user = username_user
        self.id_user = id_user
        self.root = root
        self.root.title("יד לעסק")
        self.root.geometry("900x600")

        # Load and display background image
        self.background_image = Image.open("Pic\\cool-background.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image.resize((900, 600)))
        
        self.canvas = tk.Canvas(self.root, width=900, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        
        # Fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold", underline=True)
        self.button_font = font.Font(family="Helvetica", size=12)
        self.label_font = font.Font(family="Helvetica", size=14, weight="bold")
        
        # Header title
        self.title_label = tk.Label(self.root, text="יד לעסק", font=self.title_font, fg="purple", bg=None)
        self.canvas.create_window(450, 40, window=self.title_label)
        
        # Logout button
        self.logout_button = tk.Button(self.root, text="log out", font=self.button_font, bg="lightgray", command=self.logout_action)
        self.canvas.create_window(100, 40, window=self.logout_button)
        
        # Add Business button
        self.add_business_button = tk.Button(self.root, text="add business", font=self.button_font, bg="lightgray", command=self.add_business_action)
        self.canvas.create_window(800, 40, window=self.add_business_button)

        self.show_all_businesses()
        
    def make_business_frame(self, business, x, y):
        # Business card frame
        self.business_frame = tk.Frame(self.root, bg="black", highlightbackground="black", highlightthickness=2)
        self.canvas.create_window(x, y, window=self.business_frame)
        
        # Load business image
        self.business_img = Image.open("Pic\\business1_Pizzaria\\ai_image.jpg")
        self.business_img = self.business_img.resize((600, 150))
        self.business_photo = ImageTk.PhotoImage(self.business_img)
        
        # Business image label
        self.img_label = tk.Label(self.business_frame, image=self.business_photo)
        self.img_label.pack()
        
        # Business name
        self.business_name = tk.Label(self.business_frame, text= business["name"], font=self.label_font, fg="black", bg="white")
        self.business_name.place(x=20, y=20)
        
        # Owner name
        self.owner_name = tk.Label(self.business_frame, text= business["owner_name"], font=self.button_font, fg="black", bg="white")
        self.owner_name.place(x=20, y=50)
            

    def show_all_businesses(self):
        data = Db.get_data("Businesses")
        businesses = [user_info for user_id, user_info in data.items()]
        x = 450
        y = 300
        for business in businesses:
            self.make_business_frame(business, x, y)
            x += 100
            y += 100
        

        

    def logout_action(self):
        pass
    #     self.root.destroy()
    #     root = tk.Tk()
    #     HomePage.HomePage(root)
    
    def add_business_action(self):
        self.root.destroy()
        root = tk.Tk()
        AddBusinessPage.AddBusinessPage(root, self.username_user, self.id_user)

