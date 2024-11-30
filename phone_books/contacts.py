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
    *,
    name: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    conn: AsyncConnection,
) -> list[Contact]:
    sql = """
    SELECT
        id, name, phone, email
    FROM
        contacts
    WHERE
        ($1 = '' OR name ILIKE '%' || $1 || '%')
        AND ($2 = '' OR phone = $2)
        AND ($3 = '' OR email = $3)
"""
    params = (name or "", phone or "", email or "")
    result = await conn.execute(sql, params)
    contacts = await result.fetchall()
    return [
        Contact(id=contact[0], name=contact[1], phone=contact[2], email=contact[3])
        for contact in contacts
    ]


async def get_contact_by_id(contact_id: str, conn: AsyncConnection) -> Contact | None:
    sql = """
    SELECT
        id, name, phone, email
    FROM
        contacts
    WHERE
        id = $1
"""
    params = (contact_id,)
    result = await conn.execute(sql, params)
    contact = await result.fetchone()
    if not contact:
        return None
    return Contact(id=contact[0], name=contact[1], phone=contact[2], email=contact[3])


async def update_contact(
    contact_id: str, contact: UpdateContact, conn: AsyncConnection
) -> Contact:
    sql = """
    UPDATE
        contacts
    SET
        name = COALESCE($1, name),
        phone = COALESCE($2, phone),
        email = COALESCE($3, email)
    WHERE
        id = $4
    RETURNING
        id, name, phone, email
"""
    params = (
        contact.get("name"),
        contact.get("phone"),
        contact.get("email"),
        contact_id,
    )
    result = await conn.execute(sql, params)
    updated_contact = await result.fetchone()
    return Contact(
        id=updated_contact[0],
        name=updated_contact[1],
        phone=updated_contact[2],
        email=updated_contact[3],
    )


async def delete_contact(contact_id: str, conn: AsyncConnection) -> bool:
    sql = """
    DELETE FROM
        contacts
    WHERE
        id = $1
    RETURNING
        id
    """
    params = (contact_id,)
    is_deleted = False
    result = await conn.execute(sql, params)
    deleted_id = await result.fetchone()
    if deleted_id:
        is_deleted = True
    return is_deleted
