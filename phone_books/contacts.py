from typing import TypedDict
from psycopg import AsyncConnection


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


async def create_contact(contact: CreateContact, conn: AsyncConnection) -> Contact:
    sql = """
    INSERT INTO contacts 
        (name, phone, email)
    VALUES
        ($1, $2, $3)
    RETURNING
        id
"""
    params = (contact["name"], contact["phone"], contact["email"])
    result = await conn.execute(sql, params)
    contact_id = await result.fetchone()
    return Contact(id=contact_id[0], **contact)



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
