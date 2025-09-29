from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class categoryclass:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width - 240  # Subtracting menu width (200) + padding (40)
        window_height = screen_height - 180  # Subtracting top margin (130) + bottom margin (50)
        x_position = 220  # Aligned with dashboard layout
        y_position = 130  # Aligned with dashboard layout
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.overrideredirect(True)
        self.root.title("Textile Management System | Developed by Kamesh")
        self.root.config(bg="#f0f0f0")
        self.root.overrideredirect(True)
        self.root.focus_force()
        
        # Variables
        self.var_name = StringVar()
        self.var_cat_id = StringVar()

        # Title
        lbl_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30), bg="#184a45", fg='white', bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)
        
        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 30), bg="#f0f0f0")
        lbl_name.place(x=50, y=100)
        
        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 25), bg="white")
        txt_name.place(x=50, y=170, width=300)
        
        btn_add = Button(self.root, text="ADD", command=self.add, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_add.place(x=360, y=170, width=150, height=30)
        
        btn_delete = Button(self.root, text="Delete", command=self.Delete, font=("goudy old style", 15), bg="red", fg="white", cursor="hand2")
        btn_delete.place(x=520, y=170, width=150, height=30)

        # Category Details
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=550, height=550)
        
        Scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.categoryTable = ttk.Treeview(cat_frame, columns=("cid", "name"), yscrollcommand=Scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        Scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.categoryTable.xview)
        Scrolly.config(command=self.categoryTable.yview)

        self.categoryTable.heading("cid", text="C ID")
        self.categoryTable.heading("name", text="Name")
        self.categoryTable['show'] = 'headings'
        self.categoryTable.column('cid', width=10, anchor=CENTER)
        self.categoryTable.column('name', width=300, anchor=CENTER)
        self.categoryTable.pack(fill=BOTH, expand=1)
        self.categoryTable.bind("<ButtonRelease-1>", self.get_data)

        # Image
        self.im1 = Image.open("cat.jpeg")
        self.im1 = self.im1.resize((620, 400), Image.Resampling.LANCZOS)
        self.im1 = ImageTk.PhotoImage(self.im1)

        self.lbl_im1 = Label(self.root, image=self.im1, bd=2, relief=RAISED)
        self.lbl_im1.place(x=50, y=220)
        
        self.show()

    def add(self):
        con = sqlite3.connect(database='python\\ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category Name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Category is already assigned. Try a different name.")
                else:
                    # Fetch the minimum CID that is not currently in use
                    cur.execute("SELECT MIN(cid) FROM category")
                    min_cid = cur.fetchone()[0]
                    if min_cid is None:  # If there are no categories, start from 1
                        new_cid = 1
                    else:
                        # Check the next available CID
                        while True:
                            if min_cid not in [r[0] for r in cur.execute("SELECT cid FROM category").fetchall()]:
                                new_cid = min_cid
                                break
                            min_cid += 1

                    cur.execute("INSERT INTO category(cid, name) VALUES(?, ?)", (new_cid, self.var_name.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

        self.show()

    def show(self):
        con = sqlite3.connect(database='python\\ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.categoryTable.delete(*self.categoryTable.get_children())
            for row in rows:
                self.categoryTable.insert('', END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.categoryTable.focus()
        content = (self.categoryTable.item(f))
        row = content['values']
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def Delete(self):
        con = sqlite3.connect(database='python\\ims.db')
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category must be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Category", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                        self.show()
                        self.var_cat_id.set('')
                        self.var_name.set('')

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = categoryclass(root)
    root.mainloop()
