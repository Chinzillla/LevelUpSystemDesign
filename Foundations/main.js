const app = document.getElementById("app");
const form = document.getElementById("message-form");
const messagesList = document.getElementById("messages-list");

app.textContent = "Messages";

// Function to submit and post new message to database
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  const payload = {
    name: formData.get("name"),
    message: formData.get("message"),
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/messages/", {
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

    addMessageToList(payload);
    form.reset();
  } catch (error) {
    messagesList.innerHTML = `<li>Error: ${error.message}</li>`;
  }
});

// Function to fetch and display all messages from database
async function loadMessages(showLoading = false) {
    if (showLoading) {
        messagesList.innerHTML = "<li>Loading Messages...</li>";
    }

  try {
    const response = await fetch("http://127.0.0.1:5000/messages/");
    const messages = await response.json();

    if (!response.ok) {
      throw new Error(messages.error || `HTTP error! status: ${response.status}`);
    }

    if (messages.length === 0) {
      messagesList.innerHTML = '<li data-empty-message="true">No messages found.</li>';
      return;
    }

    messagesList.innerHTML = "";

    messages.forEach((message) => {
      const li = document.createElement("li");
      li.textContent = `${message.name}: ${message.message}`;
      messagesList.appendChild(li);
    });
  } catch (error) {
    messagesList.innerHTML = `<li>Error: ${error.message}</li>`;
  }
}

function addMessageToList(message) {
  const emptyMessage = messagesList.querySelector("[data-empty-message]");

  if (emptyMessage) {
    emptyMessage.remove();
  }

  const li = document.createElement("li");
  li.textContent = `${message.name}: ${message.message}`;
  messagesList.appendChild(li);
}

loadMessages();