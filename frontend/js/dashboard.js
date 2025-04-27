// js/dashboard.js

window.onload = function() {
    checkAuth();

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

    const sidebarDiv = document.getElementById('sidebar-buttons');

    if (user.role === 'admin') {
        sidebarDiv.innerHTML = `
            <button onclick="window.location.href='patients.html'">Manage Patients</button>
            <button onclick="window.location.href='doctors.html'">Manage Doctors</button>
            <button onclick="window.location.href='appointments.html'">Manage Appointments</button>
        `;
    } else if (user.role === 'doctor') {
        sidebarDiv.innerHTML = `
            <button onclick="window.location.href='appointments.html'">View Appointments</button>
        `;
    } else if (user.role === 'patient') {
        sidebarDiv.innerHTML = `
            <button onclick="window.location.href='appointments.html'">Book/View Appointments</button>
        `;
    } else {
        sidebarDiv.innerHTML = `<p>No actions available for your role.</p>`;
    }
}
