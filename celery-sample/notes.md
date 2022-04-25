## Questions & comments
1. Celery is distributed task queue
1. celery vs redis-queue
1. brokers and backends
    1. using redis vs rabitmq or kafka for message broker
    1. sqlite or redis as backend
1. celery in fastapi & compare with background tasks

## Celery topics
1. `@app.task(bind=True)` - Bound tasks are needed for retries (using app.Task.retry()), for accessing information about the current task request, and for any additional functionality you add to custom task base classes.
The `bind` argument means that the function will be a “bound method” so that you can access attributes and methods on the task type instance.
The `bind` argument to the task decorator will give access to `self` (the task type instance).





### Commands 

1. Celery worker
        ~~~sh
        # @~/coding/python-coding/fastapi-trailers/celery-sample
        # export PYTHONPATH=src:src/common:  
        ~~~
        `$ celery -A src.celery_app worker --loglevel=info `

    - TODO: in production use daemonization
        `$ celery multi start w1 -A proj -l INFO `

   - celery worker is used to start a Celery worker
        --app=worker.celery runs the Celery Application 
        --loglevel=info sets the logging level to info

1. Monitoring
    - `$ celery -A src.celery_app flower --port=5556 `
    - `$ celery -A tasks flower --port=5555`

1. Scheduling/Periodic jobs
    - `celery beat` is a scheduler; It kicks off tasks at regular intervals, that are then executed by available worker nodes in the cluster
    - `$ celery -A src.celery_app beat --loglevel=info `

### References

1. celery 
    - https://www.youtube.com/watch?v=THxCy-6EnQM
    - FastAPI Celery, Flower and Docker
        - https://www.youtube.com/watch?v=mcX_4EvYka4&t=1443s
1. background tasks - https://www.youtube.com/watch?v=_yXOJvr5vOM
1. https://medium.com/thelorry-product-tech-data/celery-asynchronous-task-queue-with-fastapi-flower-monitoring-tool-e7135bd0479f
1. https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/index.html#broker-overview
1. https://stackoverflow.com/questions/10194975/how-to-dynamically-add-remove-periodic-tasks-to-celery-celerybeat
1. https://www.youtube.com/watch?v=Bo6UtRhedjE
1. https://denibertovic.com/posts/celery-best-practices/
1. https://blog.balthazar-rouberol.com/celery-best-practices
1. https://devchecklists.com/celery-tasks-checklist/
1. https://www.youtube.com/watch?v=XoMu8vhdc-A
1. https://www.vinta.com.br/blog/2018/celery-wild-tips-and-tricks-run-async-tasks-real-world/
1. https://medium.com/analytics-vidhya/python-celery-explained-for-beginners-to-professionals-part-3-workers-pool-and-concurrency-ef0522e89ac5

----------------------------------------------------------------

