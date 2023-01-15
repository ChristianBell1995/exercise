import json

import pytest


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "patch_crud_create_success_limit_order",
    "patch_crud_get_none",
    "patch_crud_update_success",
)
async def test_create_order_success_limit_order(
    async_app_client, limit_request_body, limit_order
):
    response = await async_app_client.post(
        "/orders/", content=json.dumps(limit_request_body)
    )

    assert response.status_code == 201
    assert response.json() == limit_order


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "patch_crud_create_success_market_order",
    "patch_crud_get_none",
    "patch_crud_update_success",
)
async def test_create_order_success_market_order(
    async_app_client, market_request_body, market_order
):
    response = await async_app_client.post(
        "/orders/", content=json.dumps(market_request_body)
    )

    assert response.status_code == 201
    assert response.json() == market_order


@pytest.mark.asyncio
@pytest.mark.usefixtures("patch_crud_get_success_market_order")
async def test_create_order_where_order_where_idempotency_key_exists(
    async_app_client, market_request_body, market_order
):
    response = await async_app_client.post(
        "/orders/",
        content=json.dumps(market_request_body),
    )

    assert response.status_code == 201
    assert response.json() == market_order


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "patch_crud_create_success_market_order",
    "patch_crud_get_none",
    "patch_stock_exchange_place_order_error",
    "patch_crud_update_success",
)
async def test_create_order_where_order_where_stock_exchange_errors(
    async_app_client, market_request_body, error_message
):
    response = await async_app_client.post(
        "/orders/",
        content=json.dumps(market_request_body),
    )

    assert response.status_code == 500
    assert response.json() == error_message


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "patch_crud_create_success_market_order",
    "patch_crud_get_none",
    "patch_crud_update_success",
)
async def test_create_order_invalid_combination_of_type_market_and_limit_price(
    async_app_client, market_request_body
):
    market_request_body["limit_price_cents"] = 100

    response = await async_app_client.post(
        "/orders/",
        content=json.dumps(market_request_body),
    )

    assert response.status_code == 422


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "patch_crud_create_success_limit_order",
    "patch_crud_get_none",
    "patch_crud_update_success",
)
async def test_create_invalid_order_no_limit_price_with_type_limit(
    async_app_client, limit_request_body
):
    del limit_request_body["limit_price_cents"]
    response = await async_app_client.post(
        "/orders/",
        content=json.dumps(limit_request_body),
    )
    assert response.status_code == 422
