
from crm import contacts
import os

def test_add_contact(tmp_path):
    contacts.DATA_FILE = tmp_path / "contacts.json"
    contacts.save_contacts([])
    contacts.add(name="Test User", email="test@example.com", phone="123")
    loaded = contacts.load_contacts()
    assert len(loaded) == 1
    assert loaded[0]["name"] == "Test User"
