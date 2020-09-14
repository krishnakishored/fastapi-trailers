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

### References
1. https://testdriven.io/blog/fastapi-crud/
1. https://www.uvicorn.org/#running-with-gunicorn
1. https://www.toptal.com/python/build-high-performing-apps-with-the-python-fastapi-framework