import json
import os
from typing import List
from models import Person, Business

PEOPLE_FILE = "data/people.json"
BUSINESSES_FILE = "data/businesses.json"


def ensure_file_exists(filepath: str):
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            json.dump([], f)


def load_people() -> List[Person]:
    ensure_file_exists(PEOPLE_FILE)
    with open(PEOPLE_FILE, "r") as f:
        data = json.load(f)
    return [Person.from_dict(item) for item in data]


def save_people(people: List[Person]):
    with open(PEOPLE_FILE, "w") as f:
        json.dump([person.to_dict() for person in people], f, indent=2)


def load_businesses() -> List[Business]:
    ensure_file_exists(BUSINESSES_FILE)
    with open(BUSINESSES_FILE, "r") as f:
        data = json.load(f)
    return [Business.from_dict(item) for item in data]


def save_businesses(businesses: List[Business]):
    with open(BUSINESSES_FILE, "w") as f:
        json.dump([business.to_dict() for business in businesses], f, indent=2)
