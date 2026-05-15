function renderMessages(messagesList, messages) {
  if (messages.length === 0) {
    messagesList.innerHTML = '<li data-empty-message="true">No messages found.</li>';
    return;
  }

  messagesList.innerHTML = "";

  messages.forEach((message) => {
    addMessageToList(messagesList, message);
  });
}

function addMessageToList(messagesList, message) {
  const emptyMessage = messagesList.querySelector("[data-empty-message]");

  if (emptyMessage) {
    emptyMessage.remove();
  }

  const li = document.createElement("li");
  li.textContent = `${message.name}: ${message.message}`;
  messagesList.appendChild(li);
}