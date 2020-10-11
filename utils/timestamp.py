from datetime import datetime, timedelta
from dateutil.relativedelta import *

now = datetime.now()
date = now.strftime("%d/%m/%y")
time = now.strftime("%H:%M")
online = now.strftime("%d%m%y")

def get_time_stamp():
    return f"{date} - {time}"

def online():
    return f"{now}"

def offline(m):
    offline = now + relativedelta(months=+m)
    return f"{offline}"

def get_date():
    return date
