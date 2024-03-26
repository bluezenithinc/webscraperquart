import pytest

from qrt import create_app


@pytest.fixture
def client():
    app = create_app("test")
    return app.test_client()
