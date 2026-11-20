def test_tasks_require_login(client):
    assert client.get("/tasks").status_code == 401


def test_create_tasks(client, make_headers):

    headers = make_headers("alice")
    r = client.post("/tasks", json={"title": "Write Test"}, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Write Test"
    assert data["done"] is False
    assert "id" in data


def test_create_task_without_title_is_rejected(client, make_headers):

    headers = make_headers("alice")
    r = client.post("/tasks", json={"description": "no title"}, headers=headers)
    assert r.status_code == 422


def test_list_returns_only_own_tasks(client, make_headers):
    alice = make_headers("alice")
    bob = make_headers("bob")
    client.post("/tasks", json={"title": "alice task"}, headers=alice)

    assert client.get("/tasks", headers=bob).json() == []
    assert len(client.get("/tasks", headers=alice).json()) == 1


def test_other_users_cannot_read_task(client, make_headers):
    alice = make_headers("alice")
    bob = make_headers("bob")

    task_id = client.post("/tasks", json={"title": "private"}, headers=alice).json()[
        "id"
    ]

    assert client.get(f"/tasks/{task_id}", headers=bob).status_code == 404
    assert client.get(f"/tasks/{task_id}", headers=alice).status_code == 200
