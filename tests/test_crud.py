def test_create_and_get_todo(client):
    # create a todo
    res = client.post("/todos", json={"title": "Learn Pytest"})
    assert res.status_code == 201
    created = res.get_json()
    assert created["title"] == "Learn Pytest"
    assert "id" in created

    # get todos list
    res = client.get("/todos")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Learn Pytest"

def test_update_todo_success(client):
    # create
    client.post("/todos", json={"title": "Old Task"})
    # update
    res = client.patch("/todos/1", json={"title": "Updated Task"})
    assert res.status_code == 200
    updated = res.get_json()
    assert updated["title"] == "Updated Task"

def test_delete_todo_success(client):
    client.post("/todos", json={"title": "Task to delete"})
    res = client.delete("/todos/1")
    assert res.status_code == 200
    body = res.get_json()
    assert body.get("message") == "Deleted successfully"
    # list now empty
    res = client.get("/todos")
    assert res.get_json() == []
