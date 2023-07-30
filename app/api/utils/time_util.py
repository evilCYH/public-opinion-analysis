import datetime


def day_get(d,day):
    oneday = datetime.timedelta(days=day)
    day = d - oneday
    date_from = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
    date_to = datetime.datetime(day.year, day.month, day.day, 23, 59, 59)
    print('---'.join([str(date_from), str(date_to)]))

def week_get(d):
    dayscount = datetime.timedelta(days=d.isoweekday())
    dayto = d - dayscount
    sixdays = datetime.timedelta(days=6)
    dayfrom = dayto - sixdays
    date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
    print ('---'.join([str(date_from), str(date_to)]))

def month_get(d):
    """    
    返回上个月第一个天和最后一天的日期时间
    :return
    date_from: 2016-01-01 00:00:00
    date_to: 2016-01-31 23:59:59
    """
    dayscount = datetime.timedelta(days=d.day)
    dayto = d - dayscount
    date_from = datetime.datetime(dayto.year, dayto.month, 1, 0, 0, 0)
    date_to = datetime.datetime(dayto.year, dayto.month, dayto.day, 23, 59, 59)
    print ('---'.join([str(date_from), str(date_to)]))
    return date_from, date_to


def get_last_week():
    current = datetime.datetime.now()
    oneday = datetime.timedelta(days=7)
    day = current - oneday
    date_from = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
    date_to = datetime.datetime(current.year, current.month, current.day, 23, 59, 59)
    return date_from,date_to

if __name__ == "__main__":
    date_from,date_to = get_last_week()
    print(date_from)
    print(date_to)