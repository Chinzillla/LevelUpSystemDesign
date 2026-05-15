const API_BASE_URL = "http://127.0.0.1:5000";

async function getMessages() {
  const response = await fetch(`${API_BASE_URL}/messages/`);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || `HTTP error! status: ${response.status}`);
  }

  return data;
}

async function createMessage(payload) {
  const response = await fetch(`${API_BASE_URL}/messages/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || `HTTP error! status: ${response.status}`);
  }

  return data;
}