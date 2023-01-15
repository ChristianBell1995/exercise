from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.api.models import CreateOrderModel, Order
from app.api.stock_exchange import OrderPlacementError
from app.main import app


@pytest_asyncio.fixture
async def async_app_client():
    async with AsyncClient(app=app, base_url="http://test") as async_app_client:
        yield async_app_client


@pytest.fixture
def request_body():
    return {
        "idempotency_id": "12332229-e6b6-4479-aff4-f180236955be",
        "side": "buy",
        "instrument": "US19260Q1076",
        "quantity": 1,
    }


@pytest.fixture
def limit_request_body(request_body):
    return {
        **request_body,
        "type": "limit",
        "limit_price_cents": 100,
    }


@pytest.fixture
def market_request_body(request_body):
    return {
        **request_body,
        "type": "market",
    }


@pytest.fixture
def limit_order(limit_request_body):
    return {
        "id": str(uuid4()),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        **limit_request_body,
    }


@pytest.fixture
def market_order(market_request_body):
    return {
        "id": str(uuid4()),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        **market_request_body,
        "limit_price_cents": None,
    }


@pytest.fixture
def error_message():
    return {"detail": "Internal server error while placing the order"}


@pytest.fixture
def patch_crud_create_success_market_order(market_order, monkeypatch):
    async def mock_create(model: CreateOrderModel):
        return market_order

    monkeypatch.setattr("app.api.crud.create", mock_create)


@pytest.fixture
def patch_crud_create_success_limit_order(limit_order, monkeypatch):
    async def mock_create(model: CreateOrderModel):
        return limit_order

    monkeypatch.setattr("app.api.crud.create", mock_create)


@pytest.fixture
def patch_crud_get_none(monkeypatch):
    async def mock_get(idempotency_id: str):
        return None

    monkeypatch.setattr("app.api.crud.get", mock_get)


@pytest.fixture
def patch_crud_get_success_market_order(market_order, monkeypatch):
    async def mock_get(idempotency_id: str):
        return market_order

    monkeypatch.setattr("app.api.crud.get", mock_get)


@pytest.fixture
def patch_crud_update_success(monkeypatch):
    async def mock_update(order: Order, status: str):
        return order

    monkeypatch.setattr("app.api.crud.update", mock_update)


@pytest.fixture
def patch_stock_exchange_place_order_error(monkeypatch):
    class MockOrderPlacementError:
        def __init__(self, *args, **kwargs):
            raise OrderPlacementError(
                "Failed to place order at stock exchange. Connection not available"
            )

    monkeypatch.setattr("app.api.stock_exchange.place_order", MockOrderPlacementError)
