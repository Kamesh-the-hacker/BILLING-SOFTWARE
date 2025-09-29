

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from datetime import datetime
import random

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

class BillClass:
    # ... (other methods remain the same)

    def create_ps(self, mypath, customer, code):
        page_width = 6 * 72  # 6 inches
        page_height = 4 * 72  # 4 inches
        c = canvas.Canvas(mypath, pagesize=(page_width, page_height))
        c.setLineWidth(1)
        c.rect(1*mm, 2*mm, page_width-3*mm, page_height-5*mm, fill=0)
        
        # Draw the main title
        c.setFont("Helvetica-Bold", 12)
        c.drawString(page_width/2 - 40, page_height - 20, "PACKING SLIP")
        c.line(1*mm, page_height-8*mm, page_width-2*mm, page_height-8*mm)
        c.drawString(page_width/2 - 65, page_height - 35, "SARAVANA FASHION")
        c.line(1*mm, page_height-14*mm, page_width-2*mm, page_height-14*mm)
        
        # Draw header information
        c.setFont("Helvetica", 9)
        current_date = datetime.now().strftime("%d/%m/%Y")
        c.drawString(10, page_height - 35, f"Packing Date: {current_date}")
        c.drawString(page_width - 127, page_height - 35, f"Packing Slip No: {code}")
        
        # Draw To address box
        c.setFont("Helvetica-Bold", 9)
        c.drawString(15, page_height - 50, "To:")
        c.setFont("Helvetica", 9)

        # Improved address handling
        address_components = [
            customer[3],      # Customer name
            customer[12],     # City
            customer[10]      # State
        ]

        # Remove any None or empty components
        address_components = [str(comp).strip() for comp in address_components if comp]

        # Print address lines, wrapping long lines if necessary
        max_line_width = 25  # Maximum characters per line
        formatted_address = []

        for component in address_components:
            while len(component) > max_line_width:
                split_index = component[:max_line_width].rfind(' ')
                if split_index == -1:
                    split_index = max_line_width
                formatted_address.append(component[:split_index])
                component = component[split_index:].strip()
            if component:
                formatted_address.append(component)

        # Print formatted address lines
        for i, line in enumerate(formatted_address):
            c.drawString(35, page_height - 55 - (i * 10), line)

        # Draw the table
        y_table = page_height - 100
        c.setFont("Helvetica-Bold", 8)
        
        # Draw the style column header
        c.rect(10, y_table, 100, 15)
        c.drawString(15, y_table + 5, "STYLE")
        
        # Get unique sizes from cart items
        sizes = sorted(set(item[1] for item in self.cart))
        
        # Draw size column headers
        x_pos = 110
        for size in sizes + ["TOTAL"]:
            c.rect(x_pos, y_table, 35, 15)
            c.drawString(x_pos + 3, y_table + 5, str(size))
            x_pos += 35
        
        # Draw product rows
        y_pos = y_table - 15
        
        # Group items by product name
        product_groups = {}
        for item in self.cart:
            product_name, size, _, qty, _ = item
            if product_name not in product_groups:
                product_groups[product_name] = {}
            product_groups[product_name][size] = qty
        
        # Draw each product row
        for product_name, sizes_dict in product_groups.items():
            # Draw style cell
            c.rect(10, y_pos, 100, 15)
            c.setFont("Helvetica", 8)
            c.drawString(15, y_pos + 5, product_name)
            
            # Draw quantity cells
            x_pos = 110
            total = 0
            for size in sizes:
                c.rect(x_pos, y_pos, 35, 15)
                qty = sizes_dict.get(size, 0)
                if qty > 0:
                    c.drawString(x_pos + 5, y_pos + 5, str(qty))
                total += qty
                x_pos += 35
                
            # Draw total cell
            c.rect(x_pos, y_pos, 35, 15)
            c.drawString(x_pos + 5, y_pos + 5, str(total))
            
            y_pos -= 15
        
        # Draw total row
        c.rect(10, y_pos, 100, 15)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(15, y_pos + 5, "TOTAL")
        
        # Calculate and draw column totals
        x_pos = 110
        grand_total = 0
        for size in sizes:
            total = sum(sizes_dict.get(size, 0) for sizes_dict in product_groups.values())
            c.rect(x_pos, y_pos, 35, 15)
            if total > 0:
                c.drawString(x_pos + 5, y_pos + 5, str(total))
            grand_total += total
            x_pos += 35
        
        # Draw grand total
        c.rect(x_pos, y_pos, 35, 15)
        c.drawString(x_pos + 5, y_pos + 5, str(grand_total))
        
        # Draw footer
        y_pos -= 30
        c.line(page_width-100, y_pos, page_width-10, y_pos)  # Line for checked by
        c.setFont("Helvetica", 8)
        c.drawString(page_width-80, y_pos - 20, "( Checked By )")
        
        c.save()
        messagebox.showinfo("Success", f"Packing slip generated successfully!\nYour packing slip code is: {code}")
