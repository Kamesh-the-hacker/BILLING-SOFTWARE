import importlib
import os
import sys
import sqlite3
from datetime import datetime

def integrate_accounts():
    """
    Integrate accounts module with main IMS system
    """
    # Check if we have required dependencies
    missing_deps = check_dependencies()
    if missing_deps:
        print("Missing required dependencies for Accounts module:")
        print(", ".join(missing_deps))
        print("\nPlease install these packages using pip:")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    
    # Create/update database tables
    setup_database()
    
    # Try to patch the IMS class
    try:
        # Import and patch IMS class
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from IMS import IMS
        from accounts_manager import add_accounts_to_ims
        
        # Apply the patch
        patched_IMS = add_accounts_to_ims(IMS)
        
        # Replace the original IMS class with the patched one
        sys.modules['IMS'].IMS = patched_IMS
        
        print("Successfully integrated Accounts module with IMS")
        return True
    
    except ImportError:
        print("Could not import the IMS class. Make sure the main system is properly installed.")
        return False
    
    except Exception as e:
        print(f"Error integrating Accounts module: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'pandas',
        'matplotlib', 
        'seaborn',
        'numpy',
        'tkcalendar',
        'xlsxwriter',
        'pillow'
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing.append(package)
    
    return missing

def setup_database():
    """Setup or update database tables required for accounting"""
    try:
        # Connect to database
        conn = sqlite3.connect('python//ims.db')
        cursor = conn.cursor()

        # Create financial_transactions table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_date TEXT,
                transaction_type TEXT,
                amount REAL,
                description TEXT,
                reference_id TEXT,
                category TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create accounting_categories table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounting_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                type TEXT,
                description TEXT
            )
        """)

        # Create billing_summary table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS billing_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                billing_id TEXT UNIQUE,
                customer_name TEXT,
                bill_date TEXT,
                total_amount REAL,
                payment_status TEXT,
                FOREIGN KEY (billing_id) REFERENCES billing(id)
            )
        """)

        # Create billing_items table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS billing_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                billing_id TEXT,
                product_name TEXT,
                size TEXT,
                qty INTEGER,
                price REAL,
                amount REAL,
                FOREIGN KEY (billing_id) REFERENCES billing(id)
            )
        """)
            
        # Insert default categories if accounting_categories is empty
        cursor.execute("SELECT COUNT(*) FROM accounting_categories")
        if cursor.fetchone()[0] == 0:
            default_categories = [
                ('Sales', 'Income', 'Revenue from product sales'),
                ('Purchases', 'Expense', 'Cost of goods purchased'),
                ('Rent', 'Expense', 'Office and warehouse rent'),
                ('Salaries', 'Expense', 'Employee salaries'),
                ('Utilities', 'Expense', 'Electricity, water, and other utilities'),
                ('Shipping', 'Expense', 'Shipping and delivery costs'),
                ('Tax', 'Expense', 'Sales tax and other taxes'),
                ('Other Income', 'Income', 'Miscellaneous income sources'),
                ('Other Expenses', 'Expense', 'Miscellaneous expenses')
            ]
            
            cursor.executemany("""
                INSERT INTO accounting_categories (name, type, description) 
                VALUES (?, ?, ?)
            """, default_categories)

        # Migrate existing billing data
        cursor.execute("""
            INSERT OR IGNORE INTO billing_summary (billing_id, customer_name, bill_date, total_amount, payment_status)
            SELECT id, customer_name, date, total_amount, payment_status 
            FROM billing
        """)

        # Migrate billing items
        cursor.execute("SELECT id, cart_data FROM billing WHERE cart_data IS NOT NULL")
        for billing_id, cart_data in cursor.fetchall():
            try:
                items = eval(cart_data)
                for item in items:
                    if isinstance(item, (list, tuple)) and len(item) >= 5:
                        product_name, size, qty, price, amount = item[:5]
                        cursor.execute("""
                            INSERT OR IGNORE INTO billing_items 
                            (billing_id, product_name, size, qty, price, amount)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (billing_id, product_name, size, qty, price, amount))
            except:
                continue

        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_billing_date ON billing_summary(bill_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_billing_customer ON billing_summary(customer_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON financial_transactions(transaction_date)")
        
        conn.commit()
        conn.close()
        print("Database setup complete")
        return True
    
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

if __name__ == "__main__":
    integrate_accounts()