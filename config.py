"""
Configuration file for UPI Guard Application
"""
import os

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-2024')
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('1', 'true', 'yes')
# Use environment PORT if provided (Render sets PORT)
PORT = int(os.environ.get('PORT', '10000'))

# Database Configuration
DATABASE_PATH = 'upi_guard.db'

# OTP Configuration (Development Mode - Email Based)
OTP_EXPIRY_MINUTES = 10
OTP_LENGTH = 6

# Email Configuration (for OTP - Development)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_EMAIL = 'your-email@gmail.com'  # Change this
SMTP_PASSWORD = 'your-app-password'   # Change this (use App Password, not regular password)

# For Development: Simple OTP (no actual email sending)
# In production, configure proper SMTP settings above
DEV_MODE = True  # Set to False in production

# Fraud Detection Configuration
FRAUD_THRESHOLD = 0.5  # Probability threshold (0-1) for blocking transaction
MODEL_PATH = 'models/fraud_detection_cnn.h5'
SCALER_PATH = 'models/scaler.pkl'

# Transaction Categories
CATEGORIES = {
    1: 'Grocery',
    2: 'Food & Dining',
    3: 'Shopping',
    4: 'Travel',
    5: 'Bills & Utilities',
    6: 'Entertainment',
    7: 'Healthcare',
    8: 'Education',
    9: 'Transfer',
    10: 'Other'
}
