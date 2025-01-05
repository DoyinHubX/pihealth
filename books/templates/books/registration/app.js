const apiBaseUrl = 'http://localhost:8000/'; // Update this based on your backend URL

// Function to handle registration
async function sendRegisterRequest(username, email, password) {
    const response = await fetch(`${apiBaseUrl}/register/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password,
        }),
    });

    const data = await response.json();
    return data;
}

// Function to handle login and return JWT tokens
async function sendLoginRequest(username, password) {
    const response = await fetch(`${apiBaseUrl}/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    });

    const data = await response.json();
    if (data.access && data.refresh) {
        localStorage.setItem('access_token', data.access); // Save access token in localStorage
        localStorage.setItem('refresh_token', data.refresh); // Save refresh token in localStorage
    }
    return data;
}

// Function to check if the user is logged in
function checkAuth() {
    const accessToken = localStorage.getItem('access_token');
    return accessToken ? true : false;
}

// Function to fetch user profile (only accessible if authenticated)
async function getUserProfile() {
    const accessToken = localStorage.getItem('access_token');
    const response = await fetch(`${apiBaseUrl}/profile/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
        },
    });

    const data = await response.json();
    return data;
}

// Function to logout (clear stored JWT tokens)
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/';
}

// Handling form submission for registration
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    const data = await sendRegisterRequest(username, email, password);
    alert(data.detail || 'Registration failed');
});

// Handling form submission for login
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('login-username').value; // Change here: username instead of email
    const password = document.getElementById('login-password').value;

    const data = await sendLoginRequest(username, password); // Pass username and password
    if (data.access && data.refresh) {
        alert('Login successful');
        window.location.href = '/auth/dashboard.html'; // Redirect to the dashboard
    } else {
        alert(data.detail || 'Login failed');
    }
});

async function validateAccessToken() {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) return false;

    const response = await fetch(`${apiBaseUrl}/profile/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
        },
    });

    return response.ok; // Return true if token is valid
}

if (checkAuth()) {
    validateAccessToken().then(isValid => {
        if (!isValid) {
            alert('Session expired. Please log in again.');
            logout();
        }
    });
}

// Dashboard display logic (if logged in)
if (checkAuth()) {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('register-section').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';

    getUserProfile().then(profile => {
        document.getElementById('dashboard-user-info').innerHTML = `
            <p>Welcome, ${profile.username}</p>
            <p>Email: ${profile.email}</p>
        `;
    }).catch(() => {
        alert('Failed to fetch profile.');
    });

    document.getElementById('logout-button').addEventListener('click', () => {
        logout();
        window.location.href = '/';
    });
} else {
    document.getElementById('login-section').style.display = 'block';
    document.getElementById('register-section').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
}

