import csv
import os
from pathlib import Path
from unittest.mock import patch

import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

TEST_DATABASE_FILE = "test_tasks.csv"
TEST_TASKS_CSV = [
    {
        "id": 1,
        "title": "Test Task 1",
        "description": "Test Description 1",
        "status": "Incomplete"
    },
    {
        "id": 2,
        "title": "Test Task 2",
        "description": "Test Description 2",
        "status": "Ongoing"
    }
]

TEST_TASKS = [
    {**task_json, "id": int(task_json["id"])} for task_json in TEST_TASKS_CSV
    ]

# Defining fixtures for testing the Task Manager API.


@pytest.fixture(autouse=True)
def create_test_database():
    database_file_location = str(Path(__file__).parent / TEST_DATABASE_FILE)
    
    with patch("task_manager_app.operations.DATABASE_FILENAME", database_file_location) as csv_test:
        with open(database_file_location, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["id", "title", "description", "status"])
            writer.writeheader()
            writer.writerows(TEST_TASKS_CSV)
            print("")
        yield csv_test
    os.remove(database_file_location)
    