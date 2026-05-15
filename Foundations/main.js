const app = document.getElementById("app");
const form = document.getElementById("message-form");
const messagesList = document.getElementById("messages-list");

app.textContent = "Messages";

async function loadMessages() {
  try {
    const messages = await getMessages();
    renderMessages(messagesList, messages);
  } catch (error) {
    messagesList.innerHTML = `<li>Error: ${error.message}</li>`;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  const payload = {
    name: formData.get("name"),
    message: formData.get("message"),
  };

  try {
    await createMessage(payload);
    addMessageToList(messagesList, payload);
    form.reset();
  } catch (error) {
    messagesList.innerHTML = `<li>Error: ${error.message}</li>`;
  }
});

loadMessages();