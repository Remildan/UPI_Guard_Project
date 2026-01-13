<<<<<<< HEAD
"""
Dataset Generator for UPI Transaction Fraud Detection
Generates synthetic but realistic UPI transaction data
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime

def generate_dataset(num_transactions=50000, fraud_ratio=0.1):
    """
    Generate synthetic UPI transaction dataset
    
    Args:
        num_transactions: Total number of transactions to generate
        fraud_ratio: Ratio of fraudulent transactions (default 10%)
    """
    
    np.random.seed(42)  # For reproducibility
    random.seed(42)
    
    # Calculate number of fraud cases
    num_fraud = int(num_transactions * fraud_ratio)
    num_legitimate = num_transactions - num_fraud
    
    data = []
    
    # Generate Legitimate Transactions
    print("Generating legitimate transactions...")
    for i in range(num_legitimate):
        # Legitimate transaction patterns
        amount = np.random.lognormal(mean=5.5, sigma=1.2)  # Right-skewed (most transactions are small)
        amount = min(max(round(amount, 2), 1.0), 100000)  # Clamp between ₹1 and ₹1,00,000
        
        time_hour = np.random.choice(range(24), p=[
            0.02, 0.01, 0.01, 0.01, 0.01, 0.02,  # 12 AM - 5 AM (low activity)
            0.03, 0.05, 0.08, 0.10, 0.12, 0.15,  # 6 AM - 11 AM (increasing)
            0.18, 0.20, 0.18, 0.15, 0.12, 0.10,  # 12 PM - 5 PM (peak hours)
            0.08, 0.12, 0.15, 0.18, 0.15, 0.08   # 6 PM - 11 PM (evening peak)
        ])
        
        time_minute = random.randint(0, 59)
        user_age = random.randint(18, 80)
        merchant_age = random.randint(30, 3650)  # Established merchants
        state_code = random.randint(1, 36)
        zip_code = random.randint(100, 999)
        category = random.choices(range(1, 11), weights=[15, 20, 15, 10, 10, 8, 5, 5, 7, 5])[0]
        upi_id_hash = random.randint(1000, 99999)
        
        data.append({
            'transaction_id': i + 1,
            'amount': amount,
            'time_hour': time_hour,
            'time_minute': time_minute,
            'user_age': user_age,
            'merchant_age': merchant_age,
            'state_code': state_code,
            'zip_code': zip_code,
            'category': category,
            'upi_id_hash': upi_id_hash,
            'fraud': 0
        })
    
    # Generate Fraudulent Transactions
    print("Generating fraudulent transactions...")
    for i in range(num_fraud):
        # Fraud patterns: unusual amounts, times, locations
        amount = np.random.choice([
            np.random.lognormal(mean=7, sigma=1.5),  # High amount
            np.random.lognormal(mean=3, sigma=0.5),  # Very low amount (test transaction)
            random.choice([999, 1999, 4999, 9999])  # Round numbers (suspicious)
        ])
        amount = min(max(round(amount, 2), 1.0), 100000)
        
        # Fraud more common at odd hours
        time_hour = np.random.choice(range(24), p=[
            0.10, 0.08, 0.06, 0.05, 0.04, 0.03,  # Midnight hours (higher fraud)
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02,  # Morning (lower)
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02,  # Afternoon
            0.03, 0.04, 0.05, 0.06, 0.08, 0.10   # Evening/night (higher fraud)
        ])
        
        time_minute = random.randint(0, 59)
        user_age = random.choice([
            random.randint(18, 25),  # Younger users (higher risk)
            random.randint(65, 80),  # Elderly users (targeted)
            random.randint(18, 80)   # Random
        ])
        
        merchant_age = random.choice([
            random.randint(1, 30),   # New merchant (high risk)
            random.randint(30, 365)  # Recently created
        ])
        
        state_code = random.randint(1, 36)
        zip_code = random.randint(100, 999)
        
        # Fraud more common in certain categories
        category = random.choices(range(1, 11), weights=[5, 5, 20, 15, 10, 15, 5, 5, 15, 5])[0]
        
        upi_id_hash = random.randint(1000, 99999)
        
        data.append({
            'transaction_id': num_legitimate + i + 1,
            'amount': amount,
            'time_hour': time_hour,
            'time_minute': time_minute,
            'user_age': user_age,
            'merchant_age': merchant_age,
            'state_code': state_code,
            'zip_code': zip_code,
            'category': category,
            'upi_id_hash': upi_id_hash,
            'fraud': 1
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df['transaction_id'] = range(1, len(df) + 1)
    
    # Save to CSV
    output_path = 'data/upi_transactions.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nDataset generated successfully!")
    print(f"Total transactions: {len(df)}")
    print(f"Legitimate: {len(df[df['fraud'] == 0])} ({len(df[df['fraud'] == 0])/len(df)*100:.1f}%)")
    print(f"Fraudulent: {len(df[df['fraud'] == 1])} ({len(df[df['fraud'] == 1])/len(df)*100:.1f}%)")
    print(f"Saved to: {output_path}")
    
    # Display sample
    print("\nSample of generated data:")
    print(df.head(10))
    
    return df

if __name__ == '__main__':
    print("=" * 50)
    print("UPI Transaction Dataset Generator")
    print("=" * 50)
    generate_dataset(num_transactions=50000, fraud_ratio=0.1)
=======
"""
Dataset Generator for UPI Transaction Fraud Detection
Generates synthetic but realistic UPI transaction data
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime

def generate_dataset(num_transactions=50000, fraud_ratio=0.1):
    """
    Generate synthetic UPI transaction dataset
    
    Args:
        num_transactions: Total number of transactions to generate
        fraud_ratio: Ratio of fraudulent transactions (default 10%)
    """
    
    np.random.seed(42)  # For reproducibility
    random.seed(42)
    
    # Calculate number of fraud cases
    num_fraud = int(num_transactions * fraud_ratio)
    num_legitimate = num_transactions - num_fraud
    
    data = []
    
    # Generate Legitimate Transactions
    print("Generating legitimate transactions...")
    for i in range(num_legitimate):
        # Legitimate transaction patterns
        amount = np.random.lognormal(mean=5.5, sigma=1.2)  # Right-skewed (most transactions are small)
        amount = min(max(round(amount, 2), 1.0), 100000)  # Clamp between ₹1 and ₹1,00,000
        
        time_hour = np.random.choice(range(24), p=[
            0.02, 0.01, 0.01, 0.01, 0.01, 0.02,  # 12 AM - 5 AM (low activity)
            0.03, 0.05, 0.08, 0.10, 0.12, 0.15,  # 6 AM - 11 AM (increasing)
            0.18, 0.20, 0.18, 0.15, 0.12, 0.10,  # 12 PM - 5 PM (peak hours)
            0.08, 0.12, 0.15, 0.18, 0.15, 0.08   # 6 PM - 11 PM (evening peak)
        ])
        
        time_minute = random.randint(0, 59)
        user_age = random.randint(18, 80)
        merchant_age = random.randint(30, 3650)  # Established merchants
        state_code = random.randint(1, 36)
        zip_code = random.randint(100, 999)
        category = random.choices(range(1, 11), weights=[15, 20, 15, 10, 10, 8, 5, 5, 7, 5])[0]
        upi_id_hash = random.randint(1000, 99999)
        
        data.append({
            'transaction_id': i + 1,
            'amount': amount,
            'time_hour': time_hour,
            'time_minute': time_minute,
            'user_age': user_age,
            'merchant_age': merchant_age,
            'state_code': state_code,
            'zip_code': zip_code,
            'category': category,
            'upi_id_hash': upi_id_hash,
            'fraud': 0
        })
    
    # Generate Fraudulent Transactions
    print("Generating fraudulent transactions...")
    for i in range(num_fraud):
        # Fraud patterns: unusual amounts, times, locations
        amount = np.random.choice([
            np.random.lognormal(mean=7, sigma=1.5),  # High amount
            np.random.lognormal(mean=3, sigma=0.5),  # Very low amount (test transaction)
            random.choice([999, 1999, 4999, 9999])  # Round numbers (suspicious)
        ])
        amount = min(max(round(amount, 2), 1.0), 100000)
        
        # Fraud more common at odd hours
        time_hour = np.random.choice(range(24), p=[
            0.10, 0.08, 0.06, 0.05, 0.04, 0.03,  # Midnight hours (higher fraud)
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02,  # Morning (lower)
            0.02, 0.02, 0.02, 0.02, 0.02, 0.02,  # Afternoon
            0.03, 0.04, 0.05, 0.06, 0.08, 0.10   # Evening/night (higher fraud)
        ])
        
        time_minute = random.randint(0, 59)
        user_age = random.choice([
            random.randint(18, 25),  # Younger users (higher risk)
            random.randint(65, 80),  # Elderly users (targeted)
            random.randint(18, 80)   # Random
        ])
        
        merchant_age = random.choice([
            random.randint(1, 30),   # New merchant (high risk)
            random.randint(30, 365)  # Recently created
        ])
        
        state_code = random.randint(1, 36)
        zip_code = random.randint(100, 999)
        
        # Fraud more common in certain categories
        category = random.choices(range(1, 11), weights=[5, 5, 20, 15, 10, 15, 5, 5, 15, 5])[0]
        
        upi_id_hash = random.randint(1000, 99999)
        
        data.append({
            'transaction_id': num_legitimate + i + 1,
            'amount': amount,
            'time_hour': time_hour,
            'time_minute': time_minute,
            'user_age': user_age,
            'merchant_age': merchant_age,
            'state_code': state_code,
            'zip_code': zip_code,
            'category': category,
            'upi_id_hash': upi_id_hash,
            'fraud': 1
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df['transaction_id'] = range(1, len(df) + 1)
    
    # Save to CSV
    output_path = 'data/upi_transactions.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nDataset generated successfully!")
    print(f"Total transactions: {len(df)}")
    print(f"Legitimate: {len(df[df['fraud'] == 0])} ({len(df[df['fraud'] == 0])/len(df)*100:.1f}%)")
    print(f"Fraudulent: {len(df[df['fraud'] == 1])} ({len(df[df['fraud'] == 1])/len(df)*100:.1f}%)")
    print(f"Saved to: {output_path}")
    
    # Display sample
    print("\nSample of generated data:")
    print(df.head(10))
    
    return df

if __name__ == '__main__':
    print("=" * 50)
    print("UPI Transaction Dataset Generator")
    print("=" * 50)
    generate_dataset(num_transactions=50000, fraud_ratio=0.1)
>>>>>>> a692c63 (initial commit)
