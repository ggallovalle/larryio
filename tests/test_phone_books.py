import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_works():
    await asyncio.sleep(0.1)
    assert True

class TestAsyncWorks:

    @pytest.mark.asyncio
    async def test_it_works(self):
        await asyncio.sleep(0.1)
        assert True