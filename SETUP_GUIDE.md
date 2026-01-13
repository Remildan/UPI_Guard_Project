<<<<<<< HEAD
# UPI Guard - Complete Setup Guide

## Step-by-Step Installation for Windows (VS Code)

### Prerequisites
- Windows 10/11
- VS Code installed
- Internet connection

---

## Step 1: Install Python

1. **Download Python**
   - Go to https://www.python.org/downloads/
   - Download Python 3.8 or higher (recommended: Python 3.10)

2. **Install Python**
   - Run the installer
   - ✅ **IMPORTANT**: Check "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**
   - Open PowerShell or Command Prompt
   - Type: `python --version`
   - Should display: `Python 3.x.x`
   - If error: Python not in PATH - reinstall with "Add to PATH" checked

---

## Step 2: Open Project in VS Code

1. **Open VS Code**
   - Launch Visual Studio Code

2. **Open Project Folder**
   - Click: `File → Open Folder`
   - Navigate to: `D:\Projects\Real-Time UPI Fraud Detection`
   - Click "Select Folder"

3. **Install Python Extension (if prompted)**
   - VS Code may suggest installing Python extension
   - Click "Install" if prompted

---

## Step 3: Create Virtual Environment

1. **Open Terminal in VS Code**
   - Press: `Ctrl + ` (backtick) OR
   - Click: `Terminal → New Terminal`

2. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   ```
   Wait for completion (may take 30-60 seconds)

3. **Activate Virtual Environment**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **If you get an execution policy error:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then run activation command again.

4. **Verify Activation**
   - Terminal prompt should show: `(venv)` at the beginning
   - Example: `(venv) PS D:\Projects\...`

---

## Step 4: Install Python Dependencies

1. **Install from requirements.txt**
   ```powershell
   pip install -r requirements.txt
   ```
   
   **Expected installation time**: 5-10 minutes
   - This installs Flask, TensorFlow, Pandas, NumPy, Scikit-learn, etc.
   - Wait for "Successfully installed..." message

2. **Verify Installation**
   ```powershell
   pip list
   ```
   Should show all packages from requirements.txt

---

## Step 5: Generate Training Dataset

1. **Run Dataset Generator**
   ```powershell
   python data/generate_dataset.py
   ```
   
   **Expected output:**
   ```
   Dataset generated successfully!
   Total transactions: 50000
   Legitimate: 45000 (90.0%)
   Fraudulent: 5000 (10.0%)
   Saved to: data/upi_transactions.csv
   ```

2. **Verify Dataset**
   - Check: `data/upi_transactions.csv` file exists
   - File size should be around 3-5 MB

---

## Step 6: Train Machine Learning Models

1. **Train All Models**
   ```powershell
   python models/train_models.py
   ```
   
   **Expected time**: 5-15 minutes (depends on CPU)
   
   **What happens:**
   - Preprocesses data
   - Trains Logistic Regression (~1 min)
   - Trains Random Forest (~2 min)
   - Trains SVM (~3 min)
   - Trains CNN (~5-10 min)
   - Compares accuracies
   - Saves best model (CNN)

2. **Expected Output:**
   ```
   Training CNN model...
   Epoch 1/50
   ...
   Model Comparison:
   Logistic Regression:   85.23%
   Random Forest:         92.45%
   SVM:                   90.12%
   CNN (Final Model):     99.12%
   ```

3. **Verify Models Created**
   - Check `models/` folder contains:
     - `fraud_detection_cnn.h5` (CNN model)
     - `fraud_detection_lr.pkl` (Logistic Regression)
     - `fraud_detection_rf.pkl` (Random Forest)
     - `fraud_detection_svm.pkl` (SVM)
     - `scaler.pkl` (Feature scaler)

---

## Step 7: Initialize Database

1. **Create Database**
   ```powershell
   python database.py
   ```
   
   **Expected output:**
   ```
   Creating database tables...
   ✓ Users table created
   ✓ Merchants table created
   ✓ Transactions table created
   ✓ Fraud logs table created
   ✓ OTP storage table created
   ✓ Admins table created
   ✓ Default admin created
   ```

2. **Verify Database**
   - Check: `upi_guard.db` file exists in project root
   - File size: ~10-20 KB (empty database)

---

## Step 8: Run Flask Application

1. **Start Flask Server**
   ```powershell
   python app.py
   ```
   
   **Expected output:**
   ```
   Initializing UPI Guard...
   ✓ CNN model loaded from models/fraud_detection_cnn.h5
   ✓ Scaler loaded from models/scaler.pkl
   ============================================================
   UPI Guard - Real-Time Fraud Detection System
   ============================================================
   Server starting on http://127.0.0.1:5000
   ```

2. **Open Browser**
   - Open: http://127.0.0.1:5000
   - Should see login page

3. **Keep Terminal Open**
   - Server runs in terminal
   - Press `Ctrl+C` to stop server

---

## Step 9: Test the Application

### Test as Admin:
1. Mobile: `9999999999`
2. User Type: Admin
3. OTP: Check terminal/console (development mode)
4. Should see admin dashboard

### Test as User:
1. Mobile: Any 10-digit number (e.g., `9876543210`)
2. User Type: User
3. OTP: Check terminal/console
4. Should see user dashboard
5. Try making a payment

### Test as Merchant:
1. Mobile: Any 10-digit number (e.g., `9876543211`)
2. User Type: Merchant
3. OTP: Check terminal/console
4. Should see merchant dashboard
5. Generate QR code

---

## Troubleshooting

### Issue: "python is not recognized"
**Solution**: 
- Reinstall Python with "Add to PATH" checked
- Or add Python to PATH manually in System Environment Variables

### Issue: "pip is not recognized"
**Solution**:
```powershell
python -m pip install -r requirements.txt
```

### Issue: "Execution Policy Error"
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Module not found" errors
**Solution**:
1. Ensure virtual environment is activated `(venv)` in prompt
2. Reinstall: `pip install -r requirements.txt`

### Issue: TensorFlow installation fails
**Solution**:
- Make sure Python version is 3.8-3.11
- Try: `pip install tensorflow==2.15.0 --upgrade`

### Issue: Model training is too slow
**Solution**:
- Normal for CPU training
- Wait for completion (10-15 minutes)
- For faster training, use GPU (advanced)

### Issue: Database errors
**Solution**:
- Delete `upi_guard.db` file
- Run `python database.py` again

### Issue: Port 5000 already in use
**Solution**:
- Change PORT in `config.py`
- Or stop other applications using port 5000

---

## Quick Start (After Initial Setup)

Once everything is set up, to run the project:

```powershell
# 1. Open terminal in VS Code

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Run Flask app
python app.py

# 4. Open browser: http://127.0.0.1:5000
```

---

## Project Structure Checklist

After setup, verify you have:

```
Real-Time UPI Fraud Detection/
├── app.py                          ✓
├── database.py                     ✓
├── config.py                       ✓
├── requirements.txt                ✓
├── upi_guard.db                    ✓ (created after database.py)
├── models/
│   ├── train_models.py            ✓
│   ├── fraud_detection_cnn.h5     ✓ (created after training)
│   ├── fraud_detection_lr.pkl     ✓ (created after training)
│   ├── fraud_detection_rf.pkl     ✓ (created after training)
│   ├── fraud_detection_svm.pkl    ✓ (created after training)
│   └── scaler.pkl                 ✓ (created after training)
├── data/
│   ├── upi_transactions.csv       ✓ (created after generate_dataset.py)
│   ├── generate_dataset.py        ✓
│   └── dataset_info.txt           ✓
├── static/
│   ├── css/
│   │   └── style.css              ✓
│   └── js/
│       └── script.js              ✓
├── templates/
│   ├── base.html                  ✓
│   ├── login.html                 ✓
│   ├── verify_otp.html            ✓
│   ├── user_dashboard.html        ✓
│   ├── merchant_dashboard.html    ✓
│   └── admin_dashboard.html       ✓
├── venv/                           ✓ (virtual environment)
├── README.md                       ✓
└── SETUP_GUIDE.md                 ✓
```

---

## Success Checklist

✅ Python 3.8+ installed  
✅ Virtual environment created and activated  
✅ All dependencies installed  
✅ Dataset generated (50,000 transactions)  
✅ Models trained (CNN accuracy > 99%)  
✅ Database initialized  
✅ Flask server running  
✅ Can access login page in browser  
✅ Can login as admin/user/merchant  
✅ Can make transactions with fraud detection  

**If all checked, you're ready to use UPI Guard! 🎉**

---

## Need Help?

- Check error messages in terminal
- Review this guide step-by-step
- Verify file paths and names
- Ensure all files are in correct folders
=======
# UPI Guard - Complete Setup Guide

## Step-by-Step Installation for Windows (VS Code)

### Prerequisites
- Windows 10/11
- VS Code installed
- Internet connection

---

## Step 1: Install Python

1. **Download Python**
   - Go to https://www.python.org/downloads/
   - Download Python 3.8 or higher (recommended: Python 3.10)

2. **Install Python**
   - Run the installer
   - ✅ **IMPORTANT**: Check "Add Python to PATH"
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**
   - Open PowerShell or Command Prompt
   - Type: `python --version`
   - Should display: `Python 3.x.x`
   - If error: Python not in PATH - reinstall with "Add to PATH" checked

---

## Step 2: Open Project in VS Code

1. **Open VS Code**
   - Launch Visual Studio Code

2. **Open Project Folder**
   - Click: `File → Open Folder`
   - Navigate to: `D:\Projects\Real-Time UPI Fraud Detection`
   - Click "Select Folder"

3. **Install Python Extension (if prompted)**
   - VS Code may suggest installing Python extension
   - Click "Install" if prompted

---

## Step 3: Create Virtual Environment

1. **Open Terminal in VS Code**
   - Press: `Ctrl + ` (backtick) OR
   - Click: `Terminal → New Terminal`

2. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   ```
   Wait for completion (may take 30-60 seconds)

3. **Activate Virtual Environment**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **If you get an execution policy error:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then run activation command again.

4. **Verify Activation**
   - Terminal prompt should show: `(venv)` at the beginning
   - Example: `(venv) PS D:\Projects\...`

---

## Step 4: Install Python Dependencies

1. **Install from requirements.txt**
   ```powershell
   pip install -r requirements.txt
   ```
   
   **Expected installation time**: 5-10 minutes
   - This installs Flask, TensorFlow, Pandas, NumPy, Scikit-learn, etc.
   - Wait for "Successfully installed..." message

2. **Verify Installation**
   ```powershell
   pip list
   ```
   Should show all packages from requirements.txt

---

## Step 5: Generate Training Dataset

1. **Run Dataset Generator**
   ```powershell
   python data/generate_dataset.py
   ```
   
   **Expected output:**
   ```
   Dataset generated successfully!
   Total transactions: 50000
   Legitimate: 45000 (90.0%)
   Fraudulent: 5000 (10.0%)
   Saved to: data/upi_transactions.csv
   ```

2. **Verify Dataset**
   - Check: `data/upi_transactions.csv` file exists
   - File size should be around 3-5 MB

---

## Step 6: Train Machine Learning Models

1. **Train All Models**
   ```powershell
   python models/train_models.py
   ```
   
   **Expected time**: 5-15 minutes (depends on CPU)
   
   **What happens:**
   - Preprocesses data
   - Trains Logistic Regression (~1 min)
   - Trains Random Forest (~2 min)
   - Trains SVM (~3 min)
   - Trains CNN (~5-10 min)
   - Compares accuracies
   - Saves best model (CNN)

2. **Expected Output:**
   ```
   Training CNN model...
   Epoch 1/50
   ...
   Model Comparison:
   Logistic Regression:   85.23%
   Random Forest:         92.45%
   SVM:                   90.12%
   CNN (Final Model):     99.12%
   ```

3. **Verify Models Created**
   - Check `models/` folder contains:
     - `fraud_detection_cnn.h5` (CNN model)
     - `fraud_detection_lr.pkl` (Logistic Regression)
     - `fraud_detection_rf.pkl` (Random Forest)
     - `fraud_detection_svm.pkl` (SVM)
     - `scaler.pkl` (Feature scaler)

---

## Step 7: Initialize Database

1. **Create Database**
   ```powershell
   python database.py
   ```
   
   **Expected output:**
   ```
   Creating database tables...
   ✓ Users table created
   ✓ Merchants table created
   ✓ Transactions table created
   ✓ Fraud logs table created
   ✓ OTP storage table created
   ✓ Admins table created
   ✓ Default admin created
   ```

2. **Verify Database**
   - Check: `upi_guard.db` file exists in project root
   - File size: ~10-20 KB (empty database)

---

## Step 8: Run Flask Application

1. **Start Flask Server**
   ```powershell
   python app.py
   ```
   
   **Expected output:**
   ```
   Initializing UPI Guard...
   ✓ CNN model loaded from models/fraud_detection_cnn.h5
   ✓ Scaler loaded from models/scaler.pkl
   ============================================================
   UPI Guard - Real-Time Fraud Detection System
   ============================================================
   Server starting on http://127.0.0.1:5000
   ```

2. **Open Browser**
   - Open: http://127.0.0.1:5000
   - Should see login page

3. **Keep Terminal Open**
   - Server runs in terminal
   - Press `Ctrl+C` to stop server

---

## Step 9: Test the Application

### Test as Admin:
1. Mobile: `9999999999`
2. User Type: Admin
3. OTP: Check terminal/console (development mode)
4. Should see admin dashboard

### Test as User:
1. Mobile: Any 10-digit number (e.g., `9876543210`)
2. User Type: User
3. OTP: Check terminal/console
4. Should see user dashboard
5. Try making a payment

### Test as Merchant:
1. Mobile: Any 10-digit number (e.g., `9876543211`)
2. User Type: Merchant
3. OTP: Check terminal/console
4. Should see merchant dashboard
5. Generate QR code

---

## Troubleshooting

### Issue: "python is not recognized"
**Solution**: 
- Reinstall Python with "Add to PATH" checked
- Or add Python to PATH manually in System Environment Variables

### Issue: "pip is not recognized"
**Solution**:
```powershell
python -m pip install -r requirements.txt
```

### Issue: "Execution Policy Error"
**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Module not found" errors
**Solution**:
1. Ensure virtual environment is activated `(venv)` in prompt
2. Reinstall: `pip install -r requirements.txt`

### Issue: TensorFlow installation fails
**Solution**:
- Make sure Python version is 3.8-3.11
- Try: `pip install tensorflow==2.15.0 --upgrade`

### Issue: Model training is too slow
**Solution**:
- Normal for CPU training
- Wait for completion (10-15 minutes)
- For faster training, use GPU (advanced)

### Issue: Database errors
**Solution**:
- Delete `upi_guard.db` file
- Run `python database.py` again

### Issue: Port 5000 already in use
**Solution**:
- Change PORT in `config.py`
- Or stop other applications using port 5000

---

## Quick Start (After Initial Setup)

Once everything is set up, to run the project:

```powershell
# 1. Open terminal in VS Code

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Run Flask app
python app.py

# 4. Open browser: http://127.0.0.1:5000
```

---

## Project Structure Checklist

After setup, verify you have:

```
Real-Time UPI Fraud Detection/
├── app.py                          ✓
├── database.py                     ✓
├── config.py                       ✓
├── requirements.txt                ✓
├── upi_guard.db                    ✓ (created after database.py)
├── models/
│   ├── train_models.py            ✓
│   ├── fraud_detection_cnn.h5     ✓ (created after training)
│   ├── fraud_detection_lr.pkl     ✓ (created after training)
│   ├── fraud_detection_rf.pkl     ✓ (created after training)
│   ├── fraud_detection_svm.pkl    ✓ (created after training)
│   └── scaler.pkl                 ✓ (created after training)
├── data/
│   ├── upi_transactions.csv       ✓ (created after generate_dataset.py)
│   ├── generate_dataset.py        ✓
│   └── dataset_info.txt           ✓
├── static/
│   ├── css/
│   │   └── style.css              ✓
│   └── js/
│       └── script.js              ✓
├── templates/
│   ├── base.html                  ✓
│   ├── login.html                 ✓
│   ├── verify_otp.html            ✓
│   ├── user_dashboard.html        ✓
│   ├── merchant_dashboard.html    ✓
│   └── admin_dashboard.html       ✓
├── venv/                           ✓ (virtual environment)
├── README.md                       ✓
└── SETUP_GUIDE.md                 ✓
```

---

## Success Checklist

✅ Python 3.8+ installed  
✅ Virtual environment created and activated  
✅ All dependencies installed  
✅ Dataset generated (50,000 transactions)  
✅ Models trained (CNN accuracy > 99%)  
✅ Database initialized  
✅ Flask server running  
✅ Can access login page in browser  
✅ Can login as admin/user/merchant  
✅ Can make transactions with fraud detection  

**If all checked, you're ready to use UPI Guard! 🎉**

---

## Need Help?

- Check error messages in terminal
- Review this guide step-by-step
- Verify file paths and names
- Ensure all files are in correct folders
>>>>>>> a692c63 (initial commit)
