from datetime import datetime, timedelta
import pytz
pst = pytz.timezone('US/Pacific')
jst = pytz.timezone('Asia/Tokyo')

def get_time_from_epoch(epoch, tz=pst):
  dt = datetime.fromtimestamp(epoch, tz)
  hour = dt.hour
  AMPM = 'PM' if hour >= 12 else 'AM'
  hour = hour - 12 if hour > 12 else hour
  hour = hour + 12 if hour == 0 else hour
  minute = '0{0}'.format(dt.minute) if dt.minute < 10 else str(dt.minute)
  return '{0}:{1} {2}'.format(hour, minute, AMPM)

def get_date_from_epoch(epoch, tz=pst):
  dt = datetime.fromtimestamp(epoch, tz)
  month = dt.month
  day   = dt.day
  month = '0{0}'.format(month) if month < 10 else str(month)
  day   = '0{0}'.format(day)   if day   < 10 else str(day)
  return '{0}/{1}'.format(month, day)

def get_weekday(dt):
  num = dt.weekday()
  day_dic = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
  }
  return day_dic[num]

def validate_time(hour, minute, AMPM):
  if hour > 12 or hour <= 0:
    raise ValueError('Hour must be within 1-12.')
  elif minute < 0 or minute > 59:
    raise ValueError('Minute must be within 0-59.')
  elif AMPM != 'AM' and AMPM != 'PM':
    raise ValueError('Must specify AM or PM.')

def attempt_to_create_valid_datetime(time, AMPM):
  time_arr = time.split(':')
  hour = int(time_arr[0])
  mins = int(time_arr[1])
  AMPM = AMPM.upper()

  validate_time(hour, mins, AMPM)

  hour = hour - 12 if hour == 12 and AMPM == 'AM' else hour
  hour = hour + 12 if hour != 12 and AMPM == 'PM' else hour
  return datetime.now(pst).replace(hour=hour, minute=mins, second=0, microsecond=0)

def get_nearest_datetime(time, AMPM):
  date = attempt_to_create_valid_datetime(time, AMPM)
  now = datetime.now(pst)

  if date < now:
    date = date + timedelta(days=1)
  return date.timestamp()

def get_current_japan_time():
  jp_dt = datetime.now()
  return '{0}, {1}, {2}'.format(get_weekday(jp_dt), get_date_from_epoch(jp_dt.timestamp(), tz=jst), get_time_from_epoch(datetime.now().timestamp(), tz=jst))
