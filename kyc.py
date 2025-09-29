from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox #pip
import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import tkinter as tk
from tkinter import scrolledtext, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import StringVar
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
from tkinter import filedialog
from reportlab.lib.units import inch
import tkinter as tk
from tkinter import scrolledtext, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import StringVar
class KYCclass:
    def __init__(self,root):
        self.root=root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width - 240  # Subtracting menu width (200) + padding (40)
        window_height = screen_height - 180  # Subtracting top margin (130) + bottom margin (50)
        x_position = 220  # Aligned with dashboard layout
        y_position = 130  # Aligned with dashboard layout
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.title("saravana fashion | developed by kamesh ")
        self.root.config(bg="#f0f0f0")
        self.root.overrideredirect(True)
        self.root.focus_force()



        #all variable 
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_kycid=StringVar()
        self.var_agencyname=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_pcode=StringVar()
        self.var_scode=StringVar()
        self.var_email=StringVar()
        self.var_GST=StringVar()
        self.var_utype=StringVar()
        self.var_address=StringVar()
        self.var_STATE=StringVar()
        self.var_trans=StringVar()
        self.var_transno=StringVar()
        self.var_dis=StringVar()


        

        #================.
        SearchFrame=LabelFrame(self.root,text="Search KYC",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="#f0f0f0")
        SearchFrame.place(x=250,y=20,width=600,height=70)
        #opiton===========

        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Name","Agencyname","Utype","Contact","pin code"),state='readonly',justify=CENTER,font=("time new roman",15),background='yellow')
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="white").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="lightblue",fg="black",cursor="hand2 ").place(x=410,y=10,width=150,height=30)


        #tile
        title=Label(self.root,text="KYC Details",font=("goudy old style",15),bg="#0f4d7d",fg='white').place(x=50,y=100,width=1000)
        #context
        #row1
        lbl_SID=Label(self.root,text="KYC ID",font=("goudy old style",15),bg="#f0f0f0").place(x=50,y=150)
        lbl_agencyname=Label(self.root,text="AGENCY NAME",font=("goudy old style",15),bg="#f0f0f0").place(x=350,y=150)
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="#f0f0f0").place(x=750,y=150)

        txt_SID=Entry(self.root,textvariable=self.var_kycid,font=("goudy old style",15),bg="white").place(x=150,y=150,width=180)
        txt_agencyname=Entry(self.root,textvariable=self.var_agencyname,font=("goudy old style",15),bg="white").place(x=500,y=150,width=180)
        #cmb_agencyname=ttk.Combobox(self.root,textvariable=self.var_agencyname,values=("Select","Male","Female","Transagencyname"),state='readonly',justify=CENTER,font=("time new roman",15))
        #cmb_agencyname.place(x=500,y=150,width=180)
        #cmb_agencyname.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="white").place(x=850,y=150,width=180)
        #row2
        
        
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="#f0f0f0").place(x=50,y=190)
        lbl_pcode=Label(self.root,text="Pin Code",font=("goudy old style",15),bg="#f0f0f0").place(x=350,y=190)
        lbl_scode=Label(self.root,text="State Code",font=("goudy old style",15),bg="#f0f0f0").place(x=750,y=190)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="white").place(x=150,y=190,width=180)
        txt_pcode=Entry(self.root,textvariable=self.var_pcode,font=("goudy old style",15),bg="white").place(x=500,y=190,width=180)
        txt_scode=Entry(self.root,textvariable=self.var_scode,font=("goudy old style",15),bg="white").place(x=850,y=190,width=180)
        

        #row3
        lbl_email=Label(self.root,text="Email",font=("goudy old style",15),bg="#f0f0f0").place(x=50,y=230)
        lbl_GST=Label(self.root,text="GST.No",font=("goudy old style",15),bg="#f0f0f0").place(x=350,y=230)
        lbl_usertype=Label(self.root,text=" Type",font=("goudy old style",15),bg="#f0f0f0").place(x=750,y=230)

        txt_email=Entry(self.root,textvariable=self.var_email,font=("goudy old style",15),bg="white").place(x=150,y=230,width=180)
        txt_GST=Entry(self.root,textvariable=self.var_GST,font=("goudy old style",15),bg="white").place(x=500,y=230,width=180)
        txt_usertype=Entry(self.root,textvariable=self.var_utype,font=("goudy old style",15),bg="white").place(x=850,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Select","Agent","Supplier","Distributor"),state='readonly',justify=CENTER,font=("time new roman",15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)


        #row4
        lbl_address=Label(self.root,text="ADDRESS",font=("goudy old style",15),bg="#f0f0f0").place(x=50,y=270)
        lbl_STATE=Label(self.root,text="STATE",font=("goudy old style",15),bg="#f0f0f0").place(x=470,y=270)
        lbl_STATE=Label(self.root,text="DISTRICT",font=("goudy old style",15),bg="#f0f0f0").place(x=750,y=270)
        lbl_trans=Label(self.root,text="TRANS NAME",font=("goudy old style",15),bg="#f0f0f0").place(x=50,y=350)
        txt_dis=Entry(self.root,textvariable=self.var_dis,font=("goudy old style",15),bg="white").place(x=850,y=270,width=180)
        


        self.txt_address = scrolledtext.ScrolledText(self.root, font=("Goudy Old Style", 15), bg="white")
        self.txt_address.place(x=150, y=270, width=300, height=60)

        
        





        txt_STATE=Entry(self.root,textvariable=self.var_STATE,font=("goudy old style",15),bg="white").place(x=550,y=270,width=180)
        txt_tran=Entry(self.root,textvariable=self.var_trans,font=("goudy old style",15),bg="white").place(x=200,y=350,width=180)

        #button
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2 ").place(x=500,y=350,width=110,height=28)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2 ").place(x=620,y=350,width=110,height=28)
        btn_delete=Button(self.root,text="Delete",command=self.Delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2 ").place(x=740,y=350,width=110,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2 ").place(x=860,y=350,width=110,height=28)
        btn_print=Button(self.root,text="Print",command = lambda:self.save_file(),font=("goudy old style",15),bg="gold",fg="white",cursor="hand2 ").place(x=980,y=350,width=110,height=28)



        #====details
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=400,relwidth=1,height=300)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)


        self.KYCTable=ttk.Treeview(emp_frame,columns=("kycid","name","agencyname","contact","email","pcode","scode","GST","utype","address","STATE","trans","dis"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.KYCTable.xview)
        scrolly.config(command=self.KYCTable.yview)
        self.KYCTable.heading("kycid",text="KYC ID")
        self.KYCTable.heading("name",text="NAME")
        
        self.KYCTable.heading("agencyname",text="AgencyName")
        self.KYCTable.heading("email",text="EMAIL")
        self.KYCTable.heading("contact",text="CONTACT")
        self.KYCTable.heading("GST",text="GST.No")
        self.KYCTable.heading("utype",text="TYPE")
        self.KYCTable.heading("pcode",text="Pin Code")
        self.KYCTable.heading("scode",text="State Code")
        
        
        self.KYCTable.heading("address",text="ADDRESS")
        self.KYCTable.heading("STATE",text="STATE")
        self.KYCTable.heading("trans",text="T.Name")
        self.KYCTable.heading("dis",text="DISTRICT")


        self.KYCTable["show"]="headings"
        


        self.KYCTable.column("kycid",width=90,anchor=CENTER)
        self.KYCTable.column("name",width=100,anchor=CENTER)
        self.KYCTable.column("email",width=100,anchor=CENTER)
        self.KYCTable.column("agencyname",width=100,anchor=CENTER)
        self.KYCTable.column("contact",width=100,anchor=CENTER)
        self.KYCTable.column("pcode",width=100,anchor=CENTER)
        self.KYCTable.column("scode",width=100,anchor=CENTER)
        self.KYCTable.column("GST",width=100,anchor=CENTER)
        self.KYCTable.column("utype",width=100,anchor=CENTER)
        self.KYCTable.column("address",width=100,anchor=CENTER)
        self.KYCTable.column("STATE",width=100,anchor=CENTER)
        
        self.KYCTable.column("trans",width=100,anchor=CENTER)
        self.KYCTable.column("dis",width=100,anchor=CENTER)
        self.KYCTable.pack(fill=BOTH,expand=1)
        self.KYCTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()


        




        #=======================
        

                
                

                 

            
                 
    
       





        





















    def add(self):
        con=sqlite3.connect(database='python\\ims.db')
        cur=con.cursor()
        try:
            if self.var_kycid.get()=="":
                messagebox.showerror("Error","Employee Id must be required",parent=self.root)
            else:
                cur.execute("Select * from kyc where kycid=?",(self.var_kycid.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This KYC ID already assigned try different")
                else:
                    cur.execute("Insert into kyc(kycid,name,email,agencyname,contact,pcode,scode,GST,utype,address,STATE,trans,dis) values(?,?,?,?,?,?,?,?,?,?,?,?,?)",(
                                        self.var_kycid.get(),
                                        self.var_name.get(),
                                        self.var_email.get(),
                                        self.var_agencyname.get(),
                                        self.var_contact.get(),
                                        self.var_pcode.get(),
                                        self.var_scode.get(),
                                        self.var_GST.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0',END),
                                        self.var_STATE.get(),
                                        self.var_trans.get(),
                                        self.var_dis.get()

                    ))
                    con.commit()
                    messagebox.showinfo("Sucess","KYC Added Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def show(self):
         con=sqlite3.connect(database='python\\ims.db')
         cur=con.cursor()
         try:
             cur.execute("Select * from kyc")
             rows=cur.fetchall()
             self.KYCTable.delete(*self.KYCTable.get_children())
             for row in rows:
                 self.KYCTable.insert('',END,values=row)
         
         except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
    def get_data(self,ev):
        f=self.KYCTable.focus()
        content=(self.KYCTable.item(f))
        row=content['values']
        print(row)
        self.var_kycid.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_agencyname.set(row[3])
        self.var_contact.set(row[4])
        self.var_pcode.set(row[5])
        self.var_scode.set(row[6])
        self.var_GST.set(row[7])
        self.var_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.var_STATE.set(row[10])
        self.var_trans.set(row[11])
        self.var_dis.set(row[12])

    def update(self):
        con=sqlite3.connect(database='python\\ims.db')
        cur=con.cursor()
        try:
            if self.var_kycid.get()==" ":
                messagebox.showerror("Error","KYC Id must be required",parent=self.root)
            else:
                cur.execute("Select * from kyc where kycid=?",(self.var_kycid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid KYC ID")
                else:
                    cur.execute("Update kyc set name=?,email=?,agencyname=?,contact=?,pcode=?,scode=?,GST=?,utype=?,address=?,STATE=?,trans=?,dis=? where kycid=?",(
                                        
                                        self.var_name.get(),
                                        self.var_email.get(),
                                        self.var_agencyname.get(),
                                        self.var_contact.get(),
                                        self.var_pcode.get(),
                                        self.var_scode.get(),
                                        self.var_GST.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0',END),
                                        self.var_STATE.get(),
                                        self.var_trans.get(),
                                        self.var_dis.get(),
                                        self.var_kycid.get(),


                    ))
                    con.commit()
                    messagebox.showinfo("Sucess","KYC Updated Successfully",parent=self.root)
                    self.show() 

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def Delete(self):
        con=sqlite3.connect(database='python\\ims.db')
        cur=con.cursor()
        try:
            if self.var_kycid.get()=="":
                messagebox.showerror("Error","KYC Id must be required",parent=self.root)
            else:
                cur.execute("Select * from kyc where kycid=?",(self.var_kycid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid KYC ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        
                        cur.execute("delete from kyc where kycid=?",(self.var_kycid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","KYC Deleted Successfully",parent=self.root)
                        self.show()


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to:{str(ex)}",parent=self.root)


    def clear(self):
        self.var_kycid.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_agencyname.set("")
        self.var_contact.set("")
        self.var_pcode.set("")
        self.var_scode.set("")
        self.var_GST.set("")
        self.var_utype.set(" ")
        self.txt_address.delete('1.0',END)
        self.var_STATE.set(" ")
        self.var_trans.set(" ")
        self.var_dis.set(" ")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                 messagebox.showerror("Error","Select Search By Option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                 messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("Select * from kyc where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.KYCTable.delete(*self.KYCTable.get_children())
                    for row in rows:
                        self.KYCTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","NO record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)



    def split_line(self, event):
        # Insert a newline character at the cursor position
        current_index = self.txt_address.index(INSERT)
        self.txt_address.insert(current_index, "\n")
        return "break"










 
    def save_file(self):
        file = filedialog.asksaveasfilename(
        filetypes=[("pdf file", ".pdf")],
        defaultextension=".pdf",
        initialfile=self.var_agencyname.get())
    

        self.save_pdf(file) # create and save the pdf in given path

    def save_pdf(self, my_path):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        # Create document with reduced margins
        doc = SimpleDocTemplate(
            my_path,
            pagesize=A4,
            rightMargin=20,
            leftMargin=20,
            topMargin=15,  # Reduced top margin
            bottomMargin=20
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Compact header style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#8a6844'),
            spaceAfter=5,  # Reduced spacing
            alignment=1
        )
        
        # Add company header
        elements.append(Paragraph("SARAVANA FASHION", title_style))
        
        # Company details in compact format
        company_data = [
            ["221/1, THILLAI NAGAR, FIRST STREET, DHARAPURAM ROAD, TIRUPUR - 641604"],
            ["Phone: 86088 97777 / 90878 82233  |  Email: kanizokids@gmail.com"],
            ["GSTIN: 33DULPS8136R1ZL  |  State: TAMIL NADU, State Code: 33"]
        ]
        
        company_table = Table(company_data, colWidths=[520])  # Slightly wider table
        company_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),  # Minimal padding
            ('TOPPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(company_table)
        elements.append(Spacer(1, 5))  # Minimal spacing
        
        # KYC Form title
        elements.append(Paragraph("KYC DETAILS", title_style))
        elements.append(Spacer(1, 5))  # Minimal spacing
        
        # Address handling
        address_text = self.txt_address.get('1.0', 'end-1c')
        
        # KYC details table
        kyc_data = [
            ['Field', 'Details'],
            ['KYC ID:', self.var_kycid.get()],
            ['Name:', self.var_name.get()],
            ['Agency Name:', self.var_agencyname.get()],
            ['Email:', self.var_email.get()],
            ['Contact:', self.var_contact.get()],
            ['GST No:', self.var_GST.get()],
            ['User Type:', self.var_utype.get()],
            ['State Code:', self.var_scode.get()],
            ['Pin Code:', self.var_pcode.get()],
            
            ['Address:', ''],
            [address_text, ''],
            ['District:', self.var_dis.get()],
            ['State:', self.var_STATE.get()]
        ]
        
        col_widths = [120, 400]  # Adjusted widths
        kyc_table = Table(kyc_data, colWidths=col_widths)
        
        table_style = TableStyle([
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3e2c7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#8a6844')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Borders
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            
            # Cell padding
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            
            # Field labels
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 1), (0, -1), 10),
            ('TEXTCOLOR', (0, 1), (0, -1), colors.HexColor('#666666')),
            
            # Details
            ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
            ('FONTSIZE', (1, 1), (1, -1), 12),
            
            # Address styling
            ('SPAN', (0, 11), (1, 11)),
            ('FONTSIZE', (0, 11), (1, 11), 12),
            ('TOPPADDING', (0, 11), (1, 11), 12),
            ('BOTTOMPADDING', (0, 11), (1, 11), 12),
        ])
        
        kyc_table.setStyle(table_style)
        elements.append(kyc_table)
        
        # Date and signature with reduced spacing
        elements.append(Spacer(1, 20))  # Reduced spacing

        
        # Build the PDF
        doc.build(elements)










            

if __name__ == "__main__":
    root = Tk()
    obj = KYCclass(root)
    root.mainloop()