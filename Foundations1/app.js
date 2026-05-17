const API_BASE_URL = "http://127.0.0.1:5000";

function buildJsonHeaders(headers = {}) {
    return {
        "Content-Type": "application/json",
        ...headers,
    };
}

function buildAuthHeader(sessionToken) {
    return {
        "Authorization": `Bearer ${sessionToken}`,
    };
}

async function requestJson(path, options = {}) {
    const response = await fetch(`${API_BASE_URL}${path}`, options);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
    }

    return data;
}

function registerUser(payload) {
    return requestJson("/auth/register", {
        method: "POST",
        headers: buildJsonHeaders(),
        body: JSON.stringify(payload),
    });
}

function loginUser(payload) {
    return requestJson("/auth/login", {
        method: "POST",
        headers: buildJsonHeaders(),
        body: JSON.stringify(payload),
    });
}

function logoutUser(sessionToken) {
    return requestJson("/auth/logout", {
        method: "POST",
        headers: buildAuthHeader(sessionToken),
    });
}

function listItems(sessionToken) {
    return requestJson("/items/list", {
        method: "GET",
        headers: buildAuthHeader(sessionToken),
    });
}

function createItem(payload, sessionToken) {
    return requestJson("/items/create", {
        method: "POST",
        headers: buildJsonHeaders(buildAuthHeader(sessionToken)),
        body: JSON.stringify(payload),
    });
}

function updateItem(payload, sessionToken) {
    return requestJson("/items/update", {
        method: "PUT",
        headers: buildJsonHeaders(buildAuthHeader(sessionToken)),
        body: JSON.stringify(payload),
    });
}

function deleteItem(name, sessionToken) {
    return requestJson("/items/delete", {
        method: "DELETE",
        headers: buildJsonHeaders(buildAuthHeader(sessionToken)),
        body: JSON.stringify({ name }),
    });
}

if (typeof module !== "undefined") {
    module.exports = {
        API_BASE_URL,
        buildAuthHeader,
        buildJsonHeaders,
        requestJson,
        registerUser,
        loginUser,
        logoutUser,
        listItems,
        createItem,
        updateItem,
        deleteItem,
    };
}
