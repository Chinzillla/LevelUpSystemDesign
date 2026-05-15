def test_login_rejects_wrong_password(client):
    response_reg = client.post("/auth/register", json ={
        "email":"test@example.com",
        "password":"hellothere!"
    })
    response_login = client.get("/auth/login", json = {
        "email":"test@example.com",
        "password":"hellothere"
    })

    assert response_reg.status_code == 201
    assert response_login.status_code == 401
    assert response_login.get_json() == {
        "error": "Invalid email or password"
    }

def test_login_correct_password(client):
    response_reg = client.post("/auth/register", json ={
        "email":"test1@example.com",
        "password":"hellothere!"
    })
    response_login = client.get("/auth/login", json = {
        "email":"test1@example.com",
        "password":"hellothere!"
    })

    assert response_reg.status_code == 201
    assert response_login.status_code == 200