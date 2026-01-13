import sqlite3
from app import app
import time

DB = 'upi_guard.db'


def get_latest_otp(mobile):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM otp_storage WHERE mobile = ? ORDER BY created_at DESC LIMIT 1", (mobile,))
    row = cur.fetchone()
    conn.close()
    return row['otp'] if row else None


with app.test_client() as client:
    # Merchant
    merchant_mobile = '9000000002'
    print('POST /login merchant')
    r = client.post('/login', data={'mobile': merchant_mobile, 'user_type': 'merchant'}, follow_redirects=True)
    time.sleep(0.2)
    otp = get_latest_otp(merchant_mobile)
    print('Found OTP:', otp)
    r = client.post('/verify_otp', data={'otp': otp}, follow_redirects=True)
    print('Merchant verify status code:', r.status_code)

    # Check merchant exists in DB
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM merchants WHERE mobile = ?', (merchant_mobile,))
    merchant = cur.fetchone()
    conn.close()
    print('Merchant created:', bool(merchant))
    merchant_upi = merchant['upi_id']
    print('Merchant UPI:', merchant_upi)

    # User
    user_mobile = '9000000001'
    print('POST /login user')
    r = client.post('/login', data={'mobile': user_mobile, 'user_type': 'user'}, follow_redirects=True)
    time.sleep(0.2)
    otp = get_latest_otp(user_mobile)
    print('User OTP:', otp)
    r = client.post('/verify_otp', data={'otp': otp}, follow_redirects=True)
    print('User verify status code:', r.status_code)

    # Process payment
    print('POST /api/process_payment')
    payload = {'merchant_upi': merchant_upi, 'amount': '25.50', 'category': 1}
    r = client.post('/api/process_payment', json=payload)
    print('Process payment status:', r.status_code)
    print('Response json:', r.get_json())

    print('Local E2E test finished')
