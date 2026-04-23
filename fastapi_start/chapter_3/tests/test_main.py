from task_manager_app.main import app
from fastapi.testclient import TestClient
from task_manager_app.operations import read_all_tasks, read_task
from conftest import TEST_TASKS


client = TestClient(app)


# testing first endpoint
def test_endpoint_read_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == TEST_TASKS
    
# testing second endpoint
def test_endpoint_get_task():
    response = client.get("/tasks/1")
    
    assert response.status_code == 200
    assert response.json() == TEST_TASKS[0]

    response = client.get("/tasks/999")
    assert response.status_code == 404
    
# testing third endpoint

def test_endpoint_create_task():
    new_task = {
        "title": "New Task",
        "description": "This is a new task",
        "status": "Testing"
    }    
    response = client.post("/task", json = new_task)
    assert response.status_code == 200
    assert response.json() == {**new_task, "id": 3}
    assert read_all_tasks().__len__() == 3

# testing the put endpoint


def test_endpoint_update_task():
    updated_field = {"status": "Completed"}
    
    response = client.put("/task/1", json = updated_field)
    assert response.status_code == 200
    assert response.json() == {**TEST_TASKS[0], **updated_field}
    
    response = client.put("/task/999", json = updated_field)
    assert response.status_code == 404

# testing the DELETE endpoint

def test_endpoint_delete_task():
    response = client.delete("/task/2")
    assert response.status_code == 200
    expected_response = {k: v for k, v in TEST_TASKS[1].items() if k != "id"}
    assert response.json() == expected_response
    assert read_task(2) is None
    

