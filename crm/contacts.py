
import typer
import json
from datetime import datetime
from pathlib import Path

app = typer.Typer()
DATA_FILE = Path("data/contacts.json")

def load_contacts():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_contacts(contacts):
    DATA_FILE.parent.mkdir(exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=2)

@app.command()
def add(name: str, email: str = "", phone: str = ""):
    contacts = load_contacts()
    contact_id = (max([c["id"] for c in contacts]) + 1) if contacts else 1
    new_contact = {
        "id": contact_id,
        "name": name,
        "email": email,
        "phone": phone,
        "created_at": datetime.now().isoformat()
    }
    contacts.append(new_contact)
    save_contacts(contacts)
    typer.echo(f"Contact added with ID: {contact_id}")

@app.command()
def list():
    contacts = load_contacts()
    for c in contacts:
        typer.echo(f"{c['id']}: {c['name']} - {c['email']} - {c['phone']}")
