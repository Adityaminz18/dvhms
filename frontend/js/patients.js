let editingPatientId = null; // Track if editing

async function loadPatients() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert("Session expired. Please login again.");
        window.location.href = "index.html";
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/api/patients/`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.ok) {
            const patients = await response.json();
            const tableBody = document.querySelector("#patients-table tbody");
            tableBody.innerHTML = "";

            patients.forEach(patient => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${patient.name}</td>
                    <td>${patient.age}</td>
                    <td>${patient.gender}</td>
                    <td>${patient.address}</td>
                    <td>${patient.phone}</td>
                    <td>
                      <button onclick='editPatient(${JSON.stringify(patient)})'>Edit</button>
                      <button onclick="deletePatient(${patient.id})">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.error("Failed to load patients. Status:", response.status);
            alert("Failed to fetch patients list. Please check server.");
        }
    } catch (error) {
        console.error("Error while loading patients:", error);
    }
}

async function addOrUpdatePatient() {
    const token = localStorage.getItem('access_token');

    const patientData = {
        name: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        address: document.getElementById('address').value,
        phone: document.getElementById('phone').value
    };

    if (editingPatientId) {
        // Update existing patient
        const response = await fetch(`${BASE_URL}/api/patients/${editingPatientId}`, {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(patientData)
        });

        if (response.ok) {
            alert("Patient updated successfully!");
            loadPatients();
            resetForm();
        } else {
            alert("Failed to update patient.");
        }

    } else {
        // Add new patient
        const response = await fetch(`${BASE_URL}/api/patients/`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(patientData)
        });

        if (response.ok) {
            alert("Patient added successfully!");
            loadPatients();
            resetForm();
        } else {
            alert("Failed to add patient.");
        }
    }
}

function editPatient(patient) {
    document.getElementById('name').value = patient.name;
    document.getElementById('age').value = patient.age;
    document.getElementById('gender').value = patient.gender;
    document.getElementById('address').value = patient.address;
    document.getElementById('phone').value = patient.phone;
    
    editingPatientId = patient.id;
    document.getElementById('add-patient-btn').innerText = "Update Patient";
    document.getElementById('form-title').innerText = "Update Patient";
}

function deletePatient(patientId) {
    const token = localStorage.getItem('access_token');

    const confirmDelete = confirm("Are you sure you want to delete this patient?");
    if (!confirmDelete) return;

    fetch(`${BASE_URL}/api/patients/${patientId}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`
        }
    })
    .then(response => {
        if (response.ok) {
            alert("Patient deleted successfully!");
            loadPatients();
        } else {
            alert("Failed to delete patient.");
        }
    })
    .catch(error => console.error("Error:", error));
}

function resetForm() {
    document.getElementById('name').value = "";
    document.getElementById('age').value = "";
    document.getElementById('gender').value = "";
    document.getElementById('address').value = "";
    document.getElementById('phone').value = "";
    editingPatientId = null;
    document.getElementById('add-patient-btn').innerText = "Add Patient";
    document.getElementById('form-title').innerText = "Add New Patient";
}

// ✅ Attach event listener
document.addEventListener('DOMContentLoaded', function() {
    const addPatientBtn = document.getElementById('add-patient-btn');
    if (addPatientBtn) {
        addPatientBtn.addEventListener('click', addOrUpdatePatient);
    }
});
