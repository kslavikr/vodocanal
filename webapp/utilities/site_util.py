import datetime
def allow_update():
    day_now=datetime.datetime.now().day
    if day_now>9 and day_now<29:
        return True
    return False