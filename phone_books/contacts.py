from typing import TypedDict


class Contact(TypedDict):
    id: str
    name: str
    phone: str
    email: str


class CreateContact(TypedDict):
    name: str
    phone: str
    email: str


class UpdateContact(TypedDict):
    name: str | None
    phone: str | None
    email: str | None


async def create_contact(contact: CreateContact) -> Contact:
    pass

async def get_all_contacts(
    *, name: str | None = None, phone: str | None = None, email: str | None = None
) -> list[Contact]:
    pass

async def get_contact_by_id(contact_id: str) -> Contact:
    pass

async def update_contact(contact_id: str, contact: UpdateContact) -> Contact:
    pass

async def delete_contact(contact_id: str) -> bool:
    pass
