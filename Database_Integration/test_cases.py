import pytest
from Mini_Project_3 import TaskManager


# -------------------------
# FIXTURE
# -------------------------
@pytest.fixture
def tm():
    """Create a fresh TaskManager with in-memory DB for each test"""
    manager = TaskManager(db=":memory:")
    yield manager
    manager.close()


# -------------------------
# CREATE
# -------------------------
def test_create_task(tm):
    task_id = tm.create("Test Task", "Test Desc", "high", "2026-02-10")
    task = tm.read_one(task_id)

    assert task is not None
    assert task[1] == "Test Task"
    assert task[2] == "Test Desc"
    assert task[3] == "high"
    assert task[4] == "2026-02-10"
    assert task[5] == "pending"


# -------------------------
# READ
# -------------------------
def test_read_all_tasks(tm):
    tm.create("Task 1")
    tm.create("Task 2")

    tasks = tm.read_all()
    assert len(tasks) == 2


def test_read_single_task(tm):
    task_id = tm.create("Single Task")
    task = tm.read_one(task_id)

    assert task[0] == task_id
    assert task[1] == "Single Task"


def test_read_nonexistent_task(tm):
    task = tm.read_one(999)
    assert task is None


# -------------------------
# UPDATE
# -------------------------
def test_update_task(tm):
    task_id = tm.create("Old Title")
    tm.update(task_id, title="New Title", priority="low")

    task = tm.read_one(task_id)
    assert task[1] == "New Title"
    assert task[3] == "low"


def test_mark_task_completed(tm):
    task_id = tm.create("Complete Me")
    tm.update(task_id, status="completed")

    task = tm.read_one(task_id)
    assert task[5] == "completed"


# -------------------------
# DELETE
# -------------------------
def test_delete_task(tm):
    task_id = tm.create("Delete Me")
    tm.delete(task_id)

    task = tm.read_one(task_id)
    assert task is None


# -------------------------
# STATS
# -------------------------
def test_stats_empty(tm):
    stats = tm.stats()

    assert stats["total"] == 0
    assert stats["completed"] == 0
    assert stats["pending"] == 0
    assert stats["rate"] == 0


def test_stats_with_tasks(tm):
    t1 = tm.create("Task 1")
    t2 = tm.create("Task 2")
    tm.update(t1, status="completed")

    stats = tm.stats()

    assert stats["total"] == 2
    assert stats["completed"] == 1
    assert stats["pending"] == 1
    assert stats["rate"] == 50.0
