import typer
from typing import Optional
from typing_extensions import Annotated
from models import Person, Business
from storage import load_people, save_people, load_businesses, save_businesses
from utils import print_table, find_by_name_regex, export_csv
from dataclasses import fields
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
def list_people(output: str = "table",
                long: Annotated[bool, typer.Option("--long", "-l")] = False,
                custom_fields: Annotated[str, typer.Option("--fields", "-F")] = None):
    """List the current people in the database.

    Args:
            output (str, optional): How to output the data; either "table" (stdout), "json" (file), or "csv" (file). Defaults to "table".
            "--long", "-l" (Annotated[bool, typer.Option, optional): Output all available fields. Defaults to False.
            "--fields", "-F" (Annotated[str, typer.Option, optional): Given a comma-separated string of fields, output the data with those fields. Defaults to None.
    """
    output_fields = ["name", "primary_email", "primary_phone", "associated_businesses", "created_at"]
    if long:
      output_fields = [field.name for field in fields(Person)]
    elif custom_fields:
        try:
            output_fields = custom_fields.split(",")
            all_fields = [field.name for field in fields(Person)]
            valid = True
            for f in output_fields:
                if f not in all_fields:
                    print(f"'{f}' is not a valid field!")
                    valid = False
            if not valid:
                print("Available fields are:")
                for i, field in enumerate(all_fields):
                    print(f"{field}", end="")
                    end_c = ""
                    if (i+1) % 4 == 0:
                        end_c = "\n"
                    if i+1 < len(all_fields):
                        print(", ", end=end_c)
                    else:
                        print("")
                raise ValueError("Invalid custom fields!")
        except Exception as e:
            print(f"Error: {e}")
            raise e

    people = load_people()
    if output == "table":
        print_table(people, fields=output_fields)
    elif output == "json":
        import json
        typer.echo(json.dumps([p.to_dict() for p in people], indent=2))
    elif output == "csv":
        export_csv(people, fields=output_fields, filename="people_export.csv")


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
