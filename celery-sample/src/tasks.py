import time

from celery.schedules import crontab
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

from src.celery_app import app


@app.on_after_finalize.connect
def setup_periodic_task(**kwargs):
    # # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s("hello"), name="add every 10")

    # # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s("world"), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # print(**kwargs)
    periodic_task_key = app.add_periodic_task(
        # crontab(
        #     minute=kwargs.get("minute"),
        #     hour=kwargs.get("hour"),
        #     day_of_week=kwargs.get("day_of_week"),
        #     day_of_month=kwargs.get("day_of_month"),
        #     month_of_year=kwargs.get("month_of_year"),
        # ),
        crontab(minute="*"),
        # crontab(hour=7, minute=30, day_of_week=1),
        add.s(41, 999),
    )
    return periodic_task_key


# @app.task(bind=True, retry_limit=4, default_retry_delay=10)
@app.task
def add(x, y):
    logger.info(f"Adds {x} + {y}")
    return x + y


@app.task
def mul(x, y):
    logger.info(f"Multiplies {x} * {y}")
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task(name="delayed_addition")
def delayed_addition(delay, x, y):
    logger.info(f"delayed addition {x} + {y} with delay:{delay}")
    time.sleep(delay)
    return x + y
