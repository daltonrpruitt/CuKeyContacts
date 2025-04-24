
import typer
from crm import contacts, tasks

app = typer.Typer()
app.add_typer(contacts.app, name="contacts")
app.add_typer(tasks.app, name="tasks")

if __name__ == "__main__":
    app()
