import requests
import sqlite3
import time

BASE = 'http://127.0.0.1:5000'
DB = 'upi_guard.db'

def get_latest_otp(mobile):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM otp_storage WHERE mobile = ? ORDER BY created_at DESC LIMIT 1", (mobile,))
    row = cur.fetchone()
    conn.close()
    return row['otp'] if row else None


def login_and_verify(session, mobile, user_type='user'):
    # login
    r = session.post(f'{BASE}/login', data={'mobile': mobile, 'user_type': user_type}, allow_redirects=True)
    # wait for DB write
    time.sleep(0.5)
    otp = get_latest_otp(mobile)
    if not otp:
        raise RuntimeError('OTP not found in DB')
    # verify
    r = session.post(f'{BASE}/verify_otp', data={'otp': otp}, allow_redirects=True)
    return r


if __name__ == '__main__':
    # Merchant flow
    merchant_mobile = '9000000002'
    user_mobile = '9000000001'

    s_merchant = requests.Session()
    print('Logging in merchant...')
    login_and_verify(s_merchant, merchant_mobile, user_type='merchant')

    # Read merchant upi from DB
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM merchants WHERE mobile = ?', (merchant_mobile,))
    merchant = cur.fetchone()
    conn.close()
    if not merchant:
        raise RuntimeError('Merchant not created')

    merchant_upi = merchant['upi_id']
    print('Merchant UPI:', merchant_upi)

    # User flow
    s_user = requests.Session()
    print('Logging in user...')
    login_and_verify(s_user, user_mobile, user_type='user')

    # Process payment
    print('Processing payment from user to merchant...')
    payload = {'merchant_upi': merchant_upi, 'amount': '50.00', 'category': 1}
    r = s_user.post(f'{BASE}/api/process_payment', json=payload)
    print('Status code:', r.status_code)
    try:
        print('Response JSON:', r.json())
    except Exception:
        print('Response text:', r.text)

    print('E2E test finished')
