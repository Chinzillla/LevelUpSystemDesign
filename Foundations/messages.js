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
    li.dataset.messageName = message.name;
    li.dataset.messageBody = message.message;

    const text = document.createElement("span");
    text.dataset.messageText = "true";
    text.textContent = `${message.name}: ${message.message}`;

    const editButton = document.createElement("button");
    editButton.type = "button";
    editButton.textContent = "Edit";
    editButton.dataset.editMessageId = message.id;

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.textContent = "Delete";
    deleteButton.dataset.deleteMessageId = message.id;

    li.appendChild(text);
    li.appendChild(editButton);
    li.appendChild(deleteButton);
    messagesList.appendChild(li);
}

function updateMessageInList(messagesList, message) {
    const messageItem = messagesList.querySelector(`[data-message-id="${message.id}"]`);

    if (!messageItem) {
        addMessageToList(messagesList, message);
        return;
    }

    const text = messageItem.querySelector("[data-message-text]");
    messageItem.dataset.messageName = message.name;
    messageItem.dataset.messageBody = message.message;
    text.textContent = `${message.name}: ${message.message}`;
}