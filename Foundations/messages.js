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
    li.dataset.messageId = message.id;

    const text = document.createElement("span");
    text.textContent = `${message.name}: ${message.message}`;

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.textContent = "Delete";
    deleteButton.dataset.deleteMessageId = message.id;

    li.appendChild(text);
    li.appendChild(deleteButton);
    messagesList.appendChild(li);
}