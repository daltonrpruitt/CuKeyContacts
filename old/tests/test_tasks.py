
from crm import tasks
import os

def test_add_task(tmp_path):
    tasks.DATA_FILE = tmp_path / "tasks.json"
    tasks.save_tasks([])
    tasks.add(title="Follow up with client", due="2025-05-01")
    loaded = tasks.load_tasks()
    assert len(loaded) == 1
    assert loaded[0]["title"] == "Follow up with client"
