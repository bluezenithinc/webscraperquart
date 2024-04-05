import pytest

# types
from quart.testing import QuartClient


@pytest.mark.asyncio
async def test_session(client: QuartClient):
    response = await client.get("/")
    assert "session=" in response.headers["Set-Cookie"]
