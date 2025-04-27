let editingDoctorId = null; // Track if editing

async function loadDoctors() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert("Session expired. Please login again.");
        window.location.href = "index.html";
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/doctors/`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.ok) {
            const doctors = await response.json();
            const tableBody = document.querySelector("#doctors-table tbody");
            tableBody.innerHTML = "";

            doctors.forEach(doctor => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${doctor.name}</td>
                    <td>${doctor.specialization}</td>
                    <td>${doctor.phone}</td>
                    <td>
                      <button onclick='editDoctor(${JSON.stringify(doctor)})'>Edit</button>
                      <button onclick="deleteDoctor(${doctor.id})">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.error("Failed to load doctors. Status:", response.status);
            alert("Failed to fetch doctors list. Please check server.");
        }
    } catch (error) {
        console.error("Error while loading doctors:", error);
    }
}

async function addOrUpdateDoctor() {
    const token = localStorage.getItem('access_token');

    const doctorData = {
        name: document.getElementById('name').value,
        specialization: document.getElementById('specialization').value,
        phone: document.getElementById('phone').value
    };

    if (editingDoctorId) {
        const response = await fetch(`${BASE_URL}/doctors/${editingDoctorId}`, {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(doctorData)
        });

        if (response.ok) {
            alert("Doctor updated successfully!");
            loadDoctors();
            resetForm();
        } else {
            alert("Failed to update doctor.");
        }

    } else {
        const response = await fetch(`${BASE_URL}/doctors/`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(doctorData)
        });

        if (response.ok) {
            alert("Doctor added successfully!");
            loadDoctors();
            resetForm();
        } else {
            alert("Failed to add doctor.");
        }
    }
}

function editDoctor(doctor) {
    document.getElementById('name').value = doctor.name;
    document.getElementById('specialization').value = doctor.specialization;
    document.getElementById('phone').value = doctor.phone;

    editingDoctorId = doctor.id;
    document.getElementById('add-doctor-btn').innerText = "Update Doctor";
    document.getElementById('form-title').innerText = "Update Doctor";
}

async function deleteDoctor(doctorId) {
    const token = localStorage.getItem('access_token');

    const confirmDelete = confirm("Are you sure you want to delete this doctor?");
    if (!confirmDelete) return;

    const response = await fetch(`${BASE_URL}/doctors/${doctorId}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    if (response.ok) {
        alert("Doctor deleted successfully!");
        loadDoctors();
    } else {
        alert("Failed to delete doctor.");
    }
}

function resetForm() {
    document.getElementById('name').value = "";
    document.getElementById('specialization').value = "";
    document.getElementById('phone').value = "";
    editingDoctorId = null;
    document.getElementById('add-doctor-btn').innerText = "Add Doctor";
    document.getElementById('form-title').innerText = "Add New Doctor";
}

// Attach button
document.addEventListener('DOMContentLoaded', function() {
    const addDoctorBtn = document.getElementById('add-doctor-btn');
    if (addDoctorBtn) {
        addDoctorBtn.addEventListener('click', addOrUpdateDoctor);
    }
});
