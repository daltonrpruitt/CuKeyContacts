
import typer
import json
from datetime import datetime
from pathlib import Path

app = typer.Typer()
DATA_FILE = Path("data/tasks.json")

def load_tasks():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@app.command()
def add(title: str, due: str = ""):
    tasks = load_tasks()
    task_id = (max([t["id"] for t in tasks]) + 1) if tasks else 1
    new_task = {
        "id": task_id,
        "title": title,
        "due": due,
        "created_at": datetime.now().isoformat(),
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    typer.echo(f"Task added with ID: {task_id}")

@app.command()
def list():
    tasks = load_tasks()
    for t in tasks:
        status = "Done" if t["completed"] else "Pending"
        typer.echo(f"{t['id']}: {t['title']} - Due: {t['due']} - {status}")
