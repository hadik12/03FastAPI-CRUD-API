import os
import tempfile
import uuid
from pathlib import Path
from importlib import reload

import pytest
from httpx import ASGITransport, AsyncClient

os.environ["API_KEY"] = "test-key"

# уникальная БД на каждый запуск тестов (не конфликтует и не залипает)
TEST_DB_PATH = Path(tempfile.gettempdir()) / f"test_items_{uuid.uuid4().hex}.db"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.as_posix()}"

# reload модулей после выставления env
import src.settings as settings_module
reload(settings_module)
import src.db as db_module
reload(db_module)
import main
reload(main)

Base = db_module.Base
engine = db_module.engine
app = main.app

HEADERS = {"X-API-Key": os.environ["API_KEY"]}


def reset_database() -> None:
    # важно на Windows: закрыть пул соединений перед удалением файла
    try:
        engine.dispose()
    except Exception:
        pass

    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink(missing_ok=True)

    Base.metadata.create_all(bind=engine)


@pytest.fixture(autouse=True)
def _clean_db():
    reset_database()
    yield
    try:
        engine.dispose()
    except Exception:
        pass
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink(missing_ok=True)


@pytest.fixture
async def client():
    # совместимость с разными версиями httpx
    try:
        transport = ASGITransport(app=app, lifespan="on")
    except TypeError:
        transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        yield async_client


@pytest.mark.anyio
async def test_create_item(client: AsyncClient):
    payload = {"name": "Test Item", "description": "A test description", "price": 12.5, "in_stock": True}
    response = await client.post("/items", json=payload, headers=HEADERS)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]


@pytest.mark.anyio
async def test_list_items_contains_created(client: AsyncClient):
    payload = {"name": "List Item", "description": "For listing", "price": 25.0, "in_stock": True}
    create_response = await client.post("/items", json=payload, headers=HEADERS)
    assert create_response.status_code == 201

    list_response = await client.get("/items", headers=HEADERS)
    assert list_response.status_code == 200
    data = list_response.json()
    assert any(item["name"] == payload["name"] for item in data)
