import pytest

# types
from quart.testing import QuartClient


@pytest.mark.asyncio
async def test_cors(client: QuartClient):
    response = await client.get("/", headers={"Origin": "https://google.com"})
    assert "Access-Control-Allow-Origin" in response.headers
