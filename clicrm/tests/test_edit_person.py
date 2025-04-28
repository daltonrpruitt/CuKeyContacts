# tests/test_edit_person.py

import pytest
import json
import os
from uuid import uuid4
from datetime import datetime
from models import Person
from storage import save_people, load_people
from cli import edit_person

@pytest.fixture
def temp_people_file(tmp_path):
    """Fixture to create a temporary people.json for testing."""
    people = [
        Person(
            id=str(uuid4()),
            name="John Doe",
            preferred_name="Johnny",
            primary_email="john@example.com",
            other_emails=[],
            primary_phone="123-4567",
            other_phones=[],
            associated_organizations=[],
            primary_address="123 Main St",
            created_at=str(datetime.now()),
            last_contacted=None
        )
    ]
    filepath = tmp_path / "people.json"
    save_people(people, filepath=filepath)
    return filepath, people

def test_edit_person_primary_email(monkeypatch, temp_people_file):
    """Test editing the primary email of a person."""
    filepath, people = temp_people_file
    person_id = str(people[0].id)

    # Patch load_people and save_people to use our temp file
    monkeypatch.setattr("storage.load_people", lambda: load_people(filepath=filepath))
    monkeypatch.setattr("storage.save_people", lambda data: save_people(data,filepath=filepath))

    # Edit primary email
    new_email = "new_email@example.com"
    edit_person(
        id=person_id,
        name=None,
        primary_email=new_email,
        preferred_name=None,
        other_emails=None,
        primary_phone=None,
        other_phones=None,
        primary_address=None,
        associated_organizations=None,
        last_contacted=None,
        overwrite_lists=False,
        filepath=filepath
    )

    updated_people = load_people(filepath=filepath)
    updated_person = updated_people[0]

    assert updated_person.primary_email == new_email, "Primary email was not updated correctly."

def test_edit_person_add_other_phone(monkeypatch, temp_people_file):
    """Test appending a new phone number to other_phones."""
    filepath, people = temp_people_file
    person_id = str(people[0].id)

    monkeypatch.setattr("storage.load_people", lambda: load_people(filepath=filepath))
    monkeypatch.setattr("storage.save_people", lambda data: save_people(data, filepath=filepath))

    # Add other phone numbers
    new_phones = ["555-1234", "555-5678"]
    edit_person(
        id=person_id,
        name=None,
        primary_email=None,
        preferred_name=None,
        other_emails=None,
        primary_phone=None,
        other_phones=new_phones,
        primary_address=None,
        associated_organizations=None,
        last_contacted=None,
        overwrite_lists=False,
        filepath=filepath
    )

    updated_people = load_people(filepath=filepath)
    updated_person = updated_people[0]

    assert all(phone in updated_person.other_phones for phone in new_phones), "Other phones were not appended correctly."

