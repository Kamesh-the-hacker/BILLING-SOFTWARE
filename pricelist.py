import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class InventoryManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x600")

        # Variables
        self.var_pid = tk.StringVar()
        self.var_cat = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_price = tk.StringVar()
        self.var_qty = tk.StringVar()
        self.var_size = tk.StringVar()
        self.var_series = tk.StringVar()

        # Database
        self.create_tables()

        # Product Frame
        product_frame = tk.LabelFrame(self.root, text="Product Details", font=("Arial", 12))
        product_frame.place(x=10, y=10, width=400, height=580)

        # Labels and Entry fields
        lbl_category = tk.Label(product_frame, text="Category", font=("Arial", 12))
        lbl_category.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.cmb_cat = ttk.Combobox(product_frame, textvariable=self.var_cat, font=("Arial", 12))
        self.cmb_cat.grid(row=0, column=1, padx=10, pady=10)
        self.cmb_cat['values'] = self.fetch_categories()

        lbl_name = tk.Label(product_frame, text="Name", font=("Arial", 12))
        lbl_name.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        txt_name = tk.Entry(product_frame, textvariable=self.var_name, font=("Arial", 12))
        txt_name.grid(row=1, column=1, padx=10, pady=10)

        lbl_price = tk.Label(product_frame, text="Price", font=("Arial", 12))
        lbl_price.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        txt_price = tk.Entry(product_frame, textvariable=self.var_price, font=("Arial", 12))
        txt_price.grid(row=2, column=1, padx=10, pady=10)

        lbl_qty = tk.Label(product_frame, text="Quantity", font=("Arial", 12))
        lbl_qty.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        txt_qty = tk.Entry(product_frame, textvariable=self.var_qty, font=("Arial", 12))
        txt_qty.grid(row=3, column=1, padx=10, pady=10)

        lbl_size = tk.Label(product_frame, text="Size", font=("Arial", 12))
        lbl_size.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.cmb_size = ttk.Combobox(product_frame, textvariable=self.var_size, font=("Arial", 12))
        self.cmb_size.grid(row=4, column=1, padx=10, pady=10)
        self.cmb_size['values'] = ('S', 'M', 'L', 'XL', 'XXL', '45', '50', '55', '60', '65', '70', '75', '80', '85', '90', '95', '100', '105', '110', '115')

        lbl_series = tk.Label(product_frame, text="Series", font=("Arial", 12))
        lbl_series.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.cmb_series = ttk.Combobox(product_frame, textvariable=self.var_series, font=("Arial", 12))
        self.cmb_series.grid(row=5, column=1, padx=10, pady=10)
        self.cmb_series['values'] = ('Baby', 'Adult', 'Number')

        # Buttons
        btn_add = tk.Button(product_frame, text="Add", command=self.add_product, font=("Arial", 12), bg="#2196f3", fg="white")
        btn_add.grid(row=6, column=0, padx=10, pady=10)

        btn_update = tk.Button(product_frame, text="Update", command=self.update_product, font=("Arial", 12), bg="#4caf50", fg="white")
        btn_update.grid(row=6, column=1, padx=10, pady=10)

        btn_delete = tk.Button(product_frame, text="Delete", command=self.delete_product, font=("Arial", 12), bg="#f44336", fg="white")
        btn_delete.grid(row=7, column=0, padx=10, pady=10)

        btn_clear = tk.Button(product_frame, text="Clear", command=self.clear_fields, font=("Arial", 12), bg="#607d8b", fg="white")
        btn_clear.grid(row=7, column=1, padx=10, pady=10)

        # Product Table
        table_frame = tk.Frame(self.root, bd=3, relief=tk.RIDGE)
        table_frame.place(x=420, y=10, width=770, height=580)

        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.product_table = ttk.Treeview(table_frame, columns=("pid", "category", "name", "price", "qty", "size", "series"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="PID")
        self.product_table.heading("category", text="Category")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Quantity")
        self.product_table.heading("size", text="Size")
        self.product_table.heading("series", text="Series")

        self.product_table["show"] = "headings"
        self.product_table.column("pid", width=50)
        self.product_table.column("category", width=100)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=70)
        self.product_table.column("qty", width=70)
        self.product_table.column("size", width=70)
        self.product_table.column("series", width=70)

        self.product_table.pack(fill=tk.BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        # Price List Button
        btn_price_list = tk.Button(self.root, text="Price List", command=self.open_price_list, font=("Arial", 12), bg="#ff9800", fg="white")
        btn_price_list.place(x=10, y=550, width=100, height=30)

        self.show_products()

    def create_tables(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products
                         (pid INTEGER PRIMARY KEY,
                          category TEXT,
                          name TEXT,
                          price REAL,
                          qty INTEGER,
                          size TEXT,
                          series TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS price_list
                         (id INTEGER PRIMARY KEY,
                          product_id INTEGER,
                          size_series TEXT,
                          price REAL,
                          FOREIGN KEY (product_id) REFERENCES products(pid))''')
        conn.commit()
        conn.close()

    def fetch_categories(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM products")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories

    def add_product(self):
        if self.var_cat.get() == "" or self.var_name.get() == "" or self.var_price.get() == "" or self.var_qty.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('inventory.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO products (category, name, price, qty, size, series) VALUES (?, ?, ?, ?, ?, ?)",
                               (self.var_cat.get(), self.var_name.get(), self.var_price.get(), self.var_qty.get(), self.var_size.get(), self.var_series.get()))
                conn.commit()
                self.show_products()
                self.clear_fields()
                messagebox.showinfo("Success", "Product added successfully", parent=self.root)
                conn.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show_products(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM products")
            rows = cursor.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', tk.END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()

    def get_data(self, ev):
        f = self.product_table.focus()
        content = self.product_table.item(f)
        row = content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_name.set(row[2])
        self.var_price.set(row[3])
        self.var_qty.set(row[4])
        self.var_size.set(row[5])
        self.var_series.set(row[6])

    def update_product(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('inventory.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET category=?, name=?, price=?, qty=?, size=?, series=? WHERE pid=?",
                               (self.var_cat.get(), self.var_name.get(), self.var_price.get(), self.var_qty.get(),
                                self.var_size.get(), self.var_series.get(), self.var_pid.get()))
                conn.commit()
                self.show_products()
                self.clear_fields()
                messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
                conn.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete_product(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('inventory.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE pid=?", (self.var_pid.get(),))
                conn.commit()
                self.show_products()
                self.clear_fields()
                messagebox.showinfo("Success", "Product deleted successfully", parent=self.root)
                conn.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear_fields(self):
        self.var_pid.set("")
        self.var_cat.set("")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_size.set("")
        self.var_series.set("")

    def open_price_list(self):
        price_list_window = tk.Toplevel(self.root)
        price_list_window.title("Price List")
        price_list_window.geometry("600x400")

        # Product selection
        lbl_product = tk.Label(price_list_window, text="Select Product:", font=("Arial", 12))
        lbl_product.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.cmb_price_product = ttk.Combobox(price_list_window, font=("Arial", 12))
        self.cmb_price_product.grid(row=0, column=1, padx=10, pady=10)
        self.cmb_price_product['values'] = self.fetch_products()
        self.cmb_price_product.bind("<<ComboboxSelected>>", self.update_size_series)

        # Size/Series selection
        lbl_size_series = tk.Label(price_list_window, text="Size/Series:", font=("Arial", 12))
        lbl_size_series.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.cmb_price_size_series = ttk.Combobox(price_list_window, font=("Arial", 12))
        self.cmb_price_size_series.grid(row=1, column=1, padx=10, pady=10)

        # Price entry
        lbl_price = tk.Label(price_list_window, text="Price:", font=("Arial", 12))
        lbl_price.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.txt_price_list_price = tk.Entry(price_list_window, font=("Arial", 12))
        self.txt_price_list_price.grid(row=2, column=1, padx=10, pady=10)

        # Add Price button
        btn_add_price = tk.Button(price_list_window, text="Add Price", command=self.add_price, font=("Arial", 12), bg="#4caf50", fg="white")
        btn_add_price.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Price List Table
        table_frame = tk.Frame(price_list_window, bd=3, relief=tk.RIDGE)
        table_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.price_table = ttk.Treeview(table_frame, columns=("id", "product", "size_series", "price"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_y.config(command=self.price_table.yview)

        self.price_table.heading("id", text="ID")
        self.price_table.heading("product", text="Product")
        self.price_table.heading("size_series", text="Size/Series")
        self.price_table.heading("price", text="Price")

        self.price_table["show"] = "headings"
        self.price_table.column("id", width=50)
        self.price_table.column("product", width=200)
        self.price_table.column("size_series", width=100)
        self.price_table.column("price", width=100)

        self.price_table.pack(fill=tk.BOTH, expand=1)

        self.show_price_list()

    def fetch_products(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM products")
        products = [row[0] for row in cursor.fetchall()]
        conn.close()
        return products

    def update_size_series(self, event):
        selected_product = self.cmb_price_product.get()
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT size, series FROM products WHERE name=?", (selected_product,))
        result = cursor.fetchone()
        conn.close()
        if result:
            size, series = result
            if series == 'Number':
                self.cmb_price_size_series['values'] = [f"{i}" for i in range(45, 120, 5)]
            elif series == 'Baby':
                self.cmb_price_size_series['values'] = ['S', 'M', 'L', 'XL', 'XXL']
            else:
                self.cmb_price_size_series['values'] = ['S', 'M', 'L', 'XL', 'XXL', 'XXXL']

    def add_price(self):
        product = self.cmb_price_product.get()
        size_series = self.cmb_price_size_series.get()
        price = self.txt_price_list_price.get()

        if product == "" or size_series == "" or price == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('inventory.db')
                cursor = conn.cursor()
                cursor.execute("SELECT pid FROM products WHERE name=?", (product,))
                product_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO price_list (product_id, size_series, price) VALUES (?, ?, ?)",
                               (product_id, size_series, price))
                conn.commit()
                self.show_price_list()
                messagebox.showinfo("Success", "Price added successfully", parent=self.root)
                conn.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show_price_list(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT price_list.id, products.name, price_list.size_series, price_list.price
                FROM price_list
                JOIN products ON price_list.product_id = products.pid
            """)
            rows = cursor.fetchall()
            self.price_table.delete(*self.price_table.get_children())
            for row in rows:
                self.price_table.insert('', tk.END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    obj = InventoryManagement(root)
    root.mainloop()