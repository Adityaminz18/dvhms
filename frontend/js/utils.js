// js/utils.js
const BASE_URL = window.location.origin;


function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('access_token');
    options.headers = {
        ...(options.headers || {}),
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
    return fetch(BASE_URL + url, options);
}

// js/utils.js

function decodeJWT(token) {
    if (!token) return null;
    const payload = token.split('.')[1];
    const decodedPayload = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
    return JSON.parse(decodedPayload);
}

