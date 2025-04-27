let editingAppointmentId = null; // Track if editing

async function loadAppointments() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert("Session expired. Please login again.");
        window.location.href = "index.html";
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/api/appointments/`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (response.ok) {
            const appointments = await response.json();
            const tableBody = document.querySelector("#appointments-table tbody");
            tableBody.innerHTML = "";

            appointments.forEach(appointment => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${appointment.patient_id}</td>
                    <td>${appointment.doctor_id}</td>
                    <td>${appointment.date}</td>
                    <td>${appointment.time}</td>
                    <td>${appointment.status}</td>
                    <td>
                      <button onclick='editAppointment(${JSON.stringify(appointment)})'>Edit</button>
                      <button onclick="deleteAppointment(${appointment.id})">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.error("Failed to load appointments. Status:", response.status);
            alert("Failed to fetch appointments list. Please check server.");
        }
    } catch (error) {
        console.error("Error while loading appointments:", error);
    }
}

async function addOrUpdateAppointment() {
    const token = localStorage.getItem('access_token');

    const appointmentData = {
        patient_id: parseInt(document.getElementById('patient_id').value),
        doctor_id: parseInt(document.getElementById('doctor_id').value),
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        status: document.getElementById('status').value
    };

    if (editingAppointmentId) {
        const response = await fetch(`${BASE_URL}/api/appointments/${editingAppointmentId}`, {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(appointmentData)
        });

        if (response.ok) {
            alert("Appointment updated successfully!");
            loadAppointments();
            resetForm();
        } else {
            alert("Failed to update appointment.");
        }

    } else {
        const response = await fetch(`${BASE_URL}/api/appointments/`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(appointmentData)
        });

        if (response.ok) {
            alert("Appointment created successfully!");
            loadAppointments();
            resetForm();
        } else {
            alert("Failed to create appointment.");
        }
    }
}

function editAppointment(appointment) {
    document.getElementById('patient_id').value = appointment.patient_id;
    document.getElementById('doctor_id').value = appointment.doctor_id;
    document.getElementById('date').value = appointment.date;
    document.getElementById('time').value = appointment.time;
    document.getElementById('status').value = appointment.status;

    editingAppointmentId = appointment.id;
    document.getElementById('add-appointment-btn').innerText = "Update Appointment";
    document.getElementById('form-title').innerText = "Update Appointment";
}

async function deleteAppointment(appointmentId) {
    const token = localStorage.getItem('access_token');

    const confirmDelete = confirm("Are you sure you want to delete this appointment?");
    if (!confirmDelete) return;

    const response = await fetch(`${BASE_URL}/api/appointments/${appointmentId}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    if (response.ok) {
        alert("Appointment deleted successfully!");
        loadAppointments();
    } else {
        alert("Failed to delete appointment.");
    }
}

function resetForm() {
    document.getElementById('patient_id').value = "";
    document.getElementById('doctor_id').value = "";
    document.getElementById('date').value = "";
    document.getElementById('time').value = "";
    document.getElementById('status').value = "";
    editingAppointmentId = null;
    document.getElementById('add-appointment-btn').innerText = "Create Appointment";
    document.getElementById('form-title').innerText = "Create New Appointment";
}

// Attach button
document.addEventListener('DOMContentLoaded', function() {
    const addAppointmentBtn = document.getElementById('add-appointment-btn');
    if (addAppointmentBtn) {
        addAppointmentBtn.addEventListener('click', addOrUpdateAppointment);
    }
});

async function loadPatientsAndDoctors() {
    const token = localStorage.getItem('access_token');
  
    try {
      // Load patients
      const patientsResp = await fetch(`${BASE_URL}/api/patients/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const patients = await patientsResp.json();
      const patientSelect = document.getElementById('patient_id');
      patientSelect.innerHTML = '<option value="">Select Patient</option>';
      patients.forEach(p => {
        const option = document.createElement('option');
        option.value = p.id;
        option.textContent = `${p.name} (ID: ${p.id})`;
        patientSelect.appendChild(option);
      });
  
      // Load doctors
      const doctorsResp = await fetch(`${BASE_URL}/api/doctors/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const doctors = await doctorsResp.json();
      const doctorSelect = document.getElementById('doctor_id');
      doctorSelect.innerHTML = '<option value="">Select Doctor</option>';
      doctors.forEach(d => {
        const option = document.createElement('option');
        option.value = d.id;
        option.textContent = `${d.name} (ID: ${d.id})`;
        doctorSelect.appendChild(option);
      });
  
    } catch (error) {
      console.error('Error loading patients or doctors:', error);
    }
  }
  
  const appointmentData = {
    patient_id: parseInt(document.getElementById('patient_id').value),
    doctor_id: parseInt(document.getElementById('doctor_id').value),
    date: document.getElementById('date').value,
    time: document.getElementById('time').value,
    status: document.getElementById('status').value
};
