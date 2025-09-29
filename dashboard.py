from tkinter import *
from tkinter import messagebox  # Import messagebox for exit confirmation
from PIL import Image, ImageTk
from datetime import datetime
from employee import employeeclass
from kyc import KYCclass
from category import categoryclass
from product import productclass
from Billing import BillClass
from Billing import PackingSlipViewer
from Billing import PackingSlipManager

import sqlite3

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Textile Management System")
        self.root.config(bg="#f0f0f0")  # Light gray background

        # Make the window full screen
        self.root.attributes('-fullscreen', True)

        # Load and resize the image
        original_image = Image.open("icon__2_-removebg-preview.png")
        self.icon_title = ImageTk.PhotoImage(original_image.resize((50, 50)))

        # Title with an icon
        title = Label(
            self.root,
            text="SARAVANA FASHION",
            image=self.icon_title,
            compound=LEFT,
            font=("Helvetica", 40, "bold"),
            bg="#2C3E50",  # Darker blue
            fg="white",
            anchor="w",
            padx=20
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout button
        btn_logout = Button(
            self.root,
            command=self.exit_application,
            text="LOGOUT",
            font=("Helvetica", 12, "bold"),
            bg="#E74C3C",  # Red
            fg="white",
            cursor="hand2",
            relief=FLAT
        )
        btn_logout.place(x=1150, y=15, height=40, width=150)

        # Clock and Date
        self.lbl_clock = Label(
            self.root,
            text="",
            font=("Helvetica", 14),
            bg="#34495E",  # Dark blue
            fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)
        self.update_datetime()

        # Left menu
        self.MenuLogo = Image.open("left.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bg="#2C3E50", relief=FLAT)  # Darker blue
        LeftMenu.place(x=0, y=102, width=200, height=600)
        
        lbl_menulogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menulogo.pack(side=TOP, fill=X)

        # Menu label
        Label(LeftMenu, text="Menu", font=("Helvetica", 20), bg="#2C3E50", fg="white").pack(side=TOP, fill=X, pady=10)

        # Menu buttons
        menu_buttons = [
            ("EMPLOYEE", self.employee),
            ("KYC", self.kyc),
            ("CATEGORY", self.category),
            ("PRODUCT", self.product),
            ("BILLING", self.billing),
            
            
            
        ]

        for text, command in menu_buttons:
            Button(
                LeftMenu,
                text=text,
                command=command,
                font=("Helvetica", 15),
                bg="#34495E",
                fg="white",
                bd=0,
                cursor="hand2",
                activebackground="#2980B9",
                activeforeground="white",
                height=2
            ).pack(side=TOP, fill=X, pady=2, padx=5)

        # Dashboard Cards
        self.create_dashboard_cards()

        # Footer
        Label(
            self.root,
            text="Welcome To Saravana Fashion | Developed by Claviya",
            font=("Helvetica", 12),
            bg="#2C3E50",
            fg="white"
        ).pack(side=BOTTOM, fill=X)

        # Bind Escape key to exit full screen
        self.root.bind("<Escape>", self.toggle_fullscreen)

    def create_dashboard_cards(self):
        # Create frame for dashboard
        dashboard_frame = Frame(self.root, bg="#f0f0f0")
        dashboard_frame.place(x=220, y=120, width=1110, height=530)

        # Card style configuration
        card_width = 250  # Reduced width to accommodate 4 cards
        card_height = 150
        cards_data = [
            ("Total KYC", "#9B59B6", self.get_total_kyc),         # Purple
            ("Total Products", "#2ECC71", self.get_total_products),  # Green
            ("Total Bills", "#E67E22", self.get_total_bills),        # Orange
            ("Total Packing Slips", "#3498DB", self.get_total_slips) # Blue
        ]

        for i, (title, color, count_func) in enumerate(cards_data):
            x_pos = 20 + (i * (card_width + 20))
            
            card_frame = Frame(dashboard_frame, bg=color, relief=FLAT)
            card_frame.place(x=x_pos, y=20, width=card_width, height=card_height)
            
            Label(
                card_frame,
                text=title,
                font=("Helvetica", 20, "bold"),
                bg=color,
                fg="white"
            ).place(x=20, y=20)

            count = count_func()  # Get the count from database
            Label(
                card_frame,
                text=str(count),
                font=("Helvetica", 40, "bold"),
                bg=color,
                fg="white"
            ).place(x=20, y=60)

    def get_total_kyc(self):
        try:
            conn = sqlite3.connect('python\\ims.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM kyc")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0

    # ... [rest of the methods remain the same] ...

    def toggle_fullscreen(self, event=None):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def update_datetime(self):
        current_datetime = datetime.now().strftime("Date: %d-%m-%Y  |  Time: %H:%M:%S")
        self.lbl_clock.config(text=f"Welcome To Saravana Fashion  |  {current_datetime}")
        self.root.after(1000, self.update_datetime)

    def get_total_products(self):
        try:
            conn = sqlite3.connect('python\\ims.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM product")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0

    def get_total_bills(self):
        try:
            conn = sqlite3.connect('python\\ims.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM billing")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0

    def get_total_slips(self):
        try:
            conn = sqlite3.connect('python\\ims.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM packing_slip")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeclass(self.new_win)

    def kyc(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = KYCclass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryclass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productclass(self.new_win)

    def billing(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = BillClass(self.new_win)
    def bill(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = PackingSlipViewer(self.new_win)
    def login(self):
        
        self.new_win = Toplevel(self.root)
        self.new_obj = LuxuryLoginPage(self.new_win)
        

    def exit_application(self):
        
            self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()