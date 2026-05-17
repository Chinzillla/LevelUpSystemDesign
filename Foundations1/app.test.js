const test = require("node:test");
const assert = require("node:assert/strict");

const {
    API_BASE_URL,
    requestJson,
    registerUser,
    loginUser,
    logoutUser,
    listItems,
    createItem,
    updateItem,
    deleteItem,
} = require("./app.js");

function mockResponse(data, ok = true, status = 200) {
    return {
        ok,
        status,
        json: async () => data,
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
