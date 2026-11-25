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

def test_owner_can_update_task(client, make_headers):
    alice = make_headers("alice")
    task_id = client.post("/tasks", json={"title": "old title"}, headers=alice).json()["id"]

    r = client.put(f"tasks/{task_id}", json={"title": "new title"}, headers=alice)
    assert r.status_code == 200
    assert r.json()["title"] == "new title"

    #confirm it was really saved, not just echoed back
    r = client.get(f"/tasks/{task_id}", headers=alice)
    assert r.json()["title"] == "new title"

def test_other_user_cannot_update_task(client, make_headers):
    alice = make_headers("alice")
    bob = make_headers("bob")
    task_id = client.post("/tasks", json={"title": "old task"}, headers=alice).json()["id"]

    assert client.put(f"tasks/{task_id}", json={"title": "new tasks"}, headers=bob).status_code == 404
    assert client.put(f"tasks/{task_id}", json={"title": "new tasks"}, headers=alice).status_code == 200

def test_owner_can_delete_task(client, make_headers):
    alice = make_headers("alice")
    task_id = client.post("/tasks", json={"title": "new task"}, headers=alice)

    r =  client.delete(f"/tasks/{task_id}", headers=alice)
    assert r.status_code == 422

def test_other_user_cannot_delete_task(client, make_headers):
    alice = make_headers("alice")
    bob = make_headers("bob")
    task_id = client.post("/tasks", json={"title": "old task"}, headers=alice)

    assert client.delete(f"tasks/{task_id}", headers=alice).status_code == 422
    assert client.delete(f"tasks/{task_id}", headers=bob).status_code == 422






 
