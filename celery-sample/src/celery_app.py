from celery import Celery

# app = Celery("proj", broker="amqp://", backend="rpc://", include=["proj.tasks"])
app = Celery(__name__)

app.config_from_object("celery_config")


if __name__ == "__main__":
    app.start()
