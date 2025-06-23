from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from models import (Task, TaskWithID)
from operations import read_all_tasks, read_task, create_task, modify_task, remove_task

app = FastAPI()

# READ operations
@app.get("/tasks", response_model=list[TaskWithID])
def get_tasks():
    """Get all tasks from the DB

    Returns:
        List: A list of Tasks with ID
    """
    tasks = read_all_tasks()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskWithID)
def get_task(task_id: int):
    """Get a task by ID

    Args:
        task_id (int): An integer representing a Task ID.
    """
    task = read_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task

#CREATE operations
@app.post("/task", response_model=TaskWithID)
def add_task(task: Task):
    return create_task(task)

# UPDATE operations

class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

@app.put("/task/{task_id}", response_model=TaskWithID)
def update_task(task_id: int, task_update: UpdateTask):
    modified = modify_task(task_id, task_update.model_dump(exclude_unset=True))
    if not modified:
        raise HTTPException(status_code=404, detail="Task not found")
    return modified

# DELETE operations

@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id: int):
    removed_task = remove_task(task_id)
    if not remove_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return removed_task
    

