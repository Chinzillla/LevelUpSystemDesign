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
      const createdMessage = await createMessage(payload);
      addMessageToList(messagesList, createdMessage);
        form.reset();
    } catch (error) {
        messagesList.innerHTML = `<li>Error: ${error.message}</li>`;
    }
});

messagesList.addEventListener("click", async (event) => {
    const deleteButton = event.target.closest("[data-delete-message-id]");

    if (!deleteButton) {
        return;
    }

    const messageId = deleteButton.dataset.deleteMessageId;

    try {
        await deleteMessage(messageId);

        const messageItem = deleteButton.closest("li");
        messageItem.remove();

        if (messagesList.children.length === 0) {
            messagesList.innerHTML = '<li data-empty-message="true">No messages found.</li>';
        }
    } catch (error) {
        messagesList.innerHTML = `<li>Error: ${error.message}</li>`;
    }
});

loadMessages();