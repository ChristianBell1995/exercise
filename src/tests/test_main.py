import json

import pytest


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "patch_crud_create_success", "patch_crud_get_none", "patch_crud_update_success"
)
async def test_create_order_success(async_app_client, request_body, order):
    response = await async_app_client.post("/orders/", content=json.dumps(request_body))

    assert response.status_code == 201
    assert response.json() == order


@pytest.mark.asyncio
@pytest.mark.usefixtures("patch_crud_get_success")
async def test_create_order_where_order_where_idempotency_key_exists(
    async_app_client, request_body, order
):
    response = await async_app_client.post(
        "/orders/",
        content=json.dumps(request_body),
    )

    assert response.status_code == 201
    assert response.json() == order


@pytest.mark.asyncio
async def test_create_order_invalid_body(async_app_client):
    response = await async_app_client.post(
        "/orders/", content=json.dumps({"title": "something"})
    )

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "patch_crud_create_success",
    "patch_crud_get_none",
    "patch_stock_exchange_place_order_error",
    "patch_crud_update_success",
)
async def test_create_order_where_order_where_stock_exchange_errors(
    async_app_client, request_body, error_message
):
    response = await async_app_client.post(
        "/orders/",
        content=json.dumps(request_body),
    )

    assert response.status_code == 500
    assert response.json() == error_message
