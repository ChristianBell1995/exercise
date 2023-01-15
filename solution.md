# Solution
## Get started
Run `docker-compose up` to start the application.
To run the tests, execute `docker-compose exec web pytest .`

## POST Endpoint to create an Order
- To handle possible failed network requests or double requests from the client, an `idempotency_id` is added to the endpoint.
- The `limit_price` field is changed to `limit_price_cents` to handle any currency in integers instead of decimals/floats.
- When a request is received, the system checks the database for an existing order with the same `idempotency_id`. If one is found, the existing order is returned to the client.
- The order is created with a status of `PENDING` and the call to the 3rd party stock exchange service is made. This call is executed in `asyncio.to_thread` to prevent it from blocking the Python Global Interpreter.
- On successful execution, the order status is updated to `CREATED` and the order is returned to the client.
- On failure, the order status is updated to `FAILED` and an internal server error is thrown.
- The system assumes that the 3rd party stock exchange service has the capability to check the user's balance before placing the order.

## Tech stack used + future improvements
- The `databases` package is used to support async connections to the Postgres DB.
- The `db.py` file is used to create the orders table, but in the future, `alembic` can be used to handle database migrations.
fixtures are used to mock the responses from the `crud.py` file, but in the future, a test database can be set up to run the tests against.
- At the moment, the test cases do not check the `status` of each placed order, but this will be added once a test database is set up.
- The Enums `OrderStatus`, `OrderType`, and `OrderSide` are currently used at the pydantic layer. They can be moved to be Postgres enums in the future.
- The POST endpoint currently returns pydantic validation JSON for incorrect fields. This can be parsed into more helpful errors in the future.

## How would you change the system if we would receive a high volume of async updates to the orders placed through a socket connection on the stock exchange, e.g. execution information?

1. Implement a message queue or a pub/sub system to handle the async updates. This will ensure that the updates are processed in a reliable and efficient manner, without blocking the main application.
2. Create a separate service or worker process that is responsible for consuming updates from the message queue and updating the order status in the database.
3. If you have a high volume of reads and writes then at scale it may be worth looking at Multi version concurrency control where reading locks never block writing locks and vice-versa (https://www.postgresql.org/docs/7.1/mvcc.html).
