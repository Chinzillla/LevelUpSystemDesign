const API_BASE_URL = "http://127.0.0.1:5000";
const SESSION_TOKEN_KEY = "foundations1.sessionToken";

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

function saveSessionToken(sessionToken, storage = localStorage) {
    storage.setItem(SESSION_TOKEN_KEY, sessionToken);
}

function loadSessionToken(storage = localStorage) {
    return storage.getItem(SESSION_TOKEN_KEY);
}

function clearSessionToken(storage = localStorage) {
    storage.removeItem(SESSION_TOKEN_KEY);
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

function getFormPayload(form) {
    const formData = form instanceof FormData ? form : new FormData(form);

    return Object.fromEntries(formData.entries());
}

function buildCreateItemPayload(form) {
    const data = getFormPayload(form);

    return {
        name: data.name.trim(),
    };
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderItemHtml(item) {
    const status = item.completed ? "Completed" : "Active";

    return `
        <li class="item-row" data-item-name="${escapeHtml(item.name)}">
            <div>
                <span class="item-name">${escapeHtml(item.name)}</span>
                <span class="item-meta">${status}</span>
            </div>
        </li>
    `;
}

function renderItemsHtml(items) {
    if (items.length === 0) {
        return '<li class="empty-state">No items yet.</li>';
    }

    return items.map(renderItemHtml).join("");
}

function renderItems(itemList, items) {
    itemList.innerHTML = renderItemsHtml(items);
}

function getAppElements(documentRoot = document) {
    return {
        authView: documentRoot.getElementById("auth-view"),
        appView: documentRoot.getElementById("app-view"),
        registerForm: documentRoot.getElementById("register-form"),
        loginForm: documentRoot.getElementById("login-form"),
        logoutButton: documentRoot.getElementById("logout-button"),
        authStatus: documentRoot.getElementById("auth-status"),
        itemForm: documentRoot.getElementById("item-form"),
        itemList: documentRoot.getElementById("item-list"),
        itemStatus: documentRoot.getElementById("item-status"),
    };
}

function showAuthView(elements) {
    elements.authView.classList.remove("hidden");
    elements.appView.classList.add("hidden");
}

function showAppView(elements) {
    elements.authView.classList.add("hidden");
    elements.appView.classList.remove("hidden");
}

function setAuthStatus(elements, message) {
    elements.authStatus.textContent = message;
}

function setItemStatus(elements, message) {
    elements.itemStatus.textContent = message;
}

async function loadAndRenderItems(elements, sessionToken) {
    const data = await listItems(sessionToken);
    renderItems(elements.itemList, data.items);
}

function initializeApp(documentRoot = document, storage = localStorage) {
    const elements = getAppElements(documentRoot);

    if (!elements.authView || !elements.appView) {
        return null;
    }

    elements.registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            await registerUser(getFormPayload(elements.registerForm));
            elements.registerForm.reset();
            setAuthStatus(elements, "Account created. You can sign in now.");
        } catch (error) {
            setAuthStatus(elements, error.message);
        }
    });

    elements.loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            const data = await loginUser(getFormPayload(elements.loginForm));
            saveSessionToken(data.session_token, storage);
            elements.loginForm.reset();
            setAuthStatus(elements, "");
            showAppView(elements);
            await loadAndRenderItems(elements, data.session_token);
        } catch (error) {
            setAuthStatus(elements, error.message);
        }
    });

    elements.logoutButton.addEventListener("click", async () => {
        const sessionToken = loadSessionToken(storage);

        try {
            if (sessionToken) {
                await logoutUser(sessionToken);
            }
        } catch (error) {
            setAuthStatus(elements, error.message);
        } finally {
            clearSessionToken(storage);
            showAuthView(elements);
        }
    });

    elements.itemForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const sessionToken = loadSessionToken(storage);

        try {
            const item = await createItem(buildCreateItemPayload(elements.itemForm), sessionToken);
            elements.itemForm.reset();
            setItemStatus(elements, `${item.name} created.`);
            await loadAndRenderItems(elements, sessionToken);
        } catch (error) {
            setItemStatus(elements, error.message);
        }
    });

    const currentToken = loadSessionToken(storage);

    if (currentToken) {
        showAppView(elements);
        loadAndRenderItems(elements, currentToken).catch((error) => {
            setItemStatus(elements, error.message);
        });
    } else {
        showAuthView(elements);
    }

    return elements;
}

if (typeof document !== "undefined") {
    initializeApp();
}

if (typeof module !== "undefined") {
    module.exports = {
        API_BASE_URL,
        SESSION_TOKEN_KEY,
        buildAuthHeader,
        buildJsonHeaders,
        saveSessionToken,
        loadSessionToken,
        clearSessionToken,
        requestJson,
        registerUser,
        loginUser,
        logoutUser,
        listItems,
        createItem,
        updateItem,
        deleteItem,
        getFormPayload,
        buildCreateItemPayload,
        escapeHtml,
        renderItemHtml,
        renderItemsHtml,
        renderItems,
        getAppElements,
        showAuthView,
        showAppView,
        initializeApp,
    };
}
