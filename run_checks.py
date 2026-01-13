import sqlite3
from app import app
import time

DB = 'upi_guard.db'

with app.test_client() as client:
    # Admin login
    admin_mobile = '9999999999'
    r = client.post('/login', data={'mobile': admin_mobile, 'user_type': 'admin'}, follow_redirects=True)
    time.sleep(0.2)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM otp_storage WHERE mobile = ? ORDER BY created_at DESC LIMIT 1", (admin_mobile,))
    otp = cur.fetchone()['otp']
    conn.close()
    r = client.post('/verify_otp', data={'otp': otp}, follow_redirects=True)
    print('Admin dashboard status:', client.get('/admin/dashboard').status_code)

    # Merchant QR generation (merchant must login first)
    merchant_mobile = '9000000002'
    client.post('/login', data={'mobile': merchant_mobile, 'user_type': 'merchant'}, follow_redirects=True)
    time.sleep(0.1)
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM otp_storage WHERE mobile = ? ORDER BY created_at DESC LIMIT 1', (merchant_mobile,))
    otp = cur.fetchone()['otp']
    conn.close()
    client.post('/verify_otp', data={'otp': otp}, follow_redirects=True)

    r = client.post('/api/generate_qr', json={}, follow_redirects=True)
    print('Generate QR status:', r.status_code, 'json:', r.get_json())
