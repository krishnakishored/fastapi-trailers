import time

from celery import Celery

app = Celery(__name__)

app.config_from_object("celery_config")

from celery.schedules import crontab

# add "birthdays_today" task to the beat schedule
app.conf.beat_schedule = {
    "schedule-addtion_task": {
        # "task": "celery_worker.addition_task",
        "task": "addition_task",
        "args": (2, 1111, 5678),
        # a job is scheduled to run for every minute of every day
        # "schedule": crontab(minute="*")
        "schedule": crontab(
            minute="55", hour="6", day_of_week="*", day_of_month="*", month_of_year="*"
        )
        # "schedule": crontab(hour=23, minute=0),
    }
}


"""
TO EXPLORE in celery features - 
1. how to create task chain (each dependent on the previous task). each task after completion updates the transaction table
2. Schedule task (at given time stamp)
3. periodical task (weekly, monthly.. or an interval - use crontab)

#######

input: 
1. MassGIS_ID (str)
2. file path SFTP with "MassGIS_ID" dir
3. get the latest file from this dir (this will be the input raw file)
4. use the raw file to generateSource(), generateTiles(),generateAddressDat() 
5. copy the generated files to output archive location.
todo: create a version number based timestamp
      eg. version - MASSGIS_2022_02_16

"""
