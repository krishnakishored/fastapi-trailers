from config import Settings, get_settings

settings: Settings = get_settings()

# import multiprocessing

# should be the internal docker PORT service
bind = f"{settings.HOST}:7600"
# # to run locally- $ gunicorn -c src/gunicorn.conf.py main:app
# bind = f"{settings.HOST}:7600"
# (TODO:change it to 7600 to match the external port)

# workers = multiprocessing.cpu_count() * 2 + 1
workers = settings.GUNICORN_WORKERS
timeout = settings.GUNICORN_TIMEOUT  # in seconds
worker_class = "uvicorn.workers.UvicornWorker"
# print(f"no.of gunicorn workers:{workers}")

# worker_class = "sync" # explore gevent, gthread
# worker_connections # for gevent workers
