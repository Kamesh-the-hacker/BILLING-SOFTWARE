import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import sqlite3
from tkinter import *
from tkinter import messagebox  # Import messagebox for exit confirmation
from PIL import Image, ImageTk

# Import all necessary classes and modules
from employee import employeeclass
from kyc import KYCclass
from category import categoryclass
from product import productclass
from Billing import BillClass, PackingSlipViewer, PackingSlipManager

class LuxuryLoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Saravana Fashion")
        self.root.geometry("800x600")
        self.root.configure(bg='#FFFFFF')
        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)

        # Default credentials
        self.default_username = "admin"
        self.default_password = "12345"
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg='#FFFFFF')
        self.main_frame.pack(expand=True, fill='both', padx=50, pady=30)
        
        # Welcome Label
        self.welcome_label = tk.Label(
            self.main_frame,
            text="Welcome \n Saravana Fashion",
            font=("Helvetica", 24, "bold"),
            bg='#FFFFFF',
            fg='#1A1A1A'
        )
        self.welcome_label.pack(pady=20)
        
        # Login Frame
        self.login_frame = tk.Frame(self.main_frame, bg='#FFFFFF')
        self.login_frame.pack(pady=20)
        
        # Username
        self.username_label = tk.Label(
            self.login_frame,
            text="Username",
            font=("Helvetica", 12),
            bg='#FFFFFF',
            fg='#1A1A1A'
        )
        self.username_label.pack(anchor='w')
        
        self.username_entry = tk.Entry(
            self.login_frame,
            font=("Helvetica", 12),
            width=30,
            relief='solid'
        )
        self.username_entry.pack(pady=5)
        self.username_entry.insert(0, "admin")  # Pre-fill admin username
        
        # Password
        self.password_label = tk.Label(
            self.login_frame,
            text="Password",
            font=("Helvetica", 12),
            bg='#FFFFFF',
            fg='#1A1A1A'
        )
        self.password_label.pack(anchor='w')
        
        self.password_entry = tk.Entry(
            self.login_frame,
            font=("Helvetica", 12),
            width=30,
            show="•",
            relief='solid'
        )
        self.password_entry.pack(pady=5)
        
        # Login Button
        self.login_button = tk.Button(
            self.login_frame,
            text="Login",
            font=("Helvetica", 12, "bold"),
            bg='#1A1A1A',
            fg='#FFFFFF',
            width=20,
            command=self.login
        )
        self.login_button.pack(pady=20)

        self.exit = tk.Button(
            self.login_frame,
            command=self.exit_application,
            text="Exit",
            font=("Helvetica", 12, "bold"),
            bg='#1A1A1A',
            fg='#FFFFFF',
            width=20)
        self.exit.pack(pady=40)           
        
        # Forgot Password Link
        self.forgot_password = tk.Label(
            self.login_frame,
            text="Forgot Password?",
            font=("Helvetica", 10, "underline"),
            bg='#FFFFFF',
            fg='#666666',
            cursor="hand2"
        )
        self.forgot_password.pack()
        self.forgot_password.bind("<Button-1>", self.forgot_password_clicked)

        # Created by text
        self.created_by = tk.Label(
            self.main_frame,
            text=f"Created by Kamesh © {datetime.now().year}",
            font=("Helvetica", 8),
            bg='#FFFFFF',
            fg='#999999'
        )
        self.created_by.pack(side='bottom', pady=10)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if username == self.default_username and password == self.default_password:
            self.root.withdraw()  # Hide the login window
            self.open_dashboard()  # Open the dashboard
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def open_dashboard(self):
        dashboard_window = tk.Toplevel(self.root)
        dashboard = IMS(dashboard_window)
        
    def forgot_password_clicked(self, event):
        ForgotPasswordWindow(self.root, self.default_username, self.default_password)

    def exit_application(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self.root.destroy()
    def bind_enter_key(self):
        self.root.bind('<Return>', lambda event: self.login())

# The ForgotPasswordWindow class remains unchanged

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
        title = tk.Label(
            self.root,
            text="SARAVANA FASHION",
            image=self.icon_title,
            compound=tk.LEFT,
            font=("Helvetica", 40, "bold"),
            bg="#2C3E50",  # Darker blue
            fg="white",
            anchor="w",
            padx=20
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        # Logout button
        btn_logout = tk.Button(
            self.root,
            command=self.exit_application,
            text="LOGOUT",
            font=("Helvetica", 12, "bold"),
            bg="#E74C3C",  # Red
            fg="white",
            cursor="hand2",
            relief=tk.FLAT
        )
        btn_logout.place(x=1150, y=15, height=40, width=150)

        # Clock and Date
        self.lbl_clock = tk.Label(
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

        LeftMenu = tk.Frame(self.root, bg="#2C3E50", relief=tk.FLAT)  # Darker blue
        LeftMenu.place(x=0, y=102, width=200, height=600)
        
        lbl_menulogo = tk.Label(LeftMenu, image=self.MenuLogo)
        lbl_menulogo.pack(side=tk.TOP, fill=tk.X)

        # Menu label
        tk.Label(LeftMenu, text="Menu", font=("Helvetica", 20), bg="#2C3E50", fg="white").pack(side=tk.TOP, fill=tk.X, pady=10)

        # Menu buttons
        menu_buttons = [
            ("EMPLOYEE", self.employee),
            ("KYC", self.kyc),
            ("CATEGORY", self.category),
            ("PRODUCT", self.product),
            ("BILLING", self.billing),
        ]

        for text, command in menu_buttons:
            tk.Button(
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
            ).pack(side=tk.TOP, fill=tk.X, pady=2, padx=5)

        # Dashboard Cards
        self.create_dashboard_cards()

        # Footer
        tk.Label(
            self.root,
            text="Welcome To Saravana Fashion | Developed by Claviya",
            font=("Helvetica", 12),
            bg="#2C3E50",
            fg="white"
        ).pack(side=tk.BOTTOM, fill=tk.X)

        # Bind Escape key to exit full screen
        self.root.bind("<Escape>", self.toggle_fullscreen)

    # The rest of the IMS class methods remain unchanged
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

def main():
    root = tk.Tk()
    login_page = LuxuryLoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()

