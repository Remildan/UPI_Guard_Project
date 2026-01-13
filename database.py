"""
Database Initialization Script
Creates SQLite database with all required tables for UPI Guard
"""

import sqlite3
import os
from datetime import datetime
import hashlib

# Database file path
DB_PATH = 'upi_guard.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def create_tables():
    """Create all required database tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Creating database tables...")
    
    # Users Table (Payers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile TEXT UNIQUE NOT NULL,
            email TEXT,
            name TEXT NOT NULL,
            age INTEGER,
            state_code INTEGER,
            zip_code INTEGER,
            upi_id TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    print("✓ Users table created")
    
    # Merchants Table (Sellers)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS merchants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile TEXT UNIQUE NOT NULL,
            email TEXT,
            business_name TEXT NOT NULL,
            merchant_age INTEGER DEFAULT 0,
            state_code INTEGER,
            zip_code INTEGER,
            upi_id TEXT UNIQUE,
            qr_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    print("✓ Merchants table created")
    
    # Transactions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            merchant_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category INTEGER,
            upi_id TEXT,
            state_code INTEGER,
            zip_code INTEGER,
            time_hour INTEGER,
            time_minute INTEGER,
            fraud_probability REAL,
            is_fraud BOOLEAN DEFAULT 0,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (merchant_id) REFERENCES merchants(id)
        )
    ''')
    print("✓ Transactions table created")
    
    # Fraud Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fraud_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT NOT NULL,
            user_id INTEGER,
            merchant_id INTEGER,
            amount REAL,
            fraud_probability REAL,
            reason TEXT,
            action_taken TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
        )
    ''')
    print("✓ Fraud logs table created")
    
    # OTP Table (for authentication)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otp_storage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile TEXT NOT NULL,
            otp TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            verified BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ OTP storage table created")
    
    # Admin Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Admins table created")
    
    conn.commit()
    conn.close()
    print("\nAll tables created successfully!")

def create_default_admin():
    """Create default admin user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT * FROM admins WHERE mobile = ?", ('9999999999',))
    admin = cursor.fetchone()
    
    if not admin:
        cursor.execute('''
            INSERT INTO admins (mobile, name, email)
            VALUES (?, ?, ?)
        ''', ('9999999999', 'Admin User', 'admin@upiguard.com'))
        conn.commit()
        print("\n✓ Default admin created")
        print("   Mobile: 9999999999")
    else:
        print("\n✓ Admin already exists")
    
    conn.close()

def generate_transaction_id():
    """Generate unique transaction ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"TXN{timestamp}"

if __name__ == '__main__':
    print("=" * 60)
    print("UPI Guard - Database Initialization")
    print("=" * 60)
    
    # Remove existing database if it exists (for fresh start)
    if os.path.exists(DB_PATH):
        response = input(f"\nDatabase '{DB_PATH}' already exists. Recreate? (y/n): ")
        if response.lower() == 'y':
            os.remove(DB_PATH)
            print("Old database removed.")
        else:
            print("Keeping existing database.")
    
    # Create tables
    create_tables()
    
    # Create default admin
    create_default_admin()
    
    print("\n" + "=" * 60)
    print("Database initialization complete!")
    print("=" * 60)
    print(f"\nDatabase file: {DB_PATH}")
    print("\nYou can now run the Flask application: python app.py")
