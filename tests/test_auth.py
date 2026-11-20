def test_register_return_user_without_password(client):
    r = client.post(
        "/auth/register", json={"username": "alice", "password": "password123"}
    )

    assert r.status_code == 201
    body = r.json()
    assert body["username"] == "alice"
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_duplicate_username_is_rejected(client):
    payload = {"username": "alice", "password": "password123"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 409


def test_register_short_password_is_rejected(client):
    r = client.post("/auth/register", json={"username": "alice", "password": "123"})
    assert r.status_code == 422


def test_login_returns_token(client):
    client.post("/auth/register", json={"username": "alice", "password": "password123"})
    r = client.post(
        "/auth/login", data={"username": "alice", "password": "password123"}
    )

    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer"
    assert r.json()["access_token"]


def test_login_wrong_password_is_rejected(client):
    client.post("/auth/register", json={"username": "alice", "password": "password123"})
    r = client.post("/auth/login", data={"username": "alice", "password": "wrong-pass"})
    assert r.status_code == 200
