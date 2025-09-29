from tkinter import*
import tkinter as tk

from PIL import Image,ImageTk
from tkinter import ttk,messagebox #pip
import sqlite3
from tkinter import *
from tkinter import ttk

class productclass:
    def __init__(self,root):
        super().__init__()
        self.root=root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width - 240  # Subtracting menu width (200) + padding (40)
        window_height = screen_height - 180  # Subtracting top margin (130) + bottom margin (50)
        x_position = 220  # Aligned with dashboard layout
        y_position = 130  # Aligned with dashboard layout
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.title("saravana fashion | devloped by kamesh")
        self.root.config(bg="#f0f0f0")
        self.root.overrideredirect(True)
        
        self.root.focus_force()


        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.cat_list=[]
        self.fetch_cat()
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_price2=StringVar()
        
        self.var_price3=StringVar()
        self.var_price4=StringVar()
        self.var_price5=StringVar()
        self.var_size=StringVar()
        self.var_qty=StringVar()
        
        


        #====================
        product_frame=Frame(self.root,bd=2,relief=RIDGE,bg='#f0f0f0')
        product_frame.place(x=10,y=20,width=450,height=630)
        #tile
        title=Label(product_frame,text="Manage Products Details",font=("goudy old style",18),bg="#0f4d7d",fg='white').pack(side=TOP,fill=X)

        lbl_category=Label(product_frame,text="Category",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=40)
        
        lbl_product_name=Label(product_frame,text="Name",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=90)
        lbl_price=Label(product_frame,text="Price",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=130)
        lbl_price2=Label(product_frame,text="Price2",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=170)
        
        lbl_price3=Label(product_frame,text="Price3",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=210)
        lbl_price4=Label(product_frame,text="Price4",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=250)
        lbl_price5=Label(product_frame,text="Price5",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=290)
        lbl_qty=Label(product_frame,text="Quantity",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=330)
        lbl_size=Label(product_frame,text="Size",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=380)



        txt_category=Label(product_frame,text="Category",font=("goudy old style",18),bg="#f0f0f0").place(x=30,y=40)
        #option
        
        
        
        
        self.cmb_cat=ttk.Combobox(product_frame,textvariable=self.var_cat,values=self.cat_list,font=("time new roman",15))
        self.cmb_cat['values'] = self.cat_list
        self.cmb_cat.place(x=150,y=40,width=200)
    
        self.cmb_cat.bind("<KeyRelease>", self.filter_combobox)
        self.cmb_cat.current(0)





        
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="white").place(x=160,y=110,width=200)
        txt_price=Entry(self.root,textvariable=self.var_price,font=("goudy old style",15),bg="white").place(x=160,y=150,width=200)
        txt_price2=Entry(self.root,textvariable=self.var_price2,font=("goudy old style",15),bg="white").place(x=160,y=190,width=200)

        txt_price3=Entry(self.root,textvariable=self.var_price3,font=("goudy old style",15),bg="white").place(x=160,y=230,width=200)
        txt_price4=Entry(self.root,textvariable=self.var_price4,font=("goudy old style",15),bg="white").place(x=160,y=270,width=200)
        txt_price5=Entry(self.root,textvariable=self.var_price5,font=("goudy old style",15),bg="white").place(x=160,y=310,width=200)
        txt_qty=Entry(self.root,textvariable=self.var_qty,font=("goudy old style",15),bg="white").place(x=160,y=350,width=200)
        cmb_size=ttk.Combobox(product_frame,textvariable=self.var_size,values=("Select",'0','40','45','50','55','60','65','70','75','80','85','90','95','100','105','110','S','M','L','XL','XXL','XXXL'),state='readonly',justify=CENTER,font=("time new roman",15))
        cmb_size.place(x=150,y=380,width=200)
        cmb_size.current(0)
        
        
        #buttton============
        btn_add=Button(product_frame,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2 ").place(x=10,y=520,width=100,height=40)
        btn_update=Button(product_frame,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2 ").place(x=120,y=520,width=100,height=40)
        btn_delete=Button(product_frame,text="Delete",command=self.Delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2 ").place(x=230,y=520,width=100,height=40)
        btn_clear=Button(product_frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2 ").place(x=340,y=520,width=100,height=40)
        
        #================
        SearchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=800,height=80)
        #opiton===========#================================
       
        
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Name"),state='readonly',justify=CENTER,font=("time new roman",15))
        
        cmb_search.place(x=10,y=10,width=180)
        

        cmb_search.current(0)

        

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="white").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="lightblue",fg="black",cursor="hand2 ").place(x=410,y=10,width=150,height=30)
        
        #product detail==============================================
        p_frame=Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=800,height=550)

        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)


        self.productTable=ttk.Treeview(p_frame,columns=("pid","category","name","price","price2",'price3','price4','price5','qty','size'),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        self.productTable.heading("pid",text="P ID")
        self.productTable.heading("category",text="Category")
        self.productTable.heading("name",text="Name")
        self.productTable.heading("price",text="Price")
        self.productTable.heading("price2",text="Price2")
        
        self.productTable.heading("price3",text="Price3")
        self.productTable.heading("price4",text="Price4")
        self.productTable.heading("price5",text="Price5")
        self.productTable.heading("price4",text="price4")
        self.productTable.heading("qty",text="QTY")
        self.productTable.heading("size",text="Size")
        self.productTable["show"]="headings"


        self.productTable.column("pid",width=50,anchor=CENTER)
        self.productTable.column("category",width=150,anchor=CENTER)
        self.productTable.column("name",width=150,anchor=CENTER)
        self.productTable.column("price",width=70,anchor=CENTER)
        self.productTable.column("price2",width=70,anchor=CENTER)
        
        self.productTable.column("price3",width=70,anchor=CENTER)
        self.productTable.column("price4",width=70,anchor=CENTER)
        self.productTable.column("price5",width=70,anchor=CENTER)
        self.productTable.column("qty",width=70,anchor=CENTER)
        self.productTable.column("size",width=70,anchor=CENTER)

        self.productTable.pack(fill=BOTH,expand=1)
        self.productTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        


        #=============
    def fetch_cat(self):
        con=sqlite3.connect(database='python\\ims.db')
        cur=con.cursor()
        self.cat_list.append("Empty")
        try:
            cur.execute("Select name from category")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("")

                for i in cat:
                    self.cat_list.append(i[0])
            





        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)





     #============================
    def add(self):
        con = sqlite3.connect(database='python\\ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                # Find the next available product ID
                cur.execute("SELECT MAX(pid) FROM product")
                max_pid = cur.fetchone()[0]
                if max_pid is None:  # No products yet
                    new_pid = 1
                else:
                    # Create a list of existing product IDs
                    cur.execute("SELECT pid FROM product")
                    existing_ids = [row[0] for row in cur.fetchall()]
                    # Find the lowest available ID
                    new_pid = 1
                    while new_pid in existing_ids:
                        new_pid += 1

                # Check for existing product by name
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                if 1==0:
                    messagebox.showerror("Error", "This product already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO product (pid, category, name, price1, price2, price3, price4, price5, qty, size) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        new_pid,
                        self.var_cat.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_price2.get(),
                        self.var_price3.get(),
                        self.var_price4.get(),
                        self.var_price5.get(),
                        self.var_qty.get(),
                        self.var_size.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product added successfully", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()



    def show(self):
         con=sqlite3.connect(database='python\\ims.db')
         cur=con.cursor()
         try:
             cur.execute("Select * from product")
             rows=cur.fetchall()
             self.productTable.delete(*self.productTable.get_children())
             for row in rows:
                 self.productTable.insert('',END,values=row)
         
         except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']
        print(row)
        self.var_pid.set(row[0])
        
        self.var_cat.set(row[1])
        self.var_name.set(row[2])
        self.var_price.set(row[3])
        self.var_price2.set(row[4])
        
        self.var_price3.set(row[5])
        self.var_price4.set(row[6])
        self.var_price5.set(row[7])
        self.var_qty.set(row[8])
        self.var_size.set(row[9])
        


    def update(self):
        con=sqlite3.connect(database='python\\ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product")
                else:
                    cur.execute("Update product set category=?,name=?,price1=?,price2=?,price3=?,price4=?,price5=?,qty=?,size=? where pid=?",(
                                        self.var_cat.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_price2.get(),
                                        
                                        self.var_price3.get(),
                                        self.var_price4.get(),
                                        self.var_price5.get(),
                                        self.var_qty.get(),

                                        self.var_size.get(),
                                        self.var_pid.get()
                                     


                                        ))
                    con.commit()
                    messagebox.showinfo("Sucess","Product Updated Successfully",parent=self.root)
                    self.show() 

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def Delete(self):
        con=sqlite3.connect(database='python\\ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select product from the list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.show()


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)

    def clear(self):
        self.var_cat.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        
        self.var_price2.set("")
        self.var_size.set("")
        self.var_price3.set("")
        self.var_price4.set("")
        self.var_price5.set("")
        self.var_qty.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()
    def search(self):
        con=sqlite3.connect(database='python\\ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                 messagebox.showerror("Error","Select Search By Option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                 messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("Select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","NO record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)



    def filter_combobox(self,event):
        input_text = self.cmb_cat.get().lower()
        filtered_categories = [cat for cat in self.cat_list if input_text.lower() in cat.lower()]

    # Update the combobox values
        self.cmb_cat['values'] = filtered_categories
        if filtered_categories:
            self.cmb_cat.current(0)  # Set to the first item in the filtered list
        else:
            self.cmb_cat.set("")  











    
            




    

        























if __name__ == "__main__":
    root = Tk()
    app=productclass(root)
    obj = productclass(root)
    root.mainloop()