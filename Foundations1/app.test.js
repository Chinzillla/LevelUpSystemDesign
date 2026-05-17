const test = require("node:test");
const assert = require("node:assert/strict");

const {
    API_BASE_URL,
    SESSION_TOKEN_KEY,
    buildAuthHeader,
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
    buildCreateItemPayload,
    buildUpdateItemPayload,
    replaceItemByName,
    removeItemByName,
    renderItemHtml,
    renderItemsHtml,
} = require("./app.js");

function mockResponse(data, ok = true, status = 200) {
    return {
        ok,
        status,
        json: async () => data,
    };
}

function createMemoryStorage() {
    const values = new Map();

    return {
        getItem(key) {
            return values.has(key) ? values.get(key) : null;
        },
        setItem(key, value) {
            values.set(key, value);
        },
        removeItem(key) {
            values.delete(key);
        },
    };
}

test("requestJson returns parsed response data", async () => {
    global.fetch = async (url, options) => {
        assert.equal(url, `${API_BASE_URL}/health/`);
        assert.deepEqual(options, { method: "GET" });
        return mockResponse({ ok: true });
    };

    assert.deepEqual(await requestJson("/health/", { method: "GET" }), { ok: true });
});

test("requestJson throws backend error messages", async () => {
    global.fetch = async () => mockResponse({ error: "Invalid session" }, false, 401);

    await assert.rejects(
        () => requestJson("/items/list", { method: "GET" }),
        /Invalid session/
    );
});

test("session helpers save, load, and clear the token", () => {
    const storage = createMemoryStorage();

    saveSessionToken("token-123", storage);

    assert.equal(storage.getItem(SESSION_TOKEN_KEY), "token-123");
    assert.equal(loadSessionToken(storage), "token-123");

    clearSessionToken(storage);

    assert.equal(loadSessionToken(storage), null);
});

test("buildAuthHeader creates a bearer auth header", () => {
    assert.deepEqual(buildAuthHeader("token-123"), {
        "Authorization": "Bearer token-123",
    });
});

test("registerUser posts credentials", async () => {
    const payload = { email: "test@example.com", password: "hellothere!" };

    global.fetch = async (url, options) => {
        assert.equal(url, `${API_BASE_URL}/auth/register`);
        assert.equal(options.method, "POST");
        assert.equal(options.headers["Content-Type"], "application/json");
        assert.deepEqual(JSON.parse(options.body), payload);
        return mockResponse({ message: "You are registered!" }, true, 201);
    };

    assert.equal((await registerUser(payload)).message, "You are registered!");
});

test("loginUser posts credentials", async () => {
    const payload = { email: "test@example.com", password: "hellothere!" };

    global.fetch = async (url, options) => {
        assert.equal(url, `${API_BASE_URL}/auth/login`);
        assert.equal(options.method, "POST");
        assert.deepEqual(JSON.parse(options.body), payload);
        return mockResponse({ session_token: "abc123" });
    };

    assert.equal((await loginUser(payload)).session_token, "abc123");
});

test("logoutUser sends bearer token", async () => {
    global.fetch = async (url, options) => {
        assert.equal(url, `${API_BASE_URL}/auth/logout`);
        assert.equal(options.method, "POST");
        assert.equal(options.headers.Authorization, "Bearer token-123");
        return mockResponse({ message: "Logout successful" });
    };

    assert.equal((await logoutUser("token-123")).message, "Logout successful");
});

test("listItems sends bearer token", async () => {
    global.fetch = async (url, options) => {
        assert.equal(url, `${API_BASE_URL}/items/list`);
        assert.equal(options.method, "GET");
        assert.equal(options.headers.Authorization, "Bearer token-123");
        return mockResponse({ items: [] });
    };

    assert.deepEqual((await listItems("token-123")).items, []);
});

test("createItem posts an item payload", async () => {
    global.fetch = async (url, options) => {
        assert.equal(url, `${API_BASE_URL}/items/create`);
        assert.equal(options.method, "POST");
        assert.equal(options.headers.Authorization, "Bearer token-123");
        assert.deepEqual(JSON.parse(options.body), { name: "book" });
        return mockResponse({ name: "book" }, true, 201);
    };

    assert.equal((await createItem({ name: "book" }, "token-123")).name, "book");
});

test("updateItem sends update payload", async () => {
    const payload = { name: "book", new_name: "notebook", completed: true };

    global.fetch = async (url, options) => {
        assert.equal(url, `${API_BASE_URL}/items/update`);
        assert.equal(options.method, "PUT");
        assert.equal(options.headers.Authorization, "Bearer token-123");
        assert.deepEqual(JSON.parse(options.body), payload);
        return mockResponse({ name: "notebook", completed: true });
    };

    assert.equal((await updateItem(payload, "token-123")).name, "notebook");
});

test("deleteItem sends name payload", async () => {
    global.fetch = async (url, options) => {
        assert.equal(url, `${API_BASE_URL}/items/delete`);
        assert.equal(options.method, "DELETE");
        assert.equal(options.headers.Authorization, "Bearer token-123");
        assert.deepEqual(JSON.parse(options.body), { name: "book" });
        return mockResponse({ name: "book" });
    };

    assert.equal((await deleteItem("book", "token-123")).name, "book");
});

test("buildCreateItemPayload trims the item name", () => {
    const form = new FormData();
    form.set("name", "  book  ");

    assert.deepEqual(buildCreateItemPayload(form), { name: "book" });
});

test("renderItemHtml renders item name and status", () => {
    const html = renderItemHtml({ name: "book", completed: false });

    assert.match(html, /book/);
    assert.match(html, /data-item-update-form/);
    assert.match(html, /data-delete-item-name="book"/);
    assert.match(html, /data-item-name="book"/);
});

test("renderItemHtml escapes user-controlled item names", () => {
    const html = renderItemHtml({ name: "<script>", completed: true });

    assert.match(html, /&lt;script&gt;/);
    assert.match(html, /checked/);
    assert.doesNotMatch(html, /<script>/);
});

test("renderItemsHtml renders an empty state", () => {
    assert.equal(renderItemsHtml([]), '<li class="empty-state">No items yet.</li>');
});

test("buildUpdateItemPayload trims new name and preserves current name", () => {
    assert.deepEqual(buildUpdateItemPayload("book", "  notebook  ", true), {
        name: "book",
        new_name: "notebook",
        completed: true,
    });
});

test("replaceItemByName replaces only the matching item", () => {
    const items = [
        { name: "book", completed: false },
        { name: "pen", completed: false },
    ];

    assert.deepEqual(replaceItemByName(items, "book", { name: "notebook", completed: true }), [
        { name: "notebook", completed: true },
        { name: "pen", completed: false },
    ]);
});

test("removeItemByName removes only the matching item", () => {
    const items = [
        { name: "book", completed: false },
        { name: "pen", completed: false },
    ];

    assert.deepEqual(removeItemByName(items, "book"), [
        { name: "pen", completed: false },
    ]);
});
