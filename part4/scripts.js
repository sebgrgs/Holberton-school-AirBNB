document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;
          
          try {
              const response = await fetch('http://localhost:5000/api/v1/auth/login', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({ email, password })
              });
              
              if (response.ok) {
                  const data = await response.json();
                  
                  const expirationDate = new Date();
                  expirationDate.setDate(expirationDate.getDate() + 1);
                  document.cookie = `token=${data.access_token}; expires=${expirationDate.toUTCString()}; path=/`;
                  
                  window.location.href = 'index.html';
              } else {
                  const errorData = await response.json();
                  displayLoginError(errorData.error || 'Login failed. Please check your credentials.');
              }
          } catch (error) {
              console.error('Login error:', error);
              displayLoginError('Network error occurred. Please try again later.');
          }
      });
  }
});

function displayLoginError(message) {

  let errorElement = document.getElementById('login-error');

  if (!errorElement) {
      errorElement = document.createElement('div');
      errorElement.id = 'login-error';
      errorElement.className = 'error-message';
      
      const loginForm = document.getElementById('login-form');
      loginForm.parentNode.insertBefore(errorElement, loginForm);
  }
  
  errorElement.textContent = message;
  errorElement.style.display = 'block';
}