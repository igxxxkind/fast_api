import csv

from typing import Optional
from models import Task, TaskWithID

DATABASE_FILENAME = "tasks.csv"

column_fields = ["id", "title", "description", "status"]
### Read operations
def read_all_tasks() -> list[TaskWithID]:
    with open(DATABASE_FILENAME, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        return [TaskWithID(**row) for row in reader]
    
def read_task(task_id) -> Optional[TaskWithID]:
    with open(DATABASE_FILENAME, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row["id"]) == task_id:
                return TaskWithID(**row)
            
# Create operations
# write a set of functions that facilitate the creation of tasks
def get_next_id():
    """Get the next available ID for each new task available.

    Returns:
        _type_: Integer
    """
    try:
        with open(DATABASE_FILENAME, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            max_id = max(int(row["id"]) for row in reader)
            return max_id + 1
    except (FileNotFoundError, ValueError):
        return 1
    
def write_task_into_csv(task: TaskWithID):
    """Write a task into the CSV file.

    Args:
        task (TaskWithID): The task to write.
    """
    with open(DATABASE_FILENAME, "a", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=column_fields)
        writer.writerow(task.model_dump())
        
def create_task(task: Task) -> TaskWithID:
    id = get_next_id()
    task_with_id = TaskWithID(id=id, **task.model_dump())
    write_task_into_csv(task_with_id)
    return task_with_id

# Update operations

def modify_task(id: int, task: dict) -> Optional[TaskWithID]:
    updated_task: Optional[TaskWithID] = None
    tasks = read_all_tasks()
    for number, task_ in enumerate(tasks):
        if task_.id == id:
            tasks[number] = (
                updated_task
                ) = task_.model_copy(update=task)
    with open(DATABASE_FILENAME, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task_.model_dump())
    if updated_task:
        return updated_task
    
# Delete Operations

def remove_task(id: int) -> bool:
    deleted_task: Optional[Task] = None
    tasks = read_all_tasks()
    with open(DATABASE_FILENAME, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_fields)
        writer.writeheader()
        for task in tasks:
            if task.id == id:
                deleted_task = task
                continue
            writer.writerow(task.model_dump())
    if deleted_task:
        dict_task_without_id = (deleted_task.model_dump())
        del dict_task_without_id["id"]
        return Task(**dict_task_without_id)
    
# HEre we have the BASIC CRUD operations implemented.

# API structure us fundamentall in RESTful APi design. IT requires definijng an endpoint and associate that with an HTTP method.
