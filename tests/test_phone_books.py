import pytest
import asyncio
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


async def test_given_a_new_contact_when_created_then_it_is_returned():
    # given
    contact = {"name": "John Doe", "phone": "1234567890", "email": "john@emil.com"}
    # when
    result = await sut.create_contact(contact)
    # then
    assert result["email"] == contact["email"]
    assert result["name"] == contact["name"]
    assert result["phone"] == contact["phone"]
    assert "id" in result

async def test_given_no_contacts_when_get_all_contacts_then_return_empty_list():
    # when
    result = await sut.get_all_contacts()
    # then
    assert result == []

async def test_given_contacts_when_get_all_contacts_then_return_all_contacts():
    # given
    contact1 = {"name": "John Doe", "phone": "1234567890", "email": "john@email.com"}
    contact2 = {"name": "John Guon", "phone": "1234567890", "email": "john@email.com"}
    contact3 = {"name": "John Xuon", "phone": "1234567890", "email": "john@email.com"}
    await sut.create_contact(contact1)
    await sut.create_contact(contact2)
    await sut.create_contact(contact3)
    # when
    result = await sut.get_all_contacts()
    # then
    assert len(result) == 3

@pytest.mark.parametrize(("name", "expected_count"), [("John", 2), ("Julio", 1), ("Guon", 3)])
async def test_given_contacts_when_get_all_contacts_with_name_then_return_contacts_with_name(name: str, expected_count: int):
    # given
    contact1 = {"name": "John Doe", "phone": "1234567890", "email": "john@email.com"}
    contact2 = {"name": "John Guon", "phone": "1234567890", "email": "john@email.com"}
    contact3 = {"name": "Maria Doe", "phone": "1234567890", "email": "john@email.com"}
    contact4 = {"name": "Maria Guon", "phone": "1234567890", "email": "john@email.com"}
    contact5 = {"name": "Julio Guon", "phone": "1234567890", "email": "john@email.com"}
    await sut.create_contact(contact1)
    await sut.create_contact(contact2)
    await sut.create_contact(contact3)
    await sut.create_contact(contact4)
    await sut.create_contact(contact5)
    # when
    result = await sut.get_all_contacts(name=name)
    # then
    assert len(result) == expected_count
