from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkcalendar import DateEntry
import seaborn as sns
from PIL import Image, ImageTk
import os
import calendar

class AccountsDashboard:
    def __init__(self, root):
        self.root = root
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width - 240
        window_height = screen_height - 180
        x_position = 220
        y_position = 130
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.title("Saravana Fashion | Accounts Dashboard")
        self.root.config(bg="#f0f0f0")
        self.root.overrideredirect(True)
        self.root.focus_force()
        
        # Database connection
        self.conn = sqlite3.connect('python\\ims.db')
        self.cursor = self.conn.cursor()
        
        # Variables
        self.var_year = StringVar()
        self.var_month = StringVar()
        self.var_search = StringVar()
        self.var_filter = StringVar()
        self.var_date_from = StringVar()
        self.var_date_to = StringVar()
        
        # Set default values
        current_year = datetime.now().year
        current_month = datetime.now().month
        self.var_year.set(str(current_year))
        self.var_month.set(calendar.month_name[current_month])
        
        # Load initial data
        self.years = self.fetch_available_years()
        self.months = ["January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        
        # Main Frame
        main_frame = Frame(self.root, bd=2, relief=RIDGE, bg='#f0f0f0')
        main_frame.place(x=10, y=10, width=window_width-20, height=window_height-20)
        
        # Title with Logo
        title_frame = Frame(main_frame, bg="#2C3E50", height=70)
        title_frame.pack(fill=X)
        
        # Try to load the logo
        try:
            logo_img = Image.open("python/icon__2_-removebg-preview.png")
            logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            Label(title_frame, image=self.logo_photo, bg="#2C3E50").place(x=20, y=10)
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        Label(title_frame, text="ACCOUNTS DASHBOARD", font=("Helvetica", 24, "bold"), 
              bg="#2C3E50", fg="white").place(x=80, y=18)
        
        # Exit Button
        Button(title_frame, text="✕", command=self.root.destroy, 
               font=("Arial", 14), bg="#E74C3C", fg="white", bd=0, 
               cursor="hand2").place(x=window_width-60, y=18, width=30, height=30)
        
        # Control Frame
        control_frame = Frame(main_frame, bg="#f0f0f0", bd=2, relief=RIDGE)
        control_frame.place(x=10, y=80, width=window_width-40, height=80)
        
        # Year Selection
        Label(control_frame, text="Select Year:", font=("Helvetica", 12), 
              bg="#f0f0f0").place(x=20, y=25)
        cmb_year = ttk.Combobox(control_frame, textvariable=self.var_year, 
                               values=self.years, font=("Helvetica", 12), state="readonly")
        cmb_year.place(x=120, y=25, width=120)
        cmb_year.bind("<<ComboboxSelected>>", self.update_dashboard)
        
        # Month Selection
        Label(control_frame, text="Select Month:", font=("Helvetica", 12), 
              bg="#f0f0f0").place(x=260, y=25)
        cmb_month = ttk.Combobox(control_frame, textvariable=self.var_month, 
                               values=self.months, font=("Helvetica", 12), state="readonly")
        cmb_month.place(x=370, y=25, width=150)
        cmb_month.bind("<<ComboboxSelected>>", self.update_dashboard)
        
        # Date Range
        Label(control_frame, text="Date From:", font=("Helvetica", 12), 
              bg="#f0f0f0").place(x=540, y=25)
        self.date_from = DateEntry(control_frame, width=12, background='#2C3E50',
                                  foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy',
                                  textvariable=self.var_date_from, font=("Helvetica", 12))
        self.date_from.place(x=630, y=25, width=120)
        
        Label(control_frame, text="To:", font=("Helvetica", 12), 
              bg="#f0f0f0").place(x=760, y=25)
        self.date_to = DateEntry(control_frame, width=12, background='#2C3E50',
                                foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy',
                                textvariable=self.var_date_to, font=("Helvetica", 12))
        self.date_to.place(x=790, y=25, width=120)
        
        Button(control_frame, text="Filter", command=self.filter_by_date, 
               font=("Helvetica", 12), bg="#2980B9", fg="white", cursor="hand2").place(x=920, y=25, width=80)
        
        Button(control_frame, text="Export Data", command=self.export_data, 
               font=("Helvetica", 12), bg="#27AE60", fg="white", cursor="hand2").place(x=1010, y=25, width=120)
        
        # Content Frame - This will contain both summary cards and visualizations
        self.content_frame = Frame(main_frame, bg="#f0f0f0")
        self.content_frame.place(x=10, y=170, width=window_width-40, height=window_height-210)
        
        # Initialize the dashboard
        self.create_summary_cards()
        self.create_visualizations()
        self.create_invoice_table()
    
    def fetch_available_years(self):
        """Fetch available years from billing data"""
        try:
            self.cursor.execute("SELECT DISTINCT strftime('%Y', date) FROM billing ORDER BY date DESC")
            years = [year[0] for year in self.cursor.fetchall()]
            if not years:  # If no data, provide current year as fallback
                years = [str(datetime.now().year)]
            return years
        except Exception as e:
            print(f"Error fetching years: {e}")
            return [str(datetime.now().year)]
    
    def create_summary_cards(self):
        """Create financial summary cards"""
        # Summary Frame
        summary_frame = Frame(self.content_frame, bg="#f0f0f0")
        summary_frame.place(x=0, y=0, width=self.content_frame.winfo_width(), height=120)
        
        # Get financial data
        financial_data = self.get_financial_data()
        
        # Create card frames
        card_width = (self.content_frame.winfo_width() - 60) // 4
        
        # Total Revenue Card
        revenue_card = Frame(summary_frame, bg="white", bd=1, relief=RIDGE)
        revenue_card.place(x=10, y=10, width=card_width, height=100)
        
        Label(revenue_card, text="Total Revenue", font=("Helvetica", 12), 
              bg="white", fg="#333").place(x=10, y=10)
        Label(revenue_card, text=f"₹{financial_data['total_revenue']:,.2f}", 
              font=("Helvetica", 18, "bold"), bg="white", fg="#16a34a").place(x=10, y=40)
        
        # Add comparison with previous period
        prev_diff = financial_data.get('revenue_growth', 0)
        diff_color = "#16a34a" if prev_diff >= 0 else "#dc2626"
        diff_symbol = "+" if prev_diff >= 0 else ""
        Label(revenue_card, text=f"{diff_symbol}{prev_diff:.1f}% vs prev period", 
              font=("Helvetica", 10), bg="white", fg=diff_color).place(x=10, y=70)
        
        # Total Expenses Card
        expenses_card = Frame(summary_frame, bg="white", bd=1, relief=RIDGE)
        expenses_card.place(x=20 + card_width, y=10, width=card_width, height=100)
        
        Label(expenses_card, text="Total Expenses", font=("Helvetica", 12), 
              bg="white", fg="#333").place(x=10, y=10)
        Label(expenses_card, text=f"₹{financial_data['total_expenses']:,.2f}", 
              font=("Helvetica", 18, "bold"), bg="white", fg="#dc2626").place(x=10, y=40)
        
        prev_diff = financial_data.get('expenses_growth', 0)
        diff_color = "#dc2626" if prev_diff >= 0 else "#16a34a"
        diff_symbol = "+" if prev_diff >= 0 else ""
        Label(expenses_card, text=f"{diff_symbol}{prev_diff:.1f}% vs prev period", 
              font=("Helvetica", 10), bg="white", fg=diff_color).place(x=10, y=70)
        
        # Net Profit Card
        profit_card = Frame(summary_frame, bg="white", bd=1, relief=RIDGE)
        profit_card.place(x=30 + card_width*2, y=10, width=card_width, height=100)
        
        Label(profit_card, text="Net Profit", font=("Helvetica", 12), 
              bg="white", fg="#333").place(x=10, y=10)
        Label(profit_card, text=f"₹{financial_data['net_profit']:,.2f}", 
              font=("Helvetica", 18, "bold"), bg="white", fg="#2563eb").place(x=10, y=40)
        
        prev_diff = financial_data.get('profit_growth', 0)
        diff_color = "#16a34a" if prev_diff >= 0 else "#dc2626"
        diff_symbol = "+" if prev_diff >= 0 else ""
        Label(profit_card, text=f"{diff_symbol}{prev_diff:.1f}% vs prev period", 
              font=("Helvetica", 10), bg="white", fg=diff_color).place(x=10, y=70)
        
        # Invoice Count Card
        invoice_card = Frame(summary_frame, bg="white", bd=1, relief=RIDGE)
        invoice_card.place(x=40 + card_width*3, y=10, width=card_width, height=100)
        
        Label(invoice_card, text="Total Invoices", font=("Helvetica", 12), 
              bg="white", fg="#333").place(x=10, y=10)
        Label(invoice_card, text=f"{financial_data['invoice_count']}", 
              font=("Helvetica", 18, "bold"), bg="white", fg="#7c3aed").place(x=10, y=40)
        
        prev_diff = financial_data.get('invoice_growth', 0)
        diff_color = "#16a34a" if prev_diff >= 0 else "#dc2626"
        diff_symbol = "+" if prev_diff >= 0 else ""
        Label(invoice_card, text=f"{diff_symbol}{prev_diff:.1f}% vs prev period", 
              font=("Helvetica", 10), bg="white", fg=diff_color).place(x=10, y=70)
    
    def create_visualizations(self):
        """Create data visualizations"""
        # Visualization Frame
        viz_frame = Frame(self.content_frame, bg="white", bd=1, relief=RIDGE)
        viz_frame.place(x=0, y=130, width=self.content_frame.winfo_width() // 2 - 5, height=300)
        
        Label(viz_frame, text="Monthly Revenue Trends", font=("Helvetica", 14, "bold"), 
              bg="white").pack(anchor=W, padx=10, pady=10)
        
        # Generate monthly data
        monthly_data = self.get_monthly_data()
        
        # Create matplotlib figure
        plt.style.use('seaborn-v0_8-whitegrid')
        self.fig_monthly, self.ax_monthly = plt.subplots(figsize=(8, 4))
        
        months = monthly_data['month']
        revenue = monthly_data['revenue']
        expenses = monthly_data['expenses']
        profit = monthly_data['profit']
        
        x = np.arange(len(months))
        bar_width = 0.25
        
        self.ax_monthly.bar(x - bar_width, revenue, bar_width, label='Revenue', color='#4F46E5')
        self.ax_monthly.bar(x, expenses, bar_width, label='Expenses', color='#F59E0B')
        self.ax_monthly.bar(x + bar_width, profit, bar_width, label='Profit', color='#10B981')
        
        self.ax_monthly.set_xticks(x)
        self.ax_monthly.set_xticklabels(months, rotation=45)
        self.ax_monthly.set_ylabel('Amount (₹)')
        self.ax_monthly.legend()
        self.ax_monthly.grid(axis='y', linestyle='--', alpha=0.7)
        self.fig_monthly.tight_layout()
        
        # Add the plot to the Tkinter window
        self.canvas_monthly = FigureCanvasTkAgg(self.fig_monthly, master=viz_frame)
        self.canvas_monthly.draw()
        self.canvas_monthly.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Visualization Frame 2 - For Pie Chart
        viz_frame2 = Frame(self.content_frame, bg="white", bd=1, relief=RIDGE)
        viz_frame2.place(x=self.content_frame.winfo_width() // 2 + 5, y=130, 
                         width=self.content_frame.winfo_width() // 2 - 5, height=300)
        
        Label(viz_frame2, text="Revenue Distribution by Category", font=("Helvetica", 14, "bold"), 
              bg="white").pack(anchor=W, padx=10, pady=10)
        
        # Generate category data
        category_data = self.get_category_distribution()
        
        # Create matplotlib pie chart
        self.fig_pie, self.ax_pie = plt.subplots(figsize=(6, 4))
        
        categories = category_data['category']
        amounts = category_data['amount']
        
        colors = ['#4F46E5', '#F59E0B', '#10B981', '#EC4899', '#8B5CF6', '#F43F5E']
        explode = [0.1 if i == amounts.index(max(amounts)) else 0 for i in range(len(amounts))]
        
        self.ax_pie.pie(amounts, explode=explode, labels=categories, colors=colors, 
                        autopct='%1.1f%%', shadow=True, startangle=90)
        self.ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        self.fig_pie.tight_layout()
        
        # Add the pie chart to the Tkinter window
        self.canvas_pie = FigureCanvasTkAgg(self.fig_pie, master=viz_frame2)
        self.canvas_pie.draw()
        self.canvas_pie.get_tk_widget().pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def create_invoice_table(self):
        """Create invoice data table"""
        table_frame = Frame(self.content_frame, bg="white", bd=1, relief=RIDGE)
        table_frame.place(x=0, y=440, width=self.content_frame.winfo_width(), 
                          height=self.content_frame.winfo_height() - 440)
        
        # Table title and search bar
        title_frame = Frame(table_frame, bg="white")
        title_frame.pack(fill=X, padx=10, pady=10)
        
        Label(title_frame, text="Invoice Details", font=("Helvetica", 14, "bold"), 
              bg="white").pack(side=LEFT)
        
        # Search Frame
        search_frame = Frame(title_frame, bg="white")
        search_frame.pack(side=RIGHT)
        
        Label(search_frame, text="Search:", font=("Helvetica", 12), bg="white").pack(side=LEFT, padx=(0, 5))
        Entry(search_frame, textvariable=self.var_search, font=("Helvetica", 12), 
              width=20).pack(side=LEFT, padx=(0, 5))
        Button(search_frame, text="Search", command=self.search_invoices, 
               font=("Helvetica", 10), bg="#2980B9", fg="white", cursor="hand2").pack(side=LEFT)
        
        # Create Treeview
        columns = ('Invoice ID', 'Customer', 'Date', 'Total Amount', 'Status')
        self.invoice_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        # Configure column widths
        self.invoice_tree.column('Invoice ID', width=100, anchor=CENTER)
        self.invoice_tree.column('Customer', width=200, anchor=W)
        self.invoice_tree.column('Date', width=120, anchor=CENTER)
        self.invoice_tree.column('Total Amount', width=150, anchor=E)
        self.invoice_tree.column('Status', width=100, anchor=CENTER)
        
        # Configure column headings
        for col in columns:
            self.invoice_tree.heading(col, text=col)
        
        # Add scrollbars
        scrolly = Scrollbar(table_frame, orient=VERTICAL, command=self.invoice_tree.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        self.invoice_tree.config(yscrollcommand=scrolly.set)
        
        scrollx = Scrollbar(table_frame, orient=HORIZONTAL, command=self.invoice_tree.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        self.invoice_tree.config(xscrollcommand=scrollx.set)
        
        self.invoice_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        
        # Bind double-click event to view invoice details
        self.invoice_tree.bind("<Double-1>", self.view_invoice_details)
        
        # Populate the table with data
        self.load_invoice_data()
    
    def load_invoice_data(self):
        """Load invoice data into the table"""
        # Clear existing data
        for item in self.invoice_tree.get_children():
            self.invoice_tree.delete(item)
        
        # Get selected year and month
        selected_year = self.var_year.get()
        selected_month = self.var_month.get()
        
        # Convert month name to number
        month_num = {name: idx for idx, name in enumerate(self.months, 1)}.get(selected_month, None)
        
        # Query based on filters
        try:
            query = """
                SELECT id, customer_name, date, total_amount, 
                CASE WHEN payment_status IS NULL THEN 'Pending' ELSE payment_status END as status
                FROM billing
                WHERE strftime('%Y', date) = ?
            """
            params = [selected_year]
            
            if month_num:
                query += " AND strftime('%m', date) = ?"
                params.append(f"{month_num:02d}")
            
            query += " ORDER BY date DESC"
            
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            
            for row in rows:
                invoice_id, customer, date, amount, status = row
                
                # Format amount with commas for thousands
                formatted_amount = f"₹{float(amount):,.2f}" if amount else "₹0.00"
                
                # Convert date format
                try:
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%d-%b-%Y")
                except:
                    formatted_date = date
                
                self.invoice_tree.insert('', END, values=(
                    invoice_id, customer, formatted_date, formatted_amount, status
                ))
            
            # If no data, show message
            if not rows:
                self.invoice_tree.insert('', END, values=("No data", "No invoices found for the selected period", "", "", ""))
                
        except Exception as e:
            print(f"Error loading invoice data: {e}")
            self.invoice_tree.insert('', END, values=("Error", f"Failed to load data: {e}", "", "", ""))
    
    def get_financial_data(self):
        """Get financial summary data"""
        # Initialize with default values
        data = {
            'total_revenue': 0,
            'total_expenses': 0,
            'net_profit': 0,
            'invoice_count': 0,
            'revenue_growth': 0,
            'expenses_growth': 0,
            'profit_growth': 0,
            'invoice_growth': 0
        }
        
        # Get selected year and month
        selected_year = self.var_year.get()
        selected_month = self.var_month.get()
        
        # Convert month name to number
        month_num = {name: idx for idx, name in enumerate(self.months, 1)}.get(selected_month, None)
        
        try:
            # Query for current period
            query = """
                SELECT SUM(total_amount) as revenue, 
                       COUNT(*) as invoice_count
                FROM billing
                WHERE strftime('%Y', date) = ?
            """
            params = [selected_year]
            
            if month_num:
                query += " AND strftime('%m', date) = ?"
                params.append(f"{month_num:02d}")
            
            self.cursor.execute(query, params)
            row = self.cursor.fetchone()
            
            if row and row[0]:
                data['total_revenue'] = float(row[0])
                data['invoice_count'] = row[1]
                
                # Estimate expenses as 70% of revenue for demonstration
                data['total_expenses'] = data['total_revenue'] * 0.7
                data['net_profit'] = data['total_revenue'] - data['total_expenses']
            
            # Query for previous period (for growth calculation)
            prev_params = []
            if month_num:
                # Previous month in same year
                prev_month = month_num - 1
                prev_year = int(selected_year)
                
                if prev_month == 0:
                    prev_month = 12
                    prev_year -= 1
                
                prev_query = """
                    SELECT SUM(total_amount) as revenue, 
                           COUNT(*) as invoice_count
                    FROM billing
                    WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
                """
                prev_params = [str(prev_year), f"{prev_month:02d}"]
            else:
                # Previous year
                prev_query = """
                    SELECT SUM(total_amount) as revenue, 
                           COUNT(*) as invoice_count
                    FROM billing
                    WHERE strftime('%Y', date) = ?
                """
                prev_params = [str(int(selected_year) - 1)]
            
            self.cursor.execute(prev_query, prev_params)
            prev_row = self.cursor.fetchone()
            
            if prev_row and prev_row[0]:
                prev_revenue = float(prev_row[0])
                prev_invoice_count = prev_row[1]
                
                # Calculate growth percentages
                if prev_revenue > 0:
                    data['revenue_growth'] = ((data['total_revenue'] - prev_revenue) / prev_revenue) * 100
                
                prev_expenses = prev_revenue * 0.7  # Estimated expenses
                if prev_expenses > 0:
                    data['expenses_growth'] = ((data['total_expenses'] - prev_expenses) / prev_expenses) * 100
                
                prev_profit = prev_revenue - prev_expenses
                if prev_profit > 0:
                    data['profit_growth'] = ((data['net_profit'] - prev_profit) / prev_profit) * 100
                
                if prev_invoice_count > 0:
                    data['invoice_growth'] = ((data['invoice_count'] - prev_invoice_count) / prev_invoice_count) * 100
            
        except Exception as e:
            print(f"Error getting financial data: {e}")
        
        return data
    
    def get_monthly_data(self):
        """Get monthly financial data for charts"""
        # Initialize data structure
        data = {
            'month': [],
            'revenue': [],
            'expenses': [],
            'profit': []
        }
        
        selected_year = self.var_year.get()
        
        try:
            query = """
                SELECT strftime('%m', date) as month, 
                       SUM(total_amount) as revenue
                FROM billing
                WHERE strftime('%Y', date) = ?
                GROUP BY month
                ORDER BY month
            """
            
            self.cursor.execute(query, [selected_year])
            rows = self.cursor.fetchall()
            
            for row in rows:
                month_num, revenue = row
                month_name = calendar.month_abbr[int(month_num)]
                
                # Convert to float and estimate expenses and profit
                revenue = float(revenue) if revenue else 0
                expenses = revenue * 0.7  # Estimated expenses as 70% of revenue
                profit = revenue - expenses
                
                data['month'].append(month_name)
                data['revenue'].append(revenue)
                data['expenses'].append(expenses)
                data['profit'].append(profit)
            
            # If no data, provide sample data
            if not rows:
                data['month'] = list(calendar.month_abbr)[1:]
                data['revenue'] = [0] * 12
                data['expenses'] = [0] * 12
                data['profit'] = [0] * 12
                
        except Exception as e:
            print(f"Error getting monthly data: {e}")
            # Provide sample data in case of error
            data['month'] = list(calendar.month_abbr)[1:]
            data['revenue'] = [0] * 12
            data['expenses'] = [0] * 12
            data['profit'] = [0] * 12
        
        return data
    
    def get_category_distribution(self):
        """Get revenue distribution by product category"""
        # Initialize data
        data = {
            'category': [],
            'amount': []
        }
        
        selected_year = self.var_year.get()
        selected_month = self.var_month.get()
        
        # Convert month name to number
        month_num = {name: idx for idx, name in enumerate(self.months, 1)}.get(selected_month, None)
        
        try:
            # Try to get actual category distribution from joined tables
            query = """
                SELECT p.category, SUM(b.total_amount) as total
                FROM billing b
                JOIN product p ON b.product_id = p.id
                WHERE strftime('%Y', b.date) = ?
            """
            params = [selected_year]
            
            if month_num:
                query += " AND strftime('%m', b.date) = ?"
                params.append(f"{month_num:02d}")
            
            query += " GROUP BY p.category ORDER BY total DESC LIMIT 6"
            
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            
            # If we got data, use it
            if rows:
                for row in rows:
                    category, amount = row
                    data['category'].append(category)
                    data['amount'].append(float(amount) if amount else 0)
            else:
                # If join didn't work, get categories and create mock distribution
                self.cursor.execute("SELECT DISTINCT name FROM category LIMIT 6")
                categories = [row[0] for row in self.cursor.fetchall()]
                
                if categories:
                    # Get total revenue for the period
                    revenue_query = """
                        SELECT SUM(total_amount) FROM billing
                        WHERE strftime('%Y', date) = ?
                    """
                    revenue_params = [selected_year]
                    
                    if month_num:
                        revenue_query += " AND strftime('%m', date) = ?"
                        revenue_params.append(f"{month_num:02d}")
                    
                    self.cursor.execute(revenue_query, revenue_params)
                    total_revenue = self.cursor.fetchone()[0]
                    
                    if total_revenue:
                        total_revenue = float(total_revenue)
                        # Create realistic mock distribution
                        weights = [0.3, 0.25, 0.2, 0.15, 0.07, 0.03][:len(categories)]
                        
                        data['category'] = categories
                        data['amount'] = [total_revenue * w for w in weights]
                    else:
                        # No revenue data, create sample data
                        data['category'] = categories
                        data['amount'] = [100, 80, 60, 40, 20, 10][:len(categories)]
                else:
                    # No categories found, create sample data
                    data['category'] = ["Clothes", "Textiles", "Accessories", "Home", "Kids", "Other"]
                    data['amount'] = [100, 80, 60, 40, 20, 10]
        except Exception as e:
            print(f"Error getting category distribution: {e}")
            # Provide sample data in case of error
            data['category'] = ["Clothes", "Textiles", "Accessories", "Home", "Kids", "Other"]
            data['amount'] = [100, 80, 60, 40, 20, 10]
        
        return data
    
    def update_dashboard(self, event=None):
        """Update all dashboard components based on selected filters"""
        # Update financial summary
        self.create_summary_cards()
        
        # Update visualizations
        self.ax_monthly.clear()
        self.ax_pie.clear()
        
        # Get updated data
        monthly_data = self.get_monthly_data()
        category_data = self.get_category_distribution()
        
        # Recreate monthly chart
        months = monthly_data['month']
        revenue = monthly_data['revenue']
        expenses = monthly_data['expenses']
        profit = monthly_data['profit']
        
        x = np.arange(len(months))
        bar_width = 0.25
        
        self.ax_monthly.bar(x - bar_width, revenue, bar_width, label='Revenue', color='#4F46E5')
        self.ax_monthly.bar(x, expenses, bar_width, label='Expenses', color='#F59E0B')
        self.ax_monthly.bar(x + bar_width, profit, bar_width, label='Profit', color='#10B981')
        
        self.ax_monthly.set_xticks(x)
        self.ax_monthly.set_xticklabels(months, rotation=45)
        self.ax_monthly.set_ylabel('Amount (₹)')
        self.ax_monthly.legend()
        self.ax_monthly.grid(axis='y', linestyle='--', alpha=0.7)
        self.fig_monthly.tight_layout()
        
        # Recreate pie chart
        categories = category_data['category']
        amounts = category_data['amount']
        
        colors = ['#4F46E5', '#F59E0B', '#10B981', '#EC4899', '#8B5CF6', '#F43F5E']
        explode = [0.1 if i == amounts.index(max(amounts)) else 0 for i in range(len(amounts))]
        
        self.ax_pie.pie(amounts, explode=explode, labels=categories, colors=colors, 
                        autopct='%1.1f%%', shadow=True, startangle=90)
        self.ax_pie.axis('equal')
        self.fig_pie.tight_layout()
        
        # Redraw the canvases
        self.canvas_monthly.draw()
        self.canvas_pie.draw()
        
        # Update invoice table
        self.load_invoice_data()
    
    def search_invoices(self):
        """Search for invoices based on search term"""
        search_term = self.var_search.get().strip().lower()
        
        if not search_term:
            # If search is empty, reload all data
            self.load_invoice_data()
            return
        
        # Clear existing data
        for item in self.invoice_tree.get_children():
            self.invoice_tree.delete(item)
        
        # Get selected year and month for filtering
        selected_year = self.var_year.get()
        selected_month = self.var_month.get()
        
        # Convert month name to number
        month_num = {name: idx for idx, name in enumerate(self.months, 1)}.get(selected_month, None)
        
        # Build query with search
        try:
            query = """
                SELECT id, customer_name, date, total_amount, 
                CASE WHEN payment_status IS NULL THEN 'Pending' ELSE payment_status END as status
                FROM billing
                WHERE strftime('%Y', date) = ?
                AND (
                    id LIKE ? OR 
                    customer_name LIKE ? OR 
                    date LIKE ? OR
                    total_amount LIKE ? OR
                    payment_status LIKE ?
                )
            """
            params = [
                selected_year,
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%"
            ]
            
            if month_num:
                query += " AND strftime('%m', date) = ?"
                params.append(f"{month_num:02d}")
            
            query += " ORDER BY date DESC"
            
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            
            for row in rows:
                invoice_id, customer, date, amount, status = row
                
                # Format amount with commas for thousands
                formatted_amount = f"₹{float(amount):,.2f}" if amount else "₹0.00"
                
                # Convert date format
                try:
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%d-%b-%Y")
                except:
                    formatted_date = date
                
                self.invoice_tree.insert('', END, values=(
                    invoice_id, customer, formatted_date, formatted_amount, status
                ))
            
            # If no data, show message
            if not rows:
                self.invoice_tree.insert('', END, values=("No matches", f"No invoices match '{search_term}'", "", "", ""))
                
        except Exception as e:
            print(f"Error searching invoice data: {e}")
            self.invoice_tree.insert('', END, values=("Error", f"Failed to search: {e}", "", "", ""))
    
    def filter_by_date(self):
        """Filter invoices by date range"""
        try:
            date_from = self.date_from.get_date()
            date_to = self.date_to.get_date()
            
            if date_from > date_to:
                messagebox.showerror("Error", "From date must be earlier than To date")
                return
            
            # Clear existing data
            for item in self.invoice_tree.get_children():
                self.invoice_tree.delete(item)
            
            # Format dates for SQL query
            date_from_str = date_from.strftime("%Y-%m-%d")
            date_to_str = date_to.strftime("%Y-%m-%d")
            
            query = """
                SELECT id, customer_name, date, total_amount, 
                CASE WHEN payment_status IS NULL THEN 'Pending' ELSE payment_status END as status
                FROM billing
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC
            """
            
            self.cursor.execute(query, [date_from_str, date_to_str])
            rows = self.cursor.fetchall()
            
            for row in rows:
                invoice_id, customer, date, amount, status = row
                
                # Format amount with commas for thousands
                formatted_amount = f"₹{float(amount):,.2f}" if amount else "₹0.00"
                
                # Convert date format
                try:
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    formatted_date = date_obj.strftime("%d-%b-%Y")
                except:
                    formatted_date = date
                
                self.invoice_tree.insert('', END, values=(
                    invoice_id, customer, formatted_date, formatted_amount, status
                ))
            
            # If no data, show message
            if not rows:
                self.invoice_tree.insert('', END, values=(
                    "No matches", f"No invoices between {date_from.strftime('%d-%m-%Y')} and {date_to.strftime('%d-%m-%Y')}", "", "", ""
                ))
                
        except Exception as e:
            print(f"Error filtering by date: {e}")
            messagebox.showerror("Error", f"Failed to filter by date: {e}")
    
    def view_invoice_details(self, event):
        """View details of selected invoice"""
        selected_item = self.invoice_tree.selection()
        if not selected_item:
            return
        
        invoice_values = self.invoice_tree.item(selected_item, 'values')
        invoice_id = invoice_values[0]
        
        # Skip if it's a message row
        if invoice_id in ["No data", "Error", "No matches"]:
            return
        
        try:
            # Get invoice details
            self.cursor.execute("""
                SELECT b.*, c.name as customer_name, c.contact as customer_contact, 
                       c.address as customer_address, c.gst_no
                FROM billing b
                LEFT JOIN kyc c ON b.customer_name = c.name
                WHERE b.id = ?
            """, [invoice_id])
            
            invoice = self.cursor.fetchone()
            
            if not invoice:
                messagebox.showerror("Error", f"Invoice #{invoice_id} not found")
                return
            
            # Create details window
            details_win = Toplevel(self.root)
            details_win.title(f"Invoice #{invoice_id} Details")
            details_win.geometry("800x600")
            details_win.grab_set()
            
            # Invoice details content
            details_frame = Frame(details_win, bg="white", padx=20, pady=20)
            details_frame.pack(fill=BOTH, expand=True)
            
            # Header
            Label(details_frame, text=f"Invoice #{invoice_id}", font=("Helvetica", 18, "bold"), bg="white").pack(pady=10)
            
            # Customer details
            customer_frame = Frame(details_frame, bg="white", bd=1, relief=SOLID, padx=15, pady=15)
            customer_frame.pack(fill=X, pady=10)
            
            Label(customer_frame, text="Customer Information", font=("Helvetica", 14, "bold"), bg="white").pack(anchor=W)
            
            customer_info = Frame(customer_frame, bg="white")
            customer_info.pack(fill=X, pady=10)
            
            # Left column
            left_col = Frame(customer_info, bg="white")
            left_col.pack(side=LEFT, fill=X, expand=True)
            
            Label(left_col, text="Name:", font=("Helvetica", 12, "bold"), bg="white").grid(row=0, column=0, sticky=W, pady=2)
            Label(left_col, text="Contact:", font=("Helvetica", 12, "bold"), bg="white").grid(row=1, column=0, sticky=W, pady=2)
            Label(left_col, text="Address:", font=("Helvetica", 12, "bold"), bg="white").grid(row=2, column=0, sticky=W, pady=2)
            
            Label(left_col, text=invoice[4] or "N/A", font=("Helvetica", 12), bg="white").grid(row=0, column=1, sticky=W, pady=2, padx=10)
            Label(left_col, text=invoice[12] or "N/A", font=("Helvetica", 12), bg="white").grid(row=1, column=1, sticky=W, pady=2, padx=10)
            Label(left_col, text=invoice[13] or "N/A", font=("Helvetica", 12), bg="white").grid(row=2, column=1, sticky=W, pady=2, padx=10)
            
            # Right column
            right_col = Frame(customer_info, bg="white")
            right_col.pack(side=RIGHT, fill=X, expand=True)
            
            Label(right_col, text="Invoice Date:", font=("Helvetica", 12, "bold"), bg="white").grid(row=0, column=0, sticky=W, pady=2)
            Label(right_col, text="GST No:", font=("Helvetica", 12, "bold"), bg="white").grid(row=1, column=0, sticky=W, pady=2)
            Label(right_col, text="Status:", font=("Helvetica", 12, "bold"), bg="white").grid(row=2, column=0, sticky=W, pady=2)
            
            # Format date
            date_str = "N/A"
            if invoice[3]:
                try:
                    date_obj = datetime.strptime(invoice[3], "%Y-%m-%d")
                    date_str = date_obj.strftime("%d-%b-%Y")
                except:
                    date_str = invoice[3]
            
            status = invoice[10] if invoice[10] else "Pending"
            
            Label(right_col, text=date_str, font=("Helvetica", 12), bg="white").grid(row=0, column=1, sticky=W, pady=2, padx=10)
            Label(right_col, text=invoice[14] or "N/A", font=("Helvetica", 12), bg="white").grid(row=1, column=1, sticky=W, pady=2, padx=10)
            status_label = Label(right_col, text=status, font=("Helvetica", 12), bg="white")
            status_label.grid(row=2, column=1, sticky=W, pady=2, padx=10)
            
            # Color code the status
            if status.lower() == "paid":
                status_label.config(fg="#16a34a")
            elif status.lower() == "pending":
                status_label.config(fg="#f59e0b")
            elif status.lower() == "overdue":
                status_label.config(fg="#dc2626")
            
            # Items frame
            items_frame = Frame(details_frame, bg="white", bd=1, relief=SOLID, padx=15, pady=15)
            items_frame.pack(fill=BOTH, expand=True, pady=10)
            
            Label(items_frame, text="Invoice Items", font=("Helvetica", 14, "bold"), bg="white").pack(anchor=W)
            
            # Try to get invoice items
            try:
                # This would need to be adjusted based on your actual database schema
                self.cursor.execute("""
                    SELECT product_name, size, qty, price, amount FROM billing_items WHERE billing_id = ?
                """, [invoice_id])
                
                items = self.cursor.fetchall()
                
                # If we got items, display them
                if items:
                    # Create Treeview for items
                    columns = ('Product', 'Size', 'Quantity', 'Price', 'Amount')
                    items_tree = ttk.Treeview(items_frame, columns=columns, show="headings", height=5)
                    
                    # Configure column widths
                    items_tree.column('Product', width=200, anchor=W)
                    items_tree.column('Size', width=80, anchor=CENTER)
                    items_tree.column('Quantity', width=80, anchor=CENTER)
                    items_tree.column('Price', width=100, anchor=E)
                    items_tree.column('Amount', width=100, anchor=E)
                    
                    # Configure column headings
                    for col in columns:
                        items_tree.heading(col, text=col)
                    
                    # Add items to treeview
                    for item in items:
                        product, size, qty, price, amount = item
                        
                        # Format numbers
                        price_str = f"₹{float(price):,.2f}" if price else "₹0.00"
                        amount_str = f"₹{float(amount):,.2f}" if amount else "₹0.00"
                        
                        items_tree.insert('', END, values=(
                            product, size, qty, price_str, amount_str
                        ))
                    
                    # Add scrollbar
                    scrolly = Scrollbar(items_frame, orient=VERTICAL, command=items_tree.yview)
                    scrolly.pack(side=RIGHT, fill=Y)
                    items_tree.config(yscrollcommand=scrolly.set)
                    
                    items_tree.pack(fill=X, expand=True, pady=10)
                    
                    # Summary section
                    summary_frame = Frame(items_frame, bg="white")
                    summary_frame.pack(fill=X, pady=10)
                    
                    # Right align financial summary
                    summary_right = Frame(summary_frame, bg="white")
                    summary_right.pack(side=RIGHT)
                    
                    # Get total amount from invoice
                    total_amount = float(invoice[6]) if invoice[6] else 0
                    
                    # Calculate GST (assuming 18%)
                    gst_rate = 0.18
                    gst_amount = total_amount * gst_rate
                    subtotal = total_amount - gst_amount
                    
                    Label(summary_right, text="Sub Total:", font=("Helvetica", 12, "bold"), bg="white").grid(row=0, column=0, sticky=E, pady=2)
                    Label(summary_right, text="GST (18%):", font=("Helvetica", 12, "bold"), bg="white").grid(row=1, column=0, sticky=E, pady=2)
                    Label(summary_right, text="Total Amount:", font=("Helvetica", 14, "bold"), bg="white").grid(row=2, column=0, sticky=E, pady=5)
                    
                    Label(summary_right, text=f"₹{subtotal:,.2f}", font=("Helvetica", 12), bg="white").grid(row=0, column=1, sticky=E, pady=2, padx=20)
                    Label(summary_right, text=f"₹{gst_amount:,.2f}", font=("Helvetica", 12), bg="white").grid(row=1, column=1, sticky=E, pady=2, padx=20)
                    Label(summary_right, text=f"₹{total_amount:,.2f}", font=("Helvetica", 14, "bold"), bg="white").grid(row=2, column=1, sticky=E, pady=5, padx=20)
                
                else:
                    # Display full invoice amount if items not available
                    Label(items_frame, text="Detailed items not available", font=("Helvetica", 12), bg="white").pack(pady=10)
                    
                    # Show total amount
                    total_amount = float(invoice[6]) if invoice[6] else 0
                    Label(items_frame, text=f"Total Amount: ₹{total_amount:,.2f}", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
            
            except Exception as e:
                print(f"Error loading invoice items: {e}")
                Label(items_frame, text=f"Error loading items: {str(e)}", font=("Helvetica", 12), fg="red", bg="white").pack(pady=10)
                
                # Show total amount from main invoice
                total_amount = float(invoice[6]) if invoice[6] else 0
                Label(items_frame, text=f"Total Amount: ₹{total_amount:,.2f}", font=("Helvetica", 14, "bold"), bg="white").pack(pady=10)
            
            # Action buttons
            btn_frame = Frame(details_frame, bg="white")
            btn_frame.pack(fill=X, pady=15)
            
            # Print Invoice button
            Button(btn_frame, text="Print Invoice", command=lambda: self.print_invoice(invoice_id), 
                   font=("Helvetica", 12), bg="#2980B9", fg="white", cursor="hand2", padx=15).pack(side=LEFT, padx=5)
            
            # Export button
            Button(btn_frame, text="Export as PDF", command=lambda: self.export_invoice_pdf(invoice_id), 
                   font=("Helvetica", 12), bg="#27AE60", fg="white", cursor="hand2", padx=15).pack(side=LEFT, padx=5)
            
            # Close button
            Button(btn_frame, text="Close", command=details_win.destroy, 
                   font=("Helvetica", 12), bg="#7f8c8d", fg="white", cursor="hand2", padx=15).pack(side=RIGHT, padx=5)
            
        except Exception as e:
            print(f"Error displaying invoice details: {e}")
            messagebox.showerror("Error", f"Failed to load invoice details: {e}")
    
    def print_invoice(self, invoice_id):
        """Print invoice (stub)"""
        messagebox.showinfo("Print Invoice", f"Printing invoice #{invoice_id}...")
        # Implement actual printing functionality based on your system requirements
    
    def export_invoice_pdf(self, invoice_id):
        """Export invoice as PDF (stub)"""
        messagebox.showinfo("Export", f"Exporting invoice #{invoice_id} as PDF...")
        # Implement actual PDF export functionality
    
    def export_data(self):
        """Export financial data to Excel"""
        try:
            # Get selected year and month
            selected_year = self.var_year.get()
            selected_month = self.var_month.get()
            
            # Create a filename
            file_name = f"Financial_Report_{selected_year}"
            if selected_month != "":
                file_name += f"_{selected_month}"
            file_name += ".xlsx"
            
            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                initialfile=file_name
            )
            
            if not file_path:
                return  # User cancelled
            
            # Create a pandas DataFrame from the invoice data
            data = []
            for item in self.invoice_tree.get_children():
                values = self.invoice_tree.item(item, 'values')
                
                # Skip message rows
                if values[0] in ["No data", "Error", "No matches"]:
                    continue
                
                # Convert amount string back to number
                amount_str = values[3]
                try:
                    amount = float(amount_str.replace('₹', '').replace(',', ''))
                except:
                    amount = 0
                
                data.append({
                    'Invoice ID': values[0],
                    'Customer': values[1],
                    'Date': values[2],
                    'Amount': amount,
                    'Status': values[4]
                })
            
            invoices_df = pd.DataFrame(data)
            
            # Create financial summary data
            financial_data = self.get_financial_data()
            summary_data = {
                'Metric': ['Total Revenue', 'Total Expenses', 'Net Profit', 'Total Invoices'],
                'Value': [
                    financial_data['total_revenue'],
                    financial_data['total_expenses'],
                    financial_data['net_profit'],
                    financial_data['invoice_count']
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            
            # Create monthly data
            monthly_data = self.get_monthly_data()
            monthly_df = pd.DataFrame({
                'Month': monthly_data['month'],
                'Revenue': monthly_data['revenue'],
                'Expenses': monthly_data['expenses'],
                'Profit': monthly_data['profit']
            })
            
            # Create category data
            category_data = self.get_category_distribution()
            category_df = pd.DataFrame({
                'Category': category_data['category'],
                'Amount': category_data['amount']
            })
            
            # Create Excel file with multiple sheets
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                # Write each dataframe to a different sheet
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                monthly_df.to_excel(writer, sheet_name='Monthly Analysis', index=False)
                category_df.to_excel(writer, sheet_name='Category Distribution', index=False)
                invoices_df.to_excel(writer, sheet_name='Invoice Details', index=False)
                
                # Access the workbook and the worksheet objects
                workbook = writer.book
                
                # Add formatting
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#2C3E50',
                    'font_color': 'white',
                    'border': 1
                })
                
                currency_format = workbook.add_format({
                    'num_format': '₹#,##0.00',
                    'border': 1
                })
                
                percent_format = workbook.add_format({
                    'num_format': '0.0%',
                    'border': 1
                })
                
                # Apply formatting to all sheets
                for sheet_name in ['Summary', 'Monthly Analysis', 'Category Distribution', 'Invoice Details']:
                    worksheet = writer.sheets[sheet_name]
                    
                    # Format headers
                    for col_num, value in enumerate(writer.sheets[sheet_name].table.columns):
                        worksheet.write(0, col_num, value, header_format)
                    
                    # Set column widths
                    worksheet.set_column(0, 0, 20)  # First column
                    worksheet.set_column(1, 10, 15)  # Other columns
                    
                    # Apply conditional formatting for invoices sheet
                    if sheet_name == 'Invoice Details':
                        worksheet.conditional_format('E2:E1000', {
                            'type': 'cell',
                            'criteria': 'equal to',
                            'value': '"Paid"',
                            'format': workbook.add_format({'bg_color': '#D5F5E3'})  # Light green
                        })
                        worksheet.conditional_format('E2:E1000', {
                            'type': 'cell',
                            'criteria': 'equal to',
                            'value': '"Pending"',
                            'format': workbook.add_format({'bg_color': '#FCF3CF'})  # Light yellow
                        })
                        worksheet.conditional_format('E2:E1000', {
                            'type': 'cell',
                            'criteria': 'equal to',
                            'value': '"Overdue"',
                            'format': workbook.add_format({'bg_color': '#F5B7B1'})  # Light red
                        })
                        
                        # Format amount column
                        worksheet.set_column(3, 3, 15, currency_format)
                
                # Create a chart for monthly data
                monthly_chart = workbook.add_chart({'type': 'column'})
                
                # Add data series
                monthly_chart.add_series({
                    'name': 'Revenue',
                    'categories': '=Monthly Analysis!$A$2:$A$' + str(len(monthly_data['month']) + 1),
                    'values': '=Monthly Analysis!$B$2:$B$' + str(len(monthly_data['month']) + 1),
                    'fill': {'color': '#4F46E5'}
                })
                
                monthly_chart.add_series({
                    'name': 'Expenses',
                    'categories': '=Monthly Analysis!$A$2:$A$' + str(len(monthly_data['month']) + 1),
                    'values': '=Monthly Analysis!$C$2:$C$' + str(len(monthly_data['month']) + 1),
                    'fill': {'color': '#F59E0B'}
                })
                
                monthly_chart.add_series({
                    'name': 'Profit',
                    'categories': '=Monthly Analysis!$A$2:$A$' + str(len(monthly_data['month']) + 1),
                    'values': '=Monthly Analysis!$D$2:$D$' + str(len(monthly_data['month']) + 1),
                    'fill': {'color': '#10B981'}
                })
                
                monthly_chart.set_title({'name': 'Monthly Financial Analysis'})
                monthly_chart.set_x_axis({'name': 'Month'})
                monthly_chart.set_y_axis({'name': 'Amount (₹)'})
                monthly_chart.set_style(10)
                
                # Insert the chart into the Monthly Analysis worksheet
                worksheet = writer.sheets['Monthly Analysis']
                worksheet.insert_chart('F2', monthly_chart, {'x_offset': 25, 'y_offset': 10, 'x_scale': 1.5, 'y_scale': 1.5})
                
                # Create a pie chart for category distribution
                pie_chart = workbook.add_chart({'type': 'pie'})
                
                # Add data series
                pie_chart.add_series({
                    'name': 'Category Distribution',
                    'categories': '=Category Distribution!$A$2:$A$' + str(len(category_data['category']) + 1),
                    'values': '=Category Distribution!$B$2:$B$' + str(len(category_data['category']) + 1),
                    'data_labels': {'percentage': True}
                })
                
                pie_chart.set_title({'name': 'Revenue by Category'})
                pie_chart.set_style(10)
                
                # Insert the chart into the Category Distribution worksheet
                worksheet = writer.sheets['Category Distribution']
                worksheet.insert_chart('D2', pie_chart, {'x_offset': 25, 'y_offset': 10, 'x_scale': 1.2, 'y_scale': 1.2})
            
            messagebox.showinfo("Export Successful", f"Financial report exported to {file_path}")
        
        except Exception as e:
            print(f"Error exporting data: {e}")
            messagebox.showerror("Export Error", f"Failed to export data: {e}")
            
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()


if __name__ == "__main__":
    root = Tk()
    obj = AccountsDashboard(root)
    root.mainloop()