<<<<<<< HEAD
// UPI Guard - Frontend JavaScript

// Close flash messages
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
    
    // Close button for flash messages
    document.querySelectorAll('.close-flash').forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => this.parentElement.remove(), 300);
        });
    });
    
    // Mobile number validation
    const mobileInput = document.getElementById('mobile');
    if (mobileInput) {
        mobileInput.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, ''); // Only numbers
        });
    }
    
    // OTP input auto-focus and formatting
    const otpInput = document.getElementById('otp');
    if (otpInput) {
        otpInput.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, ''); // Only numbers
        });
    }
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation helpers
function validateMobile(mobile) {
    return /^[0-9]{10}$/.test(mobile);
}

function validateOTP(otp) {
    return /^[0-9]{6}$/.test(otp);
}

function validateAmount(amount) {
    return amount > 0 && amount <= 100000;
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

// Utility function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
=======
// UPI Guard - Frontend JavaScript

// Close flash messages
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
    
    // Close button for flash messages
    document.querySelectorAll('.close-flash').forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => this.parentElement.remove(), 300);
        });
    });
    
    // Mobile number validation
    const mobileInput = document.getElementById('mobile');
    if (mobileInput) {
        mobileInput.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, ''); // Only numbers
        });
    }
    
    // OTP input auto-focus and formatting
    const otpInput = document.getElementById('otp');
    if (otpInput) {
        otpInput.addEventListener('input', function() {
            this.value = this.value.replace(/\D/g, ''); // Only numbers
        });
    }
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Form validation helpers
function validateMobile(mobile) {
    return /^[0-9]{10}$/.test(mobile);
}

function validateOTP(otp) {
    return /^[0-9]{6}$/.test(otp);
}

function validateAmount(amount) {
    return amount > 0 && amount <= 100000;
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

// Utility function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
>>>>>>> a692c63 (initial commit)
