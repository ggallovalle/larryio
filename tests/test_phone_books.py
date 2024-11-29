import asyncio

import pytest
from psycopg import AsyncConnection

import phone_books.contacts as sut


@pytest.mark.asyncio
async def test_async_works():
    await asyncio.sleep(0.1)
    assert True


class TestAsyncWorks:
    @pytest.mark.asyncio
    async def test_it_works(self):
        await asyncio.sleep(0.1)
        assert True


@pytest.mark.asyncio
async def test_db_connection_works(pg_conn: AsyncConnection):
    assert pg_conn is not None
    name = "John Doe"
    result = await pg_conn.execute(
        "INSERT INTO contacts (name, phone) VALUES ($1, $2) RETURNING id, name",
        (name, "1234567890"),
    )
    contact = await result.fetchone()
    assert contact[0]
    assert contact[1] == name


@pytest.mark.asyncio
async def test_given_a_new_contact_when_created_then_it_is_returned(pg_conn: AsyncConnection):
    # given
    contact = {"name": "John Doe", "phone": "1234567890", "email": "john@emil.com"}
    # when
    result = await sut.create_contact(contact, pg_conn)
    # then
    assert result["email"] == contact["email"]
    assert result["name"] == contact["name"]
    assert result["phone"] == contact["phone"]
    assert "id" in result


@pytest.mark.asyncio
async def test_given_no_contacts_when_get_all_contacts_then_return_empty_list(pg_conn: AsyncConnection):
    # when
    result = await sut.get_all_contacts(conn=pg_conn)
    # then
    assert result == []


@pytest.mark.asyncio
async def test_given_contacts_when_get_all_contacts_then_return_all_contacts(pg_conn: AsyncConnection):
    # given
    contact1 = {"name": "John Doe", "phone": "1234567890", "email": "john@email.com"}
    contact2 = {"name": "John Guon", "phone": "1234567890", "email": "john@email.com"}
    contact3 = {"name": "John Xuon", "phone": "1234567890", "email": "john@email.com"}
    await sut.create_contact(contact1, pg_conn)
    await sut.create_contact(contact2, pg_conn)
    await sut.create_contact(contact3, pg_conn)
    # when
    result = await sut.get_all_contacts(conn=pg_conn)
    # then
    assert len(result) == 3


@pytest.mark.parametrize(
    ("name", "expected_count"), [("John", 2), ("Julio", 1), ("Guon", 3)]
)
@pytest.mark.asyncio
async def test_given_contacts_when_get_all_contacts_with_name_then_return_contacts_with_name(
    name: str, expected_count: int, pg_conn: AsyncConnection
):
    # given
    contact1 = {"name": "John Doe", "phone": "1234567890", "email": "john@email.com"}
    contact2 = {"name": "John Guon", "phone": "1234567890", "email": "john@email.com"}
    contact3 = {"name": "Maria Doe", "phone": "1234567890", "email": "john@email.com"}
    contact4 = {"name": "Maria Guon", "phone": "1234567890", "email": "john@email.com"}
    contact5 = {"name": "Julio Guon", "phone": "1234567890", "email": "john@email.com"}
    await sut.create_contact(contact1, pg_conn)
    await sut.create_contact(contact2, pg_conn)
    await sut.create_contact(contact3, pg_conn)
    await sut.create_contact(contact4, pg_conn)
    await sut.create_contact(contact5, pg_conn)
    # when
    result = await sut.get_all_contacts(name=name, conn=pg_conn)
    # then
    assert len(result) == expected_count


@pytest.mark.asyncio
async def test_given_contacts_when_get_contact_by_id_then_return_contact(pg_conn: AsyncConnection):
    # given
    contact = {"name": "John Doe", "phone": "1234567890", "email": "john@email.com"}
    created = await sut.create_contact(contact, pg_conn)
    # when
    result = await sut.get_contact_by_id(created["id"], pg_conn)
    # then
    result == created


@pytest.mark.asyncio
async def test_given_contacts_when_update_contact_then_return_updated_contact(pg_conn: AsyncConnection):
    # given
    contact = {"name": "John Doe", "phone": "1234567890", "email": "john@email.com"}
    created = await sut.create_contact(contact, pg_conn)
    # when
    updated = await sut.update_contact(created["id"], {"name": "John Smith"})
    reference = await sut.get_contact_by_id(created["id"], pg_conn)
    # then
    assert updated["name"] == "John Smith"
    assert updated["name"] == reference["name"]


@pytest.mark.asyncio
async def test_given_contacts_when_delete_contact_only_deletes_one(pg_conn: AsyncConnection):
    # given
    contact1 = {"name": "John Doe", "phone": "1234567890", "email": "john@email.com"}
    contact2 = {"name": "John Guon", "phone": "1234567890", "email": "john@email.com"}
    contact3 = {"name": "Maria Doe", "phone": "1234567890", "email": "john@email.com"}
    contact4 = {"name": "Maria Guon", "phone": "1234567890", "email": "john@email.com"}
    contact5 = {"name": "Julio Guon", "phone": "1234567890", "email": "john@email.com"}
    ref1 = await sut.create_contact(contact1, pg_conn)
    await sut.create_contact(contact2, pg_conn)
    await sut.create_contact(contact3, pg_conn)
    await sut.create_contact(contact4, pg_conn)
    await sut.create_contact(contact5, pg_conn)
    # when
    deleted = await sut.delete_contact(ref1["id"])
    all_contacts = await sut.get_all_contacts(conn=pg_conn)

    # then
    assert deleted
    assert len(all_contacts) == 4
