import typer
from typing import Optional
from typing_extensions import Annotated, List
from models import Person, Business
from storage import load_people, save_people, load_businesses, save_businesses, PEOPLE
from utils import find_by_id, print_table, filter_by_regex, export_csv
from dataclasses import fields
from datetime import datetime

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
    output_fields = ["name", "primary_email", "primary_phone",
                     "associated_organizations", "created_at"]
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
            raise typer.Exit(code=1)

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
    matches = filter_by_regex(people, "name", query)
    if output == "table":
        print_table(matches, fields=["id", "name",
                    "primary_email", "primary_phone"])
    elif output == "json":
        import json
        typer.echo(json.dumps([p.to_dict() for p in matches], indent=2))
    elif output == "csv":
        export_csv(matches, fields=[
                   "id", "name", "primary_email", "primary_phone"], filename="people_search.csv")

@app.command()
def edit_person(
    id: Optional[str] = typer.Option(None, help="UUID of the person to edit"),
    name: Optional[str] = typer.Option(None, help="Regex pattern to match the person's name"),
    preferred_name: Optional[str] = typer.Option(None),
    primary_email: Optional[str] = typer.Option(None),
    other_emails: Optional[List[str]] = typer.Option(None),
    primary_phone: Optional[str] = typer.Option(None),
    other_phones: Optional[List[str]] = typer.Option(None),
    primary_address: Optional[str] = typer.Option(None),
    associated_organizations: Optional[List[str]] = typer.Option(None),
    last_contacted: Optional[str] = typer.Option(None, help="Format YYYY-MM-DD"),
    overwrite_lists: bool = typer.Option(False, help="Overwrite lists instead of appending"),
    filepath: str = PEOPLE_FILE
):
    """
    Edit (patch) a person entry by ID or name.
    """
    people = load_people(filepath=filepath)

    person = None

    if id:
        person = find_by_id(people, id)
        if person is None:
            typer.echo(f"Could not find person with id of '{id}'.")
            raise typer.Exit(code=1)
        
    elif name:
        matches = filter_by_regex(people, "name", name)
        if len(matches) == 0:
            typer.echo(f"No matches found for pattern '{name}'.")
            raise typer.Exit(code=1)
        elif len(matches) > 1:
            typer.echo("Multiple matches found. Please use --id to specify:\n")
            for p in matches:
                typer.echo(f"- {p.name} (id={p.id})")
            raise typer.Exit(code=1)
        else:
            person = matches[0]
    else:
        typer.echo("Please specify either --id or --name to identify the person.")
        raise typer.Exit(code=1)

    updated = False

    # Patch fields if provided
    if preferred_name is not None:
        person.preferred_name = preferred_name
        updated = True
    if primary_email is not None:
        person.primary_email = primary_email
        updated = True
    if primary_phone is not None:
        person.primary_phone = primary_phone
        updated = True
    if primary_address is not None:
        person.primary_address = primary_address
        updated = True
    if other_emails:
        if overwrite_lists:
            person.other_emails = other_emails
        else:
            person.other_emails.extend(other_emails)
        updated = True
    if other_phones:
        if overwrite_lists:
            person.other_phones = other_phones
        else:
            person.other_phones.extend(other_phones)
        updated = True
    if associated_organizations:
        if overwrite_lists:
            person.associated_organizations = associated_organizations
        else:
            person.associated_organizations.extend(associated_organizations)
        updated = True
    if last_contacted:
        try:
            person.last_contacted = datetime.strptime(last_contacted, "%Y-%m-%d")
        except ValueError:
            typer.echo("Invalid date format for last_contacted. Use YYYY-MM-DD.")
            raise typer.Exit(code=1)
        updated = True

    if updated:
        save_people(people, filepath=filepath)
        typer.echo(f"Person '{person.name}' updated successfully.")
    else:
        typer.echo("No changes provided.")



@app.command()
def delete_person(person_id: str):
    people = load_people()
    people = [p for p in people if p.id != person_id]
    save_people(people)
    typer.echo(f"Deleted person with ID {person_id}.")


if __name__ == "__main__":
    app()
