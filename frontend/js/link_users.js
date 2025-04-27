async function loadLinkingData() {
    const token = localStorage.getItem('access_token');
  
    const [patientsRes, doctorsRes, usersRes] = await Promise.all([
      fetch(`${BASE_URL}/patients/`, { headers: { Authorization: `Bearer ${token}` } }),
      fetch(`${BASE_URL}/doctors/`, { headers: { Authorization: `Bearer ${token}` } }),
      fetch(`${BASE_URL}/users/`, { headers: { Authorization: `Bearer ${token}` } }),
    ]);
  
    const patients = await patientsRes.json();
    const doctors = await doctorsRes.json();
    const users = await usersRes.json();
  
    // Get IDs of already linked users
    const linkedUserIds = [
      ...patients.filter(p => p.user_id !== null).map(p => p.user_id),
      ...doctors.filter(d => d.user_id !== null).map(d => d.user_id)
    ];
  
    // Filter out already linked users
    const availableUsers = users.filter(user => !linkedUserIds.includes(user.id));
  
    // Populate unlinked patients
    const unlinkedPatients = patients.filter(p => !p.user_id);
    const patientsDropdown = document.getElementById('unlinked-patients');
    patientsDropdown.innerHTML = `<option value="">Select Patient</option>`;
    unlinkedPatients.forEach(patient => {
      patientsDropdown.innerHTML += `<option value="${patient.id}">${patient.name}</option>`;
    });
  
    // Populate unlinked doctors
    const unlinkedDoctors = doctors.filter(d => !d.user_id);
    const doctorsDropdown = document.getElementById('unlinked-doctors');
    doctorsDropdown.innerHTML = `<option value="">Select Doctor</option>`;
    unlinkedDoctors.forEach(doctor => {
      doctorsDropdown.innerHTML += `<option value="${doctor.id}">${doctor.name}</option>`;
    });
  
    // Populate available users for patients
    const usersPatientDropdown = document.getElementById('available-users-patient');
    usersPatientDropdown.innerHTML = `<option value="">Select User</option>`;
    availableUsers.forEach(user => {
      usersPatientDropdown.innerHTML += `<option value="${user.id}">${user.username} (${user.role})</option>`;
    });
  
    // Populate available users for doctors
    const usersDoctorDropdown = document.getElementById('available-users-doctor');
    usersDoctorDropdown.innerHTML = `<option value="">Select User</option>`;
    availableUsers.forEach(user => {
      usersDoctorDropdown.innerHTML += `<option value="${user.id}">${user.username} (${user.role})</option>`;
    });
  }
  
  
  async function linkPatientToUser() {
    const token = localStorage.getItem('access_token');
    const patientId = document.getElementById('unlinked-patients').value;
    const userId = document.getElementById('available-users-patient').value;
  
    try {
      const resp = await fetch(`${BASE_URL}/patients/link_user/${patientId}?user_id=${userId}`, {
        method: "PUT",
        headers: { Authorization: `Bearer ${token}` }
      });
      if (resp.ok) {
        alert('Patient linked successfully!');
        loadLinkingData();
      } else {
        alert('Failed to link patient.');
      }
    } catch (error) {
      console.error('Error linking patient:', error);
    }
  }
  
  async function linkDoctorToUser() {
    const token = localStorage.getItem('access_token');
    const doctorId = document.getElementById('unlinked-doctors').value;
    const userId = document.getElementById('available-users-doctor').value;
  
    try {
      const resp = await fetch(`${BASE_URL}/doctors/link_user/${doctorId}?user_id=${userId}`, {
        method: "PUT",
        headers: { Authorization: `Bearer ${token}` }
      });
      if (resp.ok) {
        alert('Doctor linked successfully!');
        loadLinkingData();
      } else {
        alert('Failed to link doctor.');
      }
    } catch (error) {
      console.error('Error linking doctor:', error);
    }
  }
  