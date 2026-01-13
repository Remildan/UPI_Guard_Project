"""
UPI Guard - Main Flask Application
Real-Time UPI Fraud Detection System
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sqlite3
import os
import random
import string
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from tensorflow import keras
import joblib
from functools import wraps
import hashlib

from config import *

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Global variables for models (loaded once at startup)
fraud_model = None
scaler = None

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_models():
    """Load trained ML models"""
    global fraud_model, scaler
    
    try:
        # Load CNN model
        if os.path.exists(MODEL_PATH):
            fraud_model = keras.models.load_model(MODEL_PATH)
            print(f"✓ CNN model loaded from {MODEL_PATH}")
        else:
            print(f"⚠ Warning: Model not found at {MODEL_PATH}")
            print("  Please train models first: python models/train_models.py")
        
        # Load scaler
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
            print(f"✓ Scaler loaded from {SCALER_PATH}")
        else:
            print(f"⚠ Warning: Scaler not found at {SCALER_PATH}")
    except Exception as e:
        print(f"Error loading models: {e}")

# Load models at startup
print("\nInitializing UPI Guard...")
load_models()

def generate_otp(length=6):
    """Generate random OTP"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(mobile, otp):
    """Send OTP via email (development mode - simple implementation)"""
    # In production, implement proper SMTP email sending
    if DEV_MODE:
        print(f"\n[DEV MODE] OTP for {mobile}: {otp}")
        print("In production, this would be sent via email")
        return True
    else:
        # Implement actual SMTP email sending here
        # For now, return True for development
        return True

def generate_transaction_id():
    """Generate unique transaction ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"TXN{timestamp}"

def detect_fraud(transaction_data):
    """
    Real-time fraud detection using trained CNN model
    
    Args:
        transaction_data: Dictionary with transaction features
        - amount, time_hour, time_minute, user_age, merchant_age,
          state_code, zip_code, category, upi_id_hash
    
    Returns:
        tuple: (is_fraud: bool, fraud_probability: float)
    """
    global fraud_model, scaler
    
    if fraud_model is None or scaler is None:
        # If models not loaded, return safe default
        return False, 0.1
    
    try:
        # Prepare feature vector in correct order
        features = np.array([[
            transaction_data['amount'],
            transaction_data['time_hour'],
            transaction_data['time_minute'],
            transaction_data['user_age'],
            transaction_data['merchant_age'],
            transaction_data['state_code'],
            transaction_data['zip_code'],
            transaction_data['category'],
            transaction_data['upi_id_hash']
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Reshape for CNN (1D convolution)
        features_cnn = features_scaled.reshape(features_scaled.shape[0], features_scaled.shape[1], 1)
        
        # Predict fraud probability
        fraud_probability = float(fraud_model.predict(features_cnn, verbose=0)[0][0])
        
        # Determine if fraud (threshold-based)
        is_fraud = fraud_probability > FRAUD_THRESHOLD
        
        return is_fraud, fraud_probability
        
    except Exception as e:
        print(f"Error in fraud detection: {e}")
        # On error, allow transaction (fail-safe)
        return False, 0.1

def login_required(f):
    """Decorator for routes requiring authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and 'merchant_id' not in session and 'admin_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== Routes ====================

@app.route('/')
def index():
    """Home page - redirect to login"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        mobile = request.form.get('mobile', '').strip()
        user_type = request.form.get('user_type', 'user')
        
        if not mobile or len(mobile) != 10:
            flash('Please enter a valid 10-digit mobile number', 'error')
            return render_template('login.html')
        
        # Generate and store OTP
        otp = generate_otp()
        expires_at = datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Store OTP
        cursor.execute('''
            INSERT INTO otp_storage (mobile, otp, expires_at)
            VALUES (?, ?, ?)
        ''', (mobile, otp, expires_at))
        
        conn.commit()
        conn.close()
        
        # Send OTP (development mode)
        send_otp_email(mobile, otp)
        
        session['mobile'] = mobile
        session['user_type'] = user_type
        session['otp_sent'] = True
        
        flash(f'OTP sent to your mobile number! (DEV: OTP is {otp})', 'info')
        return redirect(url_for('verify_otp'))
    
    return render_template('login.html')

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    """OTP verification page"""
    if 'mobile' not in session or 'otp_sent' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        
        if not otp or len(otp) != 6:
            flash('Please enter a valid 6-digit OTP', 'error')
            return render_template('verify_otp.html')
        
        mobile = session.get('mobile')
        user_type = session.get('user_type', 'user')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verify OTP
        cursor.execute('''
            SELECT * FROM otp_storage
            WHERE mobile = ? AND otp = ? AND verified = 0
            AND expires_at > datetime('now')
            ORDER BY created_at DESC
            LIMIT 1
        ''', (mobile, otp))
        
        otp_record = cursor.fetchone()
        
        if otp_record:
            # Mark OTP as verified
            cursor.execute('''
                UPDATE otp_storage SET verified = 1
                WHERE id = ?
            ''', (otp_record['id'],))
            
            # Handle different user types
            if user_type == 'admin':
                cursor.execute('SELECT * FROM admins WHERE mobile = ?', (mobile,))
                admin = cursor.fetchone()
                if admin:
                    session['admin_id'] = admin['id']
                    session['admin_name'] = admin['name']
                    conn.commit()
                    conn.close()
                    return redirect(url_for('admin_dashboard'))
                else:
                    conn.close()
                    flash('Admin not found', 'error')
                    return redirect(url_for('login'))
            
            elif user_type == 'merchant':
                cursor.execute('SELECT * FROM merchants WHERE mobile = ?', (mobile,))
                merchant = cursor.fetchone()
                
                if not merchant:
                    # Create new merchant
                    business_name = f"Merchant_{mobile[-4:]}"
                    merchant_age = random.randint(1, 3650)
                    upi_id = f"{mobile}@upiguard"
                    
                    cursor.execute('''
                        INSERT INTO merchants (mobile, business_name, merchant_age, upi_id)
                        VALUES (?, ?, ?, ?)
                    ''', (mobile, business_name, merchant_age, upi_id))
                    conn.commit()
                    cursor.execute('SELECT * FROM merchants WHERE mobile = ?', (mobile,))
                    merchant = cursor.fetchone()
                
                session['merchant_id'] = merchant['id']
                session['merchant_name'] = merchant['business_name']
                conn.close()
                return redirect(url_for('merchant_dashboard'))
            
            else:  # user
                cursor.execute('SELECT * FROM users WHERE mobile = ?', (mobile,))
                user = cursor.fetchone()
                
                if not user:
                    # Create new user
                    name = f"User_{mobile[-4:]}"
                    age = random.randint(18, 80)
                    state_code = random.randint(1, 36)
                    zip_code = random.randint(100, 999)
                    upi_id = f"{mobile}@upiguard"
                    
                    cursor.execute('''
                        INSERT INTO users (mobile, name, age, state_code, zip_code, upi_id)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (mobile, name, age, state_code, zip_code, upi_id))
                    conn.commit()
                    cursor.execute('SELECT * FROM users WHERE mobile = ?', (mobile,))
                    user = cursor.fetchone()
                
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                conn.close()
                return redirect(url_for('user_dashboard'))
        else:
            conn.close()
            flash('Invalid or expired OTP', 'error')
    
    return render_template('verify_otp.html')

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    """User (Payer) Dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user info
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    # Get transaction history
    cursor.execute('''
        SELECT t.*, m.business_name as merchant_name
        FROM transactions t
        JOIN merchants m ON t.merchant_id = m.id
        WHERE t.user_id = ?
        ORDER BY t.created_at DESC
        LIMIT 20
    ''', (user_id,))
    transactions = cursor.fetchall()
    
    conn.close()
    
    return render_template('user_dashboard.html', user=user, transactions=transactions)

@app.route('/merchant/dashboard')
@login_required
def merchant_dashboard():
    """Merchant (Seller) Dashboard"""
    if 'merchant_id' not in session:
        return redirect(url_for('login'))
    
    merchant_id = session['merchant_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get merchant info
    cursor.execute('SELECT * FROM merchants WHERE id = ?', (merchant_id,))
    merchant = cursor.fetchone()
    
    # Get received payments
    cursor.execute('''
        SELECT t.*, u.name as user_name
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        WHERE t.merchant_id = ? AND t.status = 'completed'
        ORDER BY t.created_at DESC
        LIMIT 20
    ''', (merchant_id,))
    transactions = cursor.fetchall()
    
    conn.close()
    
    return render_template('merchant_dashboard.html', merchant=merchant, transactions=transactions)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin Dashboard"""
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Statistics
    cursor.execute('SELECT COUNT(*) as count FROM users')
    total_users = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM merchants')
    total_merchants = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM transactions')
    total_transactions = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM transactions WHERE is_fraud = 1')
    fraud_count = cursor.fetchone()['count']
    
    # Recent transactions
    cursor.execute('''
        SELECT t.*, u.name as user_name, m.business_name as merchant_name
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        JOIN merchants m ON t.merchant_id = m.id
        ORDER BY t.created_at DESC
        LIMIT 50
    ''')
    transactions = cursor.fetchall()
    
    # Fraud logs
    cursor.execute('''
        SELECT f.*, u.name as user_name, m.business_name as merchant_name
        FROM fraud_logs f
        LEFT JOIN users u ON f.user_id = u.id
        LEFT JOIN merchants m ON f.merchant_id = m.id
        ORDER BY f.created_at DESC
        LIMIT 50
    ''')
    fraud_logs = cursor.fetchall()
    
    # All users
    cursor.execute('SELECT * FROM users ORDER BY created_at DESC LIMIT 100')
    users = cursor.fetchall()
    
    # All merchants
    cursor.execute('SELECT * FROM merchants ORDER BY created_at DESC LIMIT 100')
    merchants = cursor.fetchall()
    
    conn.close()
    
    stats = {
        'total_users': total_users,
        'total_merchants': total_merchants,
        'total_transactions': total_transactions,
        'fraud_count': fraud_count
    }
    
    return render_template('admin_dashboard.html', 
                         stats=stats, 
                         transactions=transactions,
                         fraud_logs=fraud_logs,
                         users=users,
                         merchants=merchants)

@app.route('/api/process_payment', methods=['POST'])
@login_required
def process_payment():
    """Process payment with real-time fraud detection"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        merchant_upi = data.get('merchant_upi', '').strip()
        amount = float(data.get('amount', 0))
        category = int(data.get('category', 1))
        
        if amount <= 0:
            return jsonify({'success': False, 'message': 'Invalid amount'}), 400
        
        user_id = session['user_id']
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get user info
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        # Get merchant info
        cursor.execute('SELECT * FROM merchants WHERE upi_id = ?', (merchant_upi,))
        merchant = cursor.fetchone()
        
        if not merchant:
            conn.close()
            return jsonify({'success': False, 'message': 'Merchant not found'}), 404
        
        # Get current time
        now = datetime.now()
        time_hour = now.hour
        time_minute = now.minute
        
        # Generate transaction ID
        transaction_id = generate_transaction_id()
        
        # Prepare transaction data for fraud detection
        transaction_data = {
            'amount': amount,
            'time_hour': time_hour,
            'time_minute': time_minute,
            'user_age': user['age'],
            'merchant_age': merchant['merchant_age'],
            'state_code': user['state_code'],
            'zip_code': user['zip_code'],
            'category': category,
            'upi_id_hash': hash(merchant_upi) % 100000  # Simple hash
        }
        
        # REAL-TIME FRAUD DETECTION (BEFORE TRANSACTION)
        is_fraud, fraud_probability = detect_fraud(transaction_data)
        
        # Create transaction record
        status = 'blocked' if is_fraud else 'pending'
        
        cursor.execute('''
            INSERT INTO transactions (
                transaction_id, user_id, merchant_id, amount, category,
                upi_id, state_code, zip_code, time_hour, time_minute,
                fraud_probability, is_fraud, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction_id, user_id, merchant['id'], amount, category,
            merchant_upi, user['state_code'], user['zip_code'],
            time_hour, time_minute, fraud_probability, 1 if is_fraud else 0, status
        ))
        
        # If fraud detected, log it
        if is_fraud:
            cursor.execute('''
                INSERT INTO fraud_logs (
                    transaction_id, user_id, merchant_id, amount,
                    fraud_probability, reason, action_taken
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                transaction_id, user_id, merchant['id'], amount,
                fraud_probability,
                f'Fraud probability: {fraud_probability:.2%}',
                'Transaction blocked'
            ))
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': False,
                'fraud_detected': True,
                'message': f'Transaction blocked due to fraud risk ({fraud_probability:.2%})',
                'transaction_id': transaction_id
            }), 403
        
        # If safe, complete transaction
        cursor.execute('''
            UPDATE transactions SET status = 'completed'
            WHERE transaction_id = ?
        ''', (transaction_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'fraud_detected': False,
            'message': 'Payment successful',
            'transaction_id': transaction_id,
            'fraud_probability': fraud_probability
        })
        
    except Exception as e:
        print(f"Error processing payment: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/generate_qr', methods=['POST'])
@login_required
def generate_qr():
    """Generate QR code for merchant"""
    if 'merchant_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    merchant_id = session['merchant_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT upi_id FROM merchants WHERE id = ?', (merchant_id,))
    merchant = cursor.fetchone()
    
    if not merchant:
        conn.close()
        return jsonify({'success': False, 'message': 'Merchant not found'}), 404
    
    qr_data = merchant['upi_id']
    
    # Update QR code in database
    cursor.execute('''
        UPDATE merchants SET qr_code = ?
        WHERE id = ?
    ''', (qr_data, merchant_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'qr_code': qr_data,
        'upi_id': qr_data
    })

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("UPI Guard - Real-Time Fraud Detection System")
    print("=" * 60)
    print(f"\nServer starting on http://127.0.0.1:{PORT}")
    print("\nAvailable routes:")
    print("  - /login (User/Merchant/Admin login)")
    print("  - /user/dashboard (User dashboard)")
    print("  - /merchant/dashboard (Merchant dashboard)")
    print("  - /admin/dashboard (Admin dashboard)")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    app.run(debug=DEBUG, port=PORT, host='0.0.0.0')
