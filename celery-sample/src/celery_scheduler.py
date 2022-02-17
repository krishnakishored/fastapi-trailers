from celery.schedules import crontab

# add "birthdays_today" task to the beat schedule
app.conf.beat_schedule = {
    "birthday-task": {
        "task": "birthdays.birthdays_today",
        "schedule": crontab(hour=7, minute=0),
    }
}


""" crontab patterns
# a job is scheduled to run for every minute of every day
crontab(minute="*")
# a job is scheduled to run for every minute between 1am and 2am
crontab(hour=1, minute="*")
# a job is scheduled to run for every first minute of every hour
crontab(hour="*", minute=1)


# a job is scheduled to run for every minute in the first quarter of 
# each hour
crontab(minute="0-15")
# a job is scheduled to run at 1am on weekdays only
crontab(day_of_week="1-5", hour=1, minute=0)
# a job is scheduled to run on the first five days of every month at # 7:30 am
crontab(day_of_month="1-5", hour=7, minute=30)

# a job is scheduled to run on the first day of each yearly quarter
# at 8:30am
crontab(month_of_year="1,4,7,10", day_of_month=1, hour=8, minute=30)
# a job is scheduled to run on weekends at 12:15 and 00:15
crontab(day_of_week="0,6", hour="0,12", minute=15)

# a job is scheduled to run every five hours
crontab(hour="*/5")
# a job is scheduled to run every seventeen minutes
crontab(minute="*/17")
# a job is scheduled to run every two minutes during the second
# half of each hour
crontab(minute="30-59/2")
# a job is scheduled to run at the top of every hour from 6am to 6pm # and runs after every three hours thereafter
crontab(hour="*/3,6-18")
"""
