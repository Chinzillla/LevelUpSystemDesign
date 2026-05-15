const app = document.getElementById("app");
const form = document.getElementById("message-form");
const messagesList = document.getElementById("messages-list");
const submitButton = document.getElementById("submit");
const cancelEditButton = document.getElementById("cancel-edit");

let editingMessageId = null;

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
        if (editingMessageId) {
            const updatedMessage = await updateMessage(editingMessageId, payload);
            updateMessageInList(messagesList, updatedMessage);
            stopEditing();
            return;
        }

        const createdMessage = await createMessage(payload);
        addMessageToList(messagesList, createdMessage);
        form.reset();
    } catch (error) {
        messagesList.innerHTML = `<li>Error: ${error.message}</li>`;
    }
});

messagesList.addEventListener("click", async (event) => {
    const editButton = event.target.closest("[data-edit-message-id]");
    const deleteButton = event.target.closest("[data-delete-message-id]");

    if (editButton) {
        const messageItem = editButton.closest("li");

        editingMessageId = editButton.dataset.editMessageId;
        form.elements.name.value = messageItem.dataset.messageName;
        form.elements.message.value = messageItem.dataset.messageBody;
        submitButton.textContent = "Update";
        cancelEditButton.hidden = false;
        form.elements.name.focus();
        return;
    }

    if (!deleteButton) {
        return;
    }

    const messageId = deleteButton.dataset.deleteMessageId;

    try {
        await deleteMessage(messageId);

        const messageItem = deleteButton.closest("li");
        messageItem.remove();

        if (messageId === editingMessageId) {
            stopEditing();
        }

        if (messagesList.children.length === 0) {
            messagesList.innerHTML = '<li data-empty-message="true">No messages found.</li>';
        }
    } catch (error) {
        messagesList.innerHTML = `<li>Error: ${error.message}</li>`;
    }
});

cancelEditButton.addEventListener("click", () => {
    stopEditing();
});

function stopEditing() {
    editingMessageId = null;
    form.reset();
    submitButton.textContent = "Submit";
    cancelEditButton.hidden = true;
}

loadMessages();