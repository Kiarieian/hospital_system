document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const admitForm = document.getElementById("admitForm");

  // LOGIN
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const res = await fetch("/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          username: document.getElementById("username").value,
          password: document.getElementById("password").value
        })
      });

      const data = await res.json();
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "/dashboard";
      } else {
        document.getElementById("msg").textContent = "Login failed!";
      }
    });
  }

  // ADMIT PATIENT
  if (admitForm) {
    admitForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const token = localStorage.getItem("token");

      const patient = {
        full_name: document.getElementById("full_name").value,
        ward_type: document.getElementById("ward_type").value,
        address: document.getElementById("address").value,
        contact: document.getElementById("contact").value,
        gender: "female",
        date_of_birth: "2000-01-01"
      };

      const res = await fetch("/patients", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(patient)
      });

      const data = await res.json();
      document.getElementById("admitMsg").textContent = data.full_name
        ? `Admitted ${data.full_name} successfully`
        : "Error admitting patient.";
    });
  }

  // DISPLAY PATIENTS
  if (document.getElementById("patientsTable")) {
    (async () => {
      const res = await fetch("/patients");
      const patients = await res.json();
      const tbody = document.querySelector("#patientsTable tbody");
      patients.forEach(p => {
        const row = `<tr>
          <td>${p.id}</td>
          <td>${p.full_name}</td>
          <td>${p.ward_type}</td>
          <td>${p.contact}</td>
          <td>${p.address}</td>
        </tr>`;
        tbody.innerHTML += row;
      });
    })();
  }
});
