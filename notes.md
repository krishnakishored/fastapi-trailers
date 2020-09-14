## Basics

1. Unlike Django or Flask, FastAPI does not have a built-in development server. So, we'll use `Uvicorn`, an ASGI server, to serve up FastAPI
    - setting for Uvicorn:
        - command: `uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000`
        - `--reload` enables auto-reload so the server will restart after changes are made to the code base.
        - `--workers 1` provides a single worker process.
        - `--host 0.0.0.0` defines the address to host the server on.
        - `--port 8000` defines the port to host the server on.
        - `app.main:app` tells Uvicorn where it can find the FastAPI ASGI application 
           e.g., "within the 'app' module, you'll find the ASGI app, app = FastAPI(), in the 'main.py' file.

1. To Run the project _fastapi-crud_
    > $ docker-compose up -d --build
    > $ docker-comppose exec web pytest .

1. Async Handlers
    - Rather than having to go through the trouble of spinning up a task queue (like Celery or RQ) or utilizing threads, FastAPI makes it easy to deliver routes asynchronously. As long as you don't have any blocking I/O calls in the handler, you can simply declare the handler as asynchronous by adding the `async` keyword like so:

1. You can break up and modularize larger projects as well as apply versioning to your API with the `APIRouter`. If you're familiar with Flask, it is equivalent to a Blueprint.

1. SQLAlchemy `engine` - used for communicating with database. `Metadata` instance used for creating db schema. `databases` is an async SQL query builder that works on top of the `SQLAlchemy Core` expression language. It supports the following queries:
        - database.fetch_all(query)
        - database.fetch_one(query)
        - database.iterate(query)
        - database.execute(query)
        - database.execute_many(query)

1. ensure the `notes` table is created
    > $ docker-compose exec db psql --username=hello_fastapi --dbname=hello_fastapi_dev
    ~~~sh 
        hello_fastapi_dev=# \l ## list of databases
        hello_fastapi_dev=# \c hello_fastapi_dev
        ## You are now connected to database "hello_fastapi_dev" as user "hello_fastapi".
        hello_fastapi_dev=# \q # quit
    ~~~

1. Pydantic 
    - Data validation and settings management using python type annotations.
    - `pydantic` enforces type hints at runtime, and provides user friendly errors when data is invalid.

1. Testing with HTTPie
 
    > http --json POST http://localhost:8002/notes/ title=foo description=bar 
        HTTP/1.1 201 Created
        content-length: 42
        content-type: application/json
        date: Mon, 14 Sep 2020 16:47:51 GMT
        server: uvicorn

        {
            "description": "bar",
            "id": 1,
            "title": "foo"
        }

1.  We can add  metadata to the parameter with `Path`:
    ~~~py
    async def read_note(id: int = Path(..., gt=0),):
        pass
        # ... - the value is required (Ellipsis)
        #  gt - the value must be greater than 0
    ~~~
    


----------------------------------------------------------------------------------------

### References
1. https://testdriven.io/blog/fastapi-crud/
1. https://www.uvicorn.org/#running-with-gunicorn
1. https://www.toptal.com/python/build-high-performing-apps-with-the-python-fastapi-framework