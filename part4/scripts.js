document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message') || createErrorElement();

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                await loginUser(email, password);
            } catch (error) {
                showError(errorMessage, error.message || 'An error occurred during login');
            }
        });
    }
});

async function loginUser(email, password) {
    hideError();
    
    const submitButton = document.querySelector('button[type="submit"]');
    if (submitButton) {
        const originalText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Logging in...';
        
        setTimeout(() => {
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }, 3000);
    }
    
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    
    if (response.ok) {
        const data = await response.json();
        
        const expiryDate = new Date();
        expiryDate.setTime(expiryDate.getTime() + (24 * 60 * 60 * 1000));
        document.cookie = `token=${data.access_token}; path=/; expires=${expiryDate.toUTCString()}; SameSite=Strict`;
        
        window.location.href = 'index.html';
    } else {
        const errorData = await response.json().catch(() => ({ message: response.statusText }));
        throw new Error(errorData.message || 'Login failed. Please check your credentials.');
    }
}

function createErrorElement() {
    const errorElement = document.createElement('div');
    errorElement.id = 'error-message';
    errorElement.className = 'error-message';
    errorElement.style.color = 'red';
    errorElement.style.marginTop = '10px';
    errorElement.style.display = 'none';
    
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.parentNode.insertBefore(errorElement, loginForm);
    }
    
    return errorElement;
}

function showError(element, message) {
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    } else {
        alert(message);
    }
}

function hideError() {
    const errorMessage = document.getElementById('error-message');
    if (errorMessage) {
        errorMessage.style.display = 'none';
    }
}