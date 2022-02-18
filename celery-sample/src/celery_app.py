from celery import Celery

from src.celery_config import CeleryConfig

# app = Celery("proj", broker="amqp://", backend="rpc://", include=["proj.tasks"])
app = Celery(__name__)


app.config_from_object(CeleryConfig)


if __name__ == "__main__":
    app.start()
