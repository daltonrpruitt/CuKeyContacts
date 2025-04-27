import typer
from typing import Optional
from models import Person, Business
from storage import load_people, save_people, load_businesses, save_businesses
from utils import print_table, find_by_name_regex, export_csv
import uuid

app = typer.Typer()


@app.command()
def add_person(
    name: str,
    preferred_name: Optional[str] = None,
    primary_email: Optional[str] = None,
    primary_phone: Optional[str] = None,
    primary_address: Optional[str] = None,
):
    people = load_people()
    new_person = Person(
        name=name,
        preferred_name=preferred_name,
        primary_email=primary_email,
        primary_phone=primary_phone,
        primary_address=primary_address,
    )
    people.append(new_person)
    save_people(people)
    typer.echo(f"Added person {name}.")


@app.command()
def list_people(output: str = "table"):
    people = load_people()
    if output == "table":
        print_table(people, fields=["id", "name", "primary_email", "primary_phone"])
    elif output == "json":
        import json
        typer.echo(json.dumps([p.to_dict() for p in people], indent=2))
    elif output == "csv":
        export_csv(people, fields=["id", "name", "primary_email", "primary_phone"], filename="people_export.csv")


@app.command()
def search_people(query: str, output: str = "table"):
    people = load_people()
    matches = find_by_name_regex(people, "name", query)
    if output == "table":
        print_table(matches, fields=["id", "name", "primary_email", "primary_phone"])
    elif output == "json":
        import json
        typer.echo(json.dumps([p.to_dict() for p in matches], indent=2))
    elif output == "csv":
        export_csv(matches, fields=["id", "name", "primary_email", "primary_phone"], filename="people_search.csv")


@app.command()
def delete_person(person_id: str):
    people = load_people()
    people = [p for p in people if p.id != person_id]
    save_people(people)
    typer.echo(f"Deleted person with ID {person_id}.")


if __name__ == "__main__":
    app()
