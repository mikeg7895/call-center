const callsTableBody = document.getElementById("callsTableBody");
const callStats = document.getElementById("callStats");
const importExcelBtn = document.getElementById("importExcelBtn");
const startCallsBtn = document.getElementById("startCallsBtn");
const fileInput = document.getElementById("fileInput");
const form = document.getElementById("fileForm");
const loginModal = document.getElementById('loginModal');
const loginForm = document.getElementById('loginForm');
const incomingCall = document.getElementById('callModal');
const callName = document.getElementById('callName');
const callId = document.getElementById('callId');
const callPhone = document.getElementById('callPhone');
const callReason = document.getElementById('callReason');
const logoutBtn = document.getElementById('logoutBtn');
const logoutModal = document.getElementById('logoutModal');
const btnCancel = document.getElementById('cancel');
const btnLogout = document.getElementById('logoutAccepted');
const btnDelete = document.getElementById('deleteCallsBtn');
const deleteModal = document.getElementById('deleteModal');
const cancelDelete = document.getElementById('cancelDelete');
const deleteAccepted = document.getElementById('deleteAccepted');
const exportBtn = document.getElementById('exportExcelBtn');

function handleLogin(formData) {
  fetch("/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  })
    .then((res) => res.json())
    .then((data) => {
      let err = document.getElementById('loginError');
      if(data.error) {
        console.log(data.error);
        err.style.display = 'block'
        return;
      }
      loginModal.style.display = 'none';
      err.style.display = 'none';
      getClients();
      createWebSocketConnection();
    })
    .catch((err) => {
      console.log(err);
    });
}

loginForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value;
  const key = document.getElementById('key').value;
  const formData = new URLSearchParams();
  formData.append('grant_type', 'password');
  formData.append('username', name);
  formData.append('password', key);
  formData.append('scope', '');
  formData.append('client_id', 'string');
  formData.append('client_secret', 'string');
  handleLogin(formData);
});

logoutBtn.addEventListener('click', () => {
  logoutModal.style.display = 'flex';
});

btnCancel.addEventListener('click', () => {
  logoutModal.style.display = 'none';
});

btnLogout.addEventListener('click', () => {
  fetch("/logout/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if(data.error) {
        console.log(data.error);
        return;
      }
      console.log(data.data);
      logoutModal.style.display = 'none';
      loginModal.style.display = 'flex';
      ws.close();
      callsTableBody.innerHTML = "";
    })
    .catch((err) => {
      console.log(err);
    });
});

cancelDelete.addEventListener('click', () => {
  deleteModal.style.display = 'none';
});

deleteAccepted.addEventListener('click', () => {
  fetch("/clients/", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if(data.error) {
        console.log(data.error);
        return;
      }
      console.log(data.data);
      callsTableBody.innerHTML = "";
      deleteModal.style.display = 'none';
      callStats.innerHTML = `
        <p>Total de llamadas: 0</p>
        <p>Llamadas pendientes: 0</p>
        <p>Llamadas contestadas: 0</p>
        `;
    });
});

btnDelete.addEventListener('click', () => {
  deleteModal.style.display = 'flex';
});

exportBtn.addEventListener('click', async () => {
  if(!callsTableBody.innerHTML) {
    alert("No hay llamadas para exportar");
    return;
  }
  fetch("/export/", {
    method: "GET",
  })
    .then( async (res) => {
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'clients.xlsx';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a); 
    }) 
    /*.then((data) => {
      console.log(data);
      if(data.error) {
        console.log(data.error);
        return;
      }
      const blob = data.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'clients.xlsx';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    }*/
});

// Función para mostrar las llamadas en la tabla
function renderCalls(calls) {
  callsTableBody.innerHTML = "";
  calls.forEach((call) => {
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${call.id}</td>
        <td>${call.name}</td>
        <td>${call.phone_number}</td>
        <td>${call.reason}</td>
        <td>
          ${
            call.status === "En curso"
              ? `<button class="small-btn" onclick="handleCallAnswered(${call.id})">Contestada</button>`
              : ""
          }
        </td>
      `;
    callsTableBody.appendChild(row);
  });
  updateStats(calls);
}

function getClients(){
  fetch("/clients", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer`,
    },
  })
    .then((res) => res.json())
    .then((data) => {
      if(data.error) {
        console.log(data.error);
        return;
      }
      renderCalls(data.data);
    })
    .catch((err) => {
      console.log(err);
    });
}

// Función para actualizar las estadísticas de las llamadas
function updateStats(calls) {
  const total = calls.length;
  //const pending = calls.filter((c) => c.status === "Pendiente").length;
  //const inProgress = calls.filter((c) => c.status === "En curso").length;
  //const answered = calls.filter((c) => c.status === "Contestada").length;

  callStats.innerHTML = `
      <p>Total de llamadas: ${total}</p>
      <p>Llamadas pendientes: ${0}</p>
      <p>Llamadas contestadas: ${0}</p>
    `;
}

// Función para manejar llamadas contestadas
function handleCallAnswered(id) {
  const call = calls.find((call) => call.id === id);
  if (call) {
    call.status = "Contestada";
    toastr.success(`Llamada ${id} contestada!`);
    renderCalls();
  }
}

importExcelBtn.addEventListener("click", () => {
  fileInput.click();
});

startCallsBtn.addEventListener("click", () => {
  fetch("/start-calls")
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if(data.error) {
        console.log(data.error);
        return;
      }
      if(data.detail == "Ya se ha iniciado el proceso") {
        alert("Ya hay un proceso de llamadas en curso");
      }
    })
    .catch((err) => {
      console.log(err);
    });
});

fileInput.addEventListener("change", (e) => {
  form.dispatchEvent(new Event("submit"));
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      if(data.error || data.data.error) {
        console.log(data.error);
        return;
      }
      console.log(data);
      renderCalls(data.data);
      fileInput.value = "";
    })
    .catch((err) => {
      console.log(err);
    });
});

function getCookie(name) {
  const cookies = document.cookie.split('; ');
  for (let cookie of cookies) {
    const [key, value] = cookie.split('=');
    if (key === name) {
      return decodeURIComponent(value);
    }
  }
  return null;
}

let ws = null;

function createWebSocketConnection() {
  if (ws && ws.readyState === WebSocket.OPEN) {
    return;
  }

  ws = new WebSocket("ws://localhost:8000/ws/?token=" + getCookie('session_call'));

  ws.onopen = () => {
    console.log("Connected to the server");
  };

  ws.onmessage = (event) => {
    const data_json = JSON.parse(event.data);
    if (data_json.call_incoming) {
      callName.innerText = data_json.client.name;
      callId.innerText = data_json.client.document;
      callPhone.innerText = data_json.client.phone_number;
      callReason.innerText = data_json.client.reason;
      incomingCall.style.display = 'flex';
    }
    if (data_json.finished) {
      incomingCall.style.display = 'none';
    }
  };


  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
}

document.addEventListener("DOMContentLoaded", () => {
  const user = getCookie('session_call');
  if (!user) {
    loginModal.style.display = 'flex';
    return;
  }
  getClients();

  createWebSocketConnection();
});
