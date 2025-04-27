
 // Change if you deploy

 async function login() {
    console.log("login() called ✅");

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        alert('Please fill in all fields.');
        return;
    }

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const response = await fetch(`${BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        const responseBody = await response.json(); // ✅ always parse

        if (response.ok) {
            console.log("Login successful:", responseBody);

            localStorage.setItem('access_token', responseBody.access_token);
            localStorage.setItem('user_role', responseBody.role);
            localStorage.setItem('username', responseBody.username);

            if (responseBody.role === 'admin') {
                window.location.href = 'admin_dashboard.html';
            } else if (responseBody.role === 'doctor') {
                window.location.href = 'doctor_dashboard.html';
            } else if (responseBody.role === 'patient') {
                window.location.href = 'patient_dashboard.html';
            } else {
                alert('Unknown role.');
            }
        } else {
            console.error("Login failed:", responseBody);
            alert('Login failed: ' + (responseBody.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Network error. Please try again later.');
    }
}


// Add Event Listener after page load
window.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', login);
    }
});
// Function to decode JWT token 
function decodeJWT(token) {
    if (!token) return null;

    const payload = token.split('.')[1];
    const decodedPayload = JSON.parse(atob(payload));

    return decodedPayload;
}
// Function to check if user is logged in
function checkAuth() {
    const token = localStorage.getItem('access_token');
    const user = decodeJWT(token);

    if (!user) {
        alert("Session expired. Please login again.");
        window.location.href = "index.html";
        return;
    }

    document.getElementById('user-info').innerHTML = `
        <h3>Hello, ${user.sub}</h3>
        <p>Role: ${user.role}</p>
    `;
}

localStorage.setItem('access_token', data.access_token);
localStorage.setItem('user_role', data.role);    // ✅ save role separately
localStorage.setItem('username', data.username); // ✅ save username separately
