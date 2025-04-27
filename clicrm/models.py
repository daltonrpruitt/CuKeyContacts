from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


def current_time() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class Person:
    id: str = field(default_factory=generate_uuid)
    name: str = field(default="")
    preferred_name: Optional[str] = None
    primary_email: Optional[str] = None
    other_emails: List[str] = field(default_factory=list)
    primary_phone: Optional[str] = None
    other_phones: List[str] = field(default_factory=list)
    associated_organizations: List[str] = field(default_factory=list)  # list of UUIDs
    primary_address: Optional[str] = None
    date_added: str = field(default_factory=current_time)
    last_contacted: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Person":
        return Person(**data)


@dataclass
class Business:
    id: str = field(default_factory=generate_uuid)
    name: str = field(default="")
    primary_email: Optional[str] = None
    other_emails: List[str] = field(default_factory=list)
    primary_phone: Optional[str] = None
    other_phones: List[str] = field(default_factory=list)
    associated_people: List[str] = field(default_factory=list)  # list of UUIDs
    primary_address: Optional[str] = None
    website: Optional[str] = None
    date_added: str = field(default_factory=current_time)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Business":
        return Business(**data)
