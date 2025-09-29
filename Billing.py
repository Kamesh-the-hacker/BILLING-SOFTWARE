from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import sqlite3
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from tkinter.filedialog import asksaveasfile
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from num2words import num2words
from tkinter import filedialog
from reportlab.lib.units import inch
import tkinter as tk
from tkinter import scrolledtext, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import StringVar
import random
import string
import tkinter as tk
from tkinter import ttk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm



class PackingSlipManager:
    def __init__(self):
        self.conn = sqlite3.connect('python\\ims.db')
        self.cursor = self.conn.cursor()
        self.create_packing_slip_table()
        

    def create_packing_slip_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS packing_slips
                             (code TEXT PRIMARY KEY,
                              customer_name TEXT,
                              date TEXT,
                              cart_data TEXT,
                              status TEXT)''')
        self.conn.commit()

    def generate_unique_code(self):
        while True:
            code = f"{random.randint(1000, 9999):04d}"  # Generate 4-digit number
            self.cursor.execute("SELECT code FROM packing_slips WHERE code=?", (code,))
            if not self.cursor.fetchone():
                return code

    def save_packing_slip(self, customer_name, cart_data):
        code = self.generate_unique_code()
        date = datetime.now().strftime("%Y-%m-%d")
        cart_str = str(cart_data)
        self.cursor.execute("INSERT INTO packing_slips (code, customer_name, date, cart_data, status) VALUES (?, ?, ?, ?, ?)",
                          (code, customer_name, date, cart_str, "pending"))
        self.conn.commit()
        return code

    def get_packing_slip(self, code):
        self.cursor.execute("SELECT * FROM packing_slips WHERE code=?", (code,))
        return self.cursor.fetchone()

class PackingSlipViewer:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Packing Slip Manager")
        self.window.overrideredirect(True)
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = screen_width - 240
        window_height = screen_height - 180
        x_position = 220
        y_position = 130
        
        # Set window geometry to match BillClass
        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.window.config(bg="#f0f0f0")
        
        # Create manager instance
        self.manager = PackingSlipManager()
        
        # Main Frame
        main_frame = Frame(self.window, bd=2, relief=RIDGE, bg='#f0f0f0')
        main_frame.place(x=10, y=10, width=window_width-20, height=window_height-20)
        
        # Title
        title = Label(main_frame, text="Packing Slip Manager", font=("goudy old style", 18), bg="#404a42", fg='white')
        title.pack(side=TOP, fill=X)
        
        # Search frame
        search_frame = Frame(main_frame, bd=2, relief=RIDGE, bg='#f0f0f0')
        search_frame.pack(fill=X, padx=10, pady=10)
        
        Label(search_frame, text="Packing Slip Code:", font=("goudy old style", 15), bg="#f0f0f0").pack(side=LEFT, padx=5)
        self.code_entry = Entry(search_frame, font=("goudy old style", 15))
        self.code_entry.pack(side=LEFT, padx=5)
        
        # Buttons Frame
        btn_frame = Frame(search_frame, bg='#f0f0f0')
        btn_frame.pack(side=LEFT, padx=10)
        
        # Generate Bill Button
        Button(btn_frame, text="Generate Bill", command=self.generate_bill_from_code,
               font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").pack(side=LEFT, padx=5)
        Button(btn_frame, text="Delete", command=self.delete_packing_slip,
               font=("goudy old style", 15), bg="#ff5252", fg="white", cursor="hand2").pack(side=LEFT, padx=5)
        
        # Exit Button
        Button(btn_frame, text="Exit", command=self.window.destroy,
               font=("goudy old style", 15), bg="#ff5252", fg="white", cursor="hand2").pack(side=LEFT, padx=5)

        
        
        # List frame
        list_frame = Frame(main_frame, bg='#f0f0f0')
        list_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ('Code', 'Customer', 'Date', 'Status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Style configuration for Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("goudy old style", 12))
        style.configure("Treeview.Heading", font=("goudy old style", 12, "bold"))
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=int((window_width-60)/len(columns)), anchor=CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Bind tree selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # Load initial data
        self.load_packing_slips()
    
    def on_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0])
            code = item['values'][0]
            self.code_entry.delete(0, END)
            self.code_entry.insert(0, code)
    
    def load_packing_slips(self):
        self.tree.delete(*self.tree.get_children())
        self.manager.cursor.execute("SELECT code, customer_name, date, status FROM packing_slips")
        for row in self.manager.cursor.fetchall():
            self.tree.insert('', 'end', values=row)
    
    def generate_bill_from_code(self):
        code = self.code_entry.get().strip()
        if not code:
            messagebox.showerror("Error", "Please enter a packing slip code")
            return
            
        slip_data = self.manager.get_packing_slip(code)
        if not slip_data:
            messagebox.showerror("Error", "Invalid packing slip code")
            return
        
        # Call the method to generate the bill

        self.generate_bill(slip_data)
        self.update_status(code, "Success")

    def update_status(self, code, new_status):
        try:
            self.manager.cursor.execute("UPDATE packing_slips SET status=? WHERE code=?", (new_status, code))
            self.manager.conn.commit()
            self.load_packing_slips()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {str(e)}")
    def delete_packing_slip(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select a packing slip to delete")
            
            
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this packing slip?"):
            item = self.tree.item(selected_items[0])
            code = item['values'][0]
            
            try:
                self.manager.cursor.execute("DELETE FROM packing_slips WHERE code=?", (code,))
                self.manager.conn.commit()
                
                self.load_packing_slips()
                self.code_entry.delete(0, END)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete packing slip: {str(e)}")
    
    def on_select(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0])
            code = item['values'][0]
            self.code_entry.delete(0, END)
            self.code_entry.insert(0, code)

        

    def generate_bill(self, slip_data):
        code, customer_name, date, cart_data_str, status = slip_data
        
        try:
            # Safely evaluate the cart data string to a list
            cart_data = eval(cart_data_str)
        except (SyntaxError, ValueError):
            messagebox.showerror("Error", "Invalid cart data format")
            return

        # Validate cart data
        if not cart_data or not isinstance(cart_data, list):
            messagebox.showerror("Error", "No items in the cart")
            return

        # Calculate total amount
        total_amount = sum(item[4] for item in cart_data)  # Assuming item[4] is the total price

        gst_rate = 0.05  # 5%
        gst_amount = total_amount * gst_rate
        total_with_gst = total_amount + gst_amount

        # Open file dialog to save invoice
        file = filedialog.asksaveasfilename(
            filetypes=[("PDF file", ".pdf")],
            defaultextension=".pdf",
            initialfile=f"{customer_name}_Invoice{code}"
        )
        self.conn = sqlite3.connect('python\\ims.db')
        self.cursor = self.conn.cursor()
        self.name =customer_name
        self.cursor.execute("SELECT * FROM kyc WHERE name=?",(self.name,))
        c = self.cursor.fetchone()
        if file:  # Check if the user selected a file
            #self.create_invoice(total_with_gst, gst_amount, customer_name, total_amount, cart_data, file)
            self.generate_pdf(file,cart_data,customer_name,c)

    

    def generate_pdf(self,file,cart_data,customer,cs):
        c = canvas.Canvas(file, pagesize=A4)
        width, height = A4

        # Colors
        border_color = colors.Color(0.651, 0.486, 0.322)
        header_color = colors.Color(0.545, 0.341, 0.165)
        background_color = colors.Color(1, 0.953, 0.898)

        # Background
        c.setFillColor(background_color)
        c.rect(0, 0, width, height, fill=1)

        # Border
        c.setStrokeColor(border_color)
        c.setLineWidth(1)
        c.rect(5*mm, 5*mm, width-10*mm, height-10*mm, fill=0)

        # Header
        c.setFillColor(header_color)
        
        # Add logo
        logo_path = "python\\logo.png"
        c.drawImage(logo_path, 10*mm, height-35*mm, width=30*mm, height=25*mm, mask='auto')



        # Company details
        c.setFont("Helvetica-Bold", 18)
        c.drawString(65*mm, height-15*mm, "SARAVANA FASHION")
        c.setFont("Helvetica-Bold", 8)
        c.drawString(65*mm, height-20*mm, "22/1, THILLAI NAGAR, FIRST STREET")
        c.drawString(65*mm, height-24*mm, "DHARAPURAM ROAD, TIRUPUR - 641604")
        c.drawString(65*mm, height-28*mm, "Phone No's : 86088 97777 / 90878 82233, E-Mail : kanizokids@gmail.com")
        c.drawString(65*mm, height-32*mm, "GSTIN : 33DULPS8136R1ZL")
        c.drawString(65*mm, height-36*mm, "State :TAMIL NADU State Code : 33")

        # Separator line
        c.line(5*mm, height-44*mm, width-5*mm, height-44*mm)
        c.drawString(10*mm, height-50*mm, "M/s :")
        #=================================================================================================


        address_components = [
            cs[3],
            cs[9],
            cs[5],      # Customer name
                  # Street Address
                  # City
            cs[10],  
            cs[4]    # State
        ]

        # Remove any None or empty components
        address_components = [str(comp).strip() for comp in address_components if comp]

        # Print address lines, wrapping long lines if necessary
        max_line_width = 25  # Maximum characters per line
        formatted_address = []

        for component in address_components:
            # Break long components into multiple lines
            while len(component) > max_line_width:
                # Find the last space before max_line_width
                split_index = component[:max_line_width].rfind(' ')
                if split_index == -1:
                    split_index = max_line_width
                
                formatted_address.append(component[:split_index])
                component = component[split_index:].strip()
            
            # Add the remaining or short component
            if component:
                formatted_address.append(component)

        # Print formatted address lines
        for i, line in enumerate(formatted_address):
            c.drawString(20*mm, height-(50+i*3.5)*mm, line)


















        # Customer details with line breaks for cs[9]
        '''c.setFont("Helvetica-Bold", 9)
        c.drawString(10*mm, height-50*mm, "M/s :")
        c.drawString(20*mm, height-50*mm, f"{customer}")
        
        # Split cs[9] into multiple lines if needed
          # Split cs[9] into multiple lines if needed
        
        address_lines = [cs[9][i:i+40] for i in range(0, len(cs[9]), 40)]
        for idx, line in enumerate(address_lines):
            c.drawString(20*mm, height-(55+idx*5)*mm, line)
        
        c.drawString(20*mm, height-60*mm, f"{cs[5]}")
        c.drawString(20*mm, height-65*mm, f"{cs[10]}")
        c.drawString(20*mm, height-70*mm, f"MOBILE: {cs[4]}")'''















#==================================================================================================






        current_date = datetime.now().strftime("%d-%m-%Y")
        invoice_no = random.randint(1000, 9999)

        # Invoice details
        c.setFont("Helvetica-Bold", 9)
        c.drawString(100*mm, height-50*mm, "Invoice No :")
        c.drawString(100*mm, height-60*mm, "Order No :")
        c.drawString(100*mm, height-65*mm, "Order Date :")
        c.drawString(100*mm, height-70*mm, "Lorry Reciept No :")
        c.drawString(100*mm, height-75*mm, "Lorry Reciept Date :")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(155*mm, height-50*mm, f" {invoice_no}")
        c.drawString(155*mm, height-60*mm, f"Transport :{cs[11]}")

        c.drawString(100*mm, height-80*mm,f"Date :")
        c.drawString(155*mm, height-80*mm, f"{current_date}")
        c.line(5*mm, height-80*mm, width-120*mm, height-80*mm)
        c.line(90*mm, height-52*mm, width-5*mm, height-52*mm)

        # Additional details
        k=self.code_entry.get()
        c.setFont("Helvetica-Bold", 9)
        c.drawString(10*mm, height-85*mm, "No Of Cases : 1 BUNDLE")
        c.drawString(10*mm, height-90*mm, f"Place of Supply :{cs[10]}")
        c.drawString(10*mm, height-95*mm, f"Packing Slip No :{k}")
        c.drawString(10*mm, height-100*mm, f"Party GST No : {cs[7]}")
        c.drawString(10*mm, height-105*mm, "Credit Days : CASH")

        c.drawString(100*mm, height-85*mm, "Eway Bill No :")
        c.drawString(100*mm, height-90*mm, "Freight :")
        c.drawString(100*mm, height-95*mm, "Eway Bill No :")

        c.drawString(100*mm, height-100*mm, "Agent : DIRECT")
        c.line(5*mm, height-107*mm, width-5*mm, height-107*mm)
        
        c.line(255,717,255,539)

        # Main table
        table_top = height-110*mm
        table_bottom = 80*mm
        c.rect(5*mm, table_bottom, width-10*mm, table_top-table_bottom, fill=0)

        # Table headers
        headers = ["Sl No", "HSN Code", "Description Of Goods", "Size", "Total Box", "Qty In Pcs", "Rate / Pcs", "Net Amount"]
        x_positions = [5, 15, 30, 90, 110, 130, 150, 170, 190]
        c.setFont("Helvetica-Bold", 8)
        for i, header in enumerate(headers):
            c.drawString(x_positions[i]*mm + 1*mm, table_top-5*mm, header)

        # Vertical lines
        for x in x_positions[1:-1]:
            c.line(x*mm, table_bottom, x*mm, table_top)

        # Horizontal lines
        c.line(5*mm, table_top-7*mm, width-5*mm, table_top-7*mm)
        for i in range(1, 15):
            c.line(5*mm, table_top-7*mm-i*5*mm, width-5*mm, table_top-7*mm-i*5*mm)

        # Table content with corrected positions
        total_qty = 0
        y_pos = table_top - 11.7*mm
        for idx, item in enumerate(cart_data, 1):
            product_name, size, _, qty, amount = item
            rate = amount / qty if qty else 0
                
            c.setFont("Helvetica", 9)
            # Adjusted content positions to align within existing columns
            c.drawString(8*mm, y_pos, str(idx))            # Sl No
            c.drawString(18*mm, y_pos, "6109")            # HSN code
            c.drawString(32*mm, y_pos, product_name)      # Description
            c.drawString(93*mm, y_pos, str(size))         # Size
            c.drawString(113*mm, y_pos, "1")              # Total Box
            c.drawString(133*mm, y_pos, str(qty))         # Qty in Pcs
            c.drawString(153*mm, y_pos, f"{rate:.2f}")    # Rate/Pcs
            c.drawString(173*mm, y_pos, f"{amount:.2f}")  # Net Amount
            y_pos -= 14
            total_qty += qty
                
        

        c.line(5*mm, height-223*mm, width-5*mm, height-223*mm)
        c.line(312,125,312,210)
        c.line(5*mm, height-253*mm, width-5*mm, height-253*mm)

        # Calculate totals with GST
        total_amount = sum(amount for _, _, _, _, amount in cart_data)
        gst_rate = 0.05  # 5% GST
        gst_amount = total_amount * gst_rate
        total_with_gst = total_amount + gst_amount
        rounded_total = round(total_with_gst)

        # Update totals section
        c.setFont("Helvetica-Bold", 9)
        c.drawString(151*mm, table_bottom-4*mm, "GROSS AMT :")
        c.drawString(175*mm, table_bottom-4*mm, f"{total_amount:.2f}")
        c.drawString(120*mm, 70*mm, "GST (5%)")
        c.drawString(180*mm, 70*mm, f"{gst_amount:.2f}")
        c.drawString(120*mm, 65*mm, "ROUND OFF")
        c.drawString(180*mm, 65*mm, f"{rounded_total - total_with_gst:.2f}")
        c.drawString(120*mm, 60*mm, "Bill Amount :")
        c.drawString(180*mm, 60*mm, f"{rounded_total:.2f}")

        # Convert amount to words
        def number_to_words(number):
            # Add your number to words conversion logic here
            # This is a simplified version
            return num2words(number, lang='en').title() + " Only"

        # Amount in words
        amount_in_words = number_to_words(rounded_total)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(10*mm, 40*mm, "Amount In Words :")
        c.drawString(40*mm, 40*mm, amount_in_words)
        c.line(5*mm, 38*mm, width-5*mm, 38*mm)

        # Bank details
        y_pos = 70*mm
        c.setFont("Helvetica-Bold", 9)
        c.drawString(10*mm, y_pos, "Bank Details : SARAVANA FASHION")
        c.setFont("Helvetica", 9)
        bank_details = [
            "Bank Name : INDIAN BANK",
            "Account No : 6372272999",
            "Branch : TIRUPUR",
            "IFSC Code : IDIB000T109",
            "Payment Mode : NEFT / RTGS / UPI",
            "CHEQUES DEPOSIT ARE NOT ALLOWED"
        ]
        for detail in bank_details:
            y_pos -= 4*mm
            c.drawString(10*mm, y_pos, detail)


        # Footer text
        c.setFont("Helvetica-Bold", 8)
        footer_text = [
            "Certified that particulars given above are correct and the amount indicated",
            "represented the price actually charged and that there is no flow additional",
            "consideration directly or indirectly from the buyer.",
            "N.B : Goods once sold cannot be taken back. Our responsibility ceases as soon",
            "as the Goods leave our godown. Interest will be charged at 18% per annum",
            "after 30 days of the date of invoice CREDIT BASIS only."
        ]
        y_pos = 30*mm
        for text in footer_text:
            c.drawString(10*mm, y_pos, text)
            y_pos -= 3*mm

        # Final footer elements
        c.line(368,14,368,108)
        #c.drawString(120*mm, 15*mm, "Checked E")
        c.drawString(160*mm, 15*mm, "For Saravana Fashion")
        c.drawString(160*mm, 10*mm, "Authorized Signatory")

        c.setFont("Helvetica-Bold", 9)
        
        c.line(5*mm, height-285*mm, width-80*mm, height-285*mm)
        c.drawString(10*mm, 8*mm, "E.& O.E")
        c.drawString(70*mm, 8*mm, "Subject to TIRUPUR Jurisdictions")

        c.save()
        print("Perfect invoice PDF genenerated successfully!")
        messagebox.showinfo("Success", f"invoice generated successfully!")
class BillClass:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width - 240  # Subtracting menu width (200) + padding (40)
        window_height = screen_height - 180  # Subtracting top margin (130) + bottom margin (50)
        x_position = 220  # Aligned with dashboard layout
        y_position = 130  # Aligned with dashboard layout
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.title("Saravana Fashion | Developed by Kamesh")
        self.root.config(bg="#f0f0f0")
        self.root.overrideredirect(True)
        self.root.focus_force()
        self.conn = sqlite3.connect('python\\ims.db')
        self.cursor = self.conn.cursor()
        

        self.cat_list = self.fetch_cat()
        self.var_cat = StringVar()
        self.var_pro = StringVar()
        self.si_list = []
        self.var_si = StringVar()
        self.var_qty = StringVar()
        self.cart = []
        self.packing_manager = PackingSlipManager()

        product_frame = Frame(self.root, bd=2, relief=RIDGE, bg='#f0f0f0')
        product_frame.place(x=10, y=20, width=450, height=630)
        title=Label(product_frame,text="BILLING ",font=("goudy old style",18),bg='#0f4d7d',fg='white').pack(side=TOP,fill=X)


        # UI Elements
        Label(product_frame, text="Bill For", font=("goudy old style", 18), bg="#f0f0f0").place(x=30, y=60)
        Label(product_frame, text="Category", font=("goudy old style", 18), bg="#f0f0f0").place(x=30, y=120)
        Label(product_frame, text="Products", font=("goudy old style", 18), bg="#f0f0f0").place(x=30, y=180)
        Label(product_frame, text="Size", font=("goudy old style", 18), bg="#f0f0f0").place(x=30, y=240)
        Label(product_frame, text="Price List", font=("goudy old style", 18), bg="#f0f0f0").place(x=30, y=300)
        Label(product_frame, text="Quantity", font=("goudy old style", 18), bg="#f0f0f0").place(x=30, y=360)

        self.b_name = self.fetch_bi()
        self.cmb_bi = ttk.Combobox(product_frame, values=self.b_name, font=("time new roman", 15))
        self.cmb_bi.place(x=150, y=60, width=200)

        self.cmb_cat = ttk.Combobox(product_frame, textvariable=self.var_cat, values=self.cat_list, font=("time new roman", 15))
        self.cmb_cat.place(x=150, y=120, width=200)
        self.cmb_cat.bind("<<ComboboxSelected>>", self.update_pro)

        self.cmb_pro = ttk.Combobox(product_frame, textvariable=self.var_pro, font=("time new roman", 15))
        self.cmb_pro.place(x=150, y=180, width=200)
        self.cmb_pro.bind("<<ComboboxSelected>>", self.update_sizes)

        self.cmb_si = ttk.Combobox(product_frame, textvariable=self.var_si, values=self.si_list, font=("time new roman", 15))
        self.cmb_si.place(x=150, y=240, width=200)

        self.price_list_combo = ttk.Combobox(product_frame, font=("time new roman", 15))
        self.price_list_combo.place(x=150, y=300, width=200)
        self.cmb_pro.bind("<<ComboboxSelected>>", self.update_sizes)
        self.cmb_si.bind("<<ComboboxSelected>>", self.update_prices) 

        txt_qty = Entry(product_frame, textvariable=self.var_qty, font=("goudy old style", 15), bg="white")
        txt_qty.place(x=150, y=360, width=200)

        Button(product_frame, text="Add To Cart", command=self.add_to_cart, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=150, y=520, width=130, height=40)
        Button(product_frame, text="Packing Slip", command=self.generate_ps, font=("goudy old style", 15), bg="#4169e1", fg="white", cursor="hand2").place(x=10, y=520, width=130, height=40)
        Button(product_frame, text="Invoice", command=self.open_packing_slip_viewer, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=300, y=520, width=130, height=40)
        self.update_pro(None)


        # Tree view for cart
        self.cart_tree = ttk.Treeview(self.root, columns=("product", "size", "quantity", "price", "total"), show="headings")
        self.cart_tree.place(x=500, y=20, width=680, height=550)

        # Set column headings
        for col in ("product", "size", "quantity", "price", "total"):
            self.cart_tree.heading(col, text=col.capitalize())
            self.cart_tree.column(col, width=100, anchor=CENTER)

        # Scrollbar for tree view
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.cart_tree.yview)
        scrollbar.place(x=1180, y=20, height=550)
        self.cart_tree.configure(yscrollcommand=scrollbar.set)

        # Delete button for cart items
        self.delete_button = tk.Button(self.root, text="Delete Item", command=self.delete_from_cart,
                                       font=("goudy old style", 15), bg="#ff5722", fg="white", cursor="hand2")
        self.delete_button.place(x=500, y=580, width=130, height=40)

        # Add search functionality to comboboxes
        self.add_search_to_combobox(self.cmb_bi, self.b_name)
        self.add_search_to_combobox(self.cmb_cat, self.cat_list)


    def add_search_to_combobox(self, combobox, values):
        combobox['values'] = values
        combobox.bind('<KeyRelease>', lambda event: self.search_combobox(event, combobox, values))

    def search_combobox(self, event, combobox, values):
        value = event.widget.get()
        if value == '':
            combobox['values'] = values
        else:
            data = []
            for item in values:
                if value.lower() in item.lower():
                    data.append(item)
            combobox['values'] = data

    def delete_from_cart(self):
        selected_item = self.cart_tree.selection()
        if selected_item:
            item = self.cart_tree.item(selected_item)
            index = self.cart_tree.index(selected_item)
            self.cart.pop(index)
            self.cart_tree.delete(selected_item)
        else:
            messagebox.showwarning("Warning", "Please select an item to delete.")


    def open_packing_slip_viewer(self):
        PackingSlipViewer()

    def generate_ps(self):
        self.name = self.cmb_bi.get()
        self.cursor.execute("SELECT * FROM kyc WHERE name=?", (self.name,))
        customer = self.cursor.fetchone()

        if customer is None:
            messagebox.showerror("Error", "Customer not found!")
            return

        # Generate unique code and save packing slip data
        code = self.packing_manager.save_packing_slip(self.name, self.cart)

        file = filedialog.asksaveasfilename(
            filetypes=[("pdf file", ".pdf")],
            defaultextension=".pdf",
            initialfile=f"{self.cmb_bi.get()}_PS_{code}")
        
        if file:
            self.create_ps(file, customer, code)

    def create_ps(self, mypath, customer, code):
        c = canvas.Canvas(mypath, pagesize=(8*72, 5*72))
        width, height = 8 * 72, 5 * 72

        # Add the packing slip code at the top
        c.setFont("Helvetica-Bold", 12)
        c.drawString(10, height - 20, f"Packing Slip Code: {code}")

        # ... (rest of the existing create_ps code) ...
        
        c.save()
        messagebox.showinfo("Success", f"Packing slip generated successfully!\nYour packing slip code is: {code}")

    def generate_bill_from_packing_slip(self, code):
        slip_data = self.packing_manager.get_packing_slip(code)
        if not slip_data:
            return False

        # Set the cart data from the packing slip
        self.cart = eval(slip_data[3])  # Convert string back to list
        self.name = slip_data[1]  # Set customer name
        
        # Generate the bill
        self.generate_bill()
        
        # Update packing slip status
        self.packing_manager.cursor.execute("UPDATE packing_slips SET status='billed' WHERE code=?", (code,))
        self.packing_manager.conn.commit()
        
        return True

    def fetch_cat(self):
        with sqlite3.connect("python\\ims.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT name FROM category")
            cat = cursor.fetchall()
        return [category[0] for category in cat]

    def fetch_pro(self, category_name):
        with sqlite3.connect("python\\ims.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT name FROM product WHERE category = ?", (category_name,))
            pro = cursor.fetchall()
        return [product[0] for product in pro]

    def fetch_sizes(self, product_name):
        with sqlite3.connect("python\\ims.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT size FROM product WHERE name = ?", (product_name,))
            sizes = cursor.fetchall()
        return [size[0] for size in sizes]

    def update_sizes(self, event):
        selected_product = self.cmb_pro.get()
        if selected_product:
            sizes = self.fetch_sizes(selected_product)
            self.cmb_si["values"] = sizes
            self.cmb_si.set("")

    def update_pro(self, event):
        selected_cat = self.cmb_cat.get()
        if selected_cat:
            products = self.fetch_pro(selected_cat)
            self.cmb_pro["values"] = products
            self.cmb_pro.set("")
            self.cmb_si.set("")
            self.price_list_combo.set("")

    def update_prices(self, event):
        selected_product = self.cmb_pro.get()
        selected_size = self.cmb_si.get()

        if selected_product and selected_size:
            with sqlite3.connect("python\\ims.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT price1, price2, price3, price4, price5 FROM product WHERE name = ? AND size = ?",
                    (selected_product, selected_size)
                )
                prices = cursor.fetchone()
            
            if prices:
                # Update price_list_combo with fetched prices
                self.price_list_combo["values"] = prices
                self.price_list_combo.set("")  # Clear selection



    def fetch_bi(self):
        with sqlite3.connect("python\\ims.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT name FROM kyc")
            kyc = cursor.fetchall()
        return [nkyc[0] for nkyc in kyc]

    def add_to_cart(self):
        product_name = self.cmb_pro.get()
        selected_size = self.cmb_si.get()
        selected_price = self.price_list_combo.get()
        quantity = self.var_qty.get()

        if not product_name or not selected_size or not selected_price or not quantity:
            messagebox.showerror("Error", "Please complete all selections!")
            return

        try:
            quantity = int(quantity)
            price = float(selected_price)
        except ValueError:
            messagebox.showerror("Error", "Quantity and price must be numbers!")
            return

        total_price = price * quantity
        self.cart.append((product_name, selected_size, quantity, price, total_price))
        self.cart_tree.insert('', 'end', values=(product_name, selected_size, quantity, price, total_price))




    def generate_ps(self):
        #if not self.cart:  # Ensure the cart is not empty
          #  messagebox.showerror("Error", "No items in the cart!")
           # return

        self.name = self.cmb_bi.get()
        self.cursor.execute("SELECT * FROM kyc WHERE name=?", (self.name,))
        customer = self.cursor.fetchone()

        if customer is None:
            messagebox.showerror("Error", "Customer not found!")
            return
        file = filedialog.asksaveasfilename(
            filetypes=[("pdf file", ".pdf")],
            defaultextension=".pdf",
            initialfile=self.cmb_bi.get()+"  packing slip")
        
        if file:  # Check if the user selected a file
            self.create_ps(file, customer) 







    def create_ps(self, mypath, customer, code):
        page_width = 6 * 72
        page_height = 4 * 72
        width = 6 * 72
        height = 4 * 72
        c = canvas.Canvas(mypath, pagesize=(page_width, page_height))
        c.setLineWidth(1)
        c.rect(1*mm, 2*mm, width-3*mm, height-5*mm, fill=0)
        
        # Draw headers
        c.setFont("Helvetica-Bold", 12)
        c.drawString(page_width/2 - 40, page_height - 20, "PACKING SLIP")
        c.line(1*mm, height-8*mm, width-2*mm, height-8*mm)
        c.drawString(page_width/2 - 65, page_height - 35, "SARAVANA FASHION")
        c.line(1*mm, height-14*mm, width-2*mm, height-14*mm)
        c.line(120, 265, 120, 248)
        c.line(300, 265, 300, 248)
        
        # Draw header information
        c.setFont("Helvetica", 9)
        current_date = datetime.now().strftime("%d/%m/%Y")
        c.drawString(10, page_height - 35, f"Packing Date: {current_date}")
        c.drawString(page_width - 127, page_height - 35, f"Packing Slip No: {code}")
        
        # Draw To address
        c.setFont("Helvetica-Bold", 9)
        c.drawString(15, page_height - 50, "To:")
        address_components = [str(comp).strip() for comp in [customer[3], customer[12], customer[10]] if comp]
        for i, line in enumerate(address_components):
            c.drawString(35, page_height - 55 - (i * 10), line)
        
        # Get unique sizes from cart
        cart_sizes = sorted(set(item[1] for item in self.cart), key=lambda x: (
            # Sort numeric sizes first, then letter sizes
            (0, int(x)) if x.isdigit() else (1, x)
        ))
        
        # Add TOTAL column
        all_sizes = cart_sizes + ['TOTAL']
        
        # Calculate column widths
        style_width = 120
        available_width = page_width - style_width - 20
        size_column_width = min(50, available_width / len(all_sizes))  # Ensure minimum column width
        
        # Start table position
        y_table = page_height - 100
        c.setFont("Helvetica-Bold", 8)
        
        # Draw style column header
        c.rect(10, y_table, style_width, 15)
        c.drawString(15, y_table + 5, "STYLE")
        
        # Draw size column headers
        x_pos = 10 + style_width
        for size in all_sizes:
            c.rect(x_pos, y_table, size_column_width, 15)
            text_width = c.stringWidth(str(size), "Helvetica-Bold", 8)
            x_text = x_pos + (size_column_width - text_width) / 2
            c.drawString(x_text, y_table + 5, str(size))
            x_pos += size_column_width
        
        # Group items by product name
        product_groups = {}
        for item in self.cart:
            product_name = item[0]
            size = item[1]
            qty = item[2]
            if product_name not in product_groups:
                product_groups[product_name] = {size: 0 for size in cart_sizes}
            product_groups[product_name][size] = qty
        
        # Draw product rows
        y_pos = y_table - 15
        for product_name, sizes in product_groups.items():
            # Draw style cell
            c.rect(10, y_pos, style_width, 15)
            c.setFont("Helvetica", 8)
            max_chars = 20
            displayed_name = (product_name[:max_chars-2] + '..') if len(product_name) > max_chars else product_name
            c.drawString(15, y_pos + 5, displayed_name)
            
            # Draw quantity cells
            x_pos = 10 + style_width
            total = 0
            for size in cart_sizes:
                c.rect(x_pos, y_pos, size_column_width, 15)
                qty = sizes.get(size, 0)
                if qty > 0:
                    qty_text = str(qty)
                    text_width = c.stringWidth(qty_text, "Helvetica", 8)
                    x_text = x_pos + (size_column_width - text_width) / 2
                    c.drawString(x_text, y_pos + 5, qty_text)
                total += qty
                x_pos += size_column_width
            
            # Draw row total
            c.rect(x_pos, y_pos, size_column_width, 15)
            total_text = str(total)
            text_width = c.stringWidth(total_text, "Helvetica", 8)
            x_text = x_pos + (size_column_width - text_width) / 2
            c.drawString(x_text, y_pos + 5, total_text)
            
            y_pos -= 15
        
        # Draw total row
        c.rect(10, y_pos, style_width, 15)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(15, y_pos + 5, "TOTAL")
        
        # Calculate and draw column totals
        x_pos = 10 + style_width
        grand_total = 0
        for size in cart_sizes:
            total = sum(sizes.get(size, 0) for sizes in product_groups.values())
            c.rect(x_pos, y_pos, size_column_width, 15)
            if total > 0:
                total_text = str(total)
                text_width = c.stringWidth(total_text, "Helvetica-Bold", 8)
                x_text = x_pos + (size_column_width - text_width) / 2
                c.drawString(x_text, y_pos + 5, total_text)
            grand_total += total
            x_pos += size_column_width
        
        # Draw grand total
        c.rect(x_pos, y_pos, size_column_width, 15)
        grand_total_text = str(grand_total)
        text_width = c.stringWidth(grand_total_text, "Helvetica-Bold", 8)
        x_text = x_pos + (size_column_width - text_width) / 2
        c.drawString(x_text, y_pos + 5, grand_total_text)
        
        # Draw footer
        y_pos -= 30
        c.line(page_width-100, y_pos, page_width-10, y_pos)
        c.setFont("Helvetica", 8)
        c.drawString(page_width-80, y_pos - 20, "( Checked By )")
        
        c.save()
        messagebox.showinfo("Success", f"Packing slip generated successfully!\nYour packing slip code is: {code}")

    def generate_ps(self):
        if not self.cart:
            messagebox.showerror("Error", "No items in the cart!")
            return
            pass

        self.name = self.cmb_bi.get()
        if not self.name:
            messagebox.showerror("Error", "Please select a customer!")
            return
            

        self.cursor.execute("SELECT * FROM kyc WHERE name=?", (self.name,))
        customer = self.cursor.fetchone()

        if customer is None:
            messagebox.showerror("Error", "Customer not found!")
            return
            

        # Generate unique code and save packing slip data
        code = self.packing_manager.save_packing_slip(self.name, self.cart)

        file = filedialog.asksaveasfilename(
            filetypes=[("PDF file", ".pdf")],
            defaultextension=".pdf",
            initialfile=f"{self.name}_PS_{code}")
        
        if file:
            self.create_ps(file, customer, code)

    def open_packing_slip_viewer(self):
        PackingSlipViewer()
























  

    def generate_bill_from_packing_slip(self, code):
        slip_data = self.packing_manager.get_packing_slip(code)
        if not slip_data:
            return False

        # Set the cart data from the packing slip
        self.cart = eval(slip_data[3])  # Convert string back to list
        self.name = slip_data[1]  # Set customer name
        
        # Generate the bill
        self.generate_bill()
        
        # Update packing slip status
        self.packing_manager.cursor.execute("UPDATE packing_slips SET status='billed' WHERE code=?", (code,))
        self.packing_manager.conn.commit()
        
        return True
if __name__ == "__main__":
    root = Tk()
    app = BillClass(root)
    root.mainloop()
