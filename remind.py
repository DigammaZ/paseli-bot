import sqlite3
import asyncio
import discord
from datetime import datetime, timedelta
import pytz
pt = pytz.timezone('US/Pacific')

REMIND_LIMIT = 10
USER_GENERATED_DB = 'user_generated.db'

async def poll(bot):
  while(True):
    now_timestamp = datetime.now().replace(second=0, microsecond=0).timestamp()
    next_timestamp = now_timestamp + 60
    await asyncio.sleep(next_timestamp - datetime.now().timestamp())
    await send_reminds(bot, next_timestamp)

async def send_reminds(bot, next_timestamp):
  reminds = get_reminds(requested_time=next_timestamp)
  for remind in reminds:
    channel = discord.Object(remind['channel_id'])
    await bot.send_message(channel, '<@{0}> {1}'.format(remind['user_id'], remind['message']))
  delete_old_reminds(requested_time=next_timestamp)

def get_reminds(requested_time=0, user_id='%%'):
  if requested_time:
    rows = select_reminds(requested_time=requested_time, user_id=user_id)
  else:
    rows = show_reminds(user_id=user_id)
  if not rows:
    return []
  return [{
    'id': row[0],
    'requested_time': row[1],
    'channel_id': row[2],
    'user_id': row[3],
    'message': row[4]
  } for row in rows]

def attempt_create_remind(ctx, hour_min, am_pm, msg):
  requested_time = convert_to_valid_time(hour_min, am_pm)
  count = count_reminds(user_id=ctx.message.author.id)
  if count >= REMIND_LIMIT:
    return 'You already have {0} reminds'.format(REMIND_LIMIT)
  else:
    insert_remind(requested_time=requested_time, channel_id=ctx.message.channel.id, user_id=ctx.message.author.id, message=msg)
    return 'You have {0} reminds remaining. Reminding at {1} {2}.'.format(REMIND_LIMIT - count - 1, hour_min, am_pm)

def convert_to_valid_time(hour_min, am_pm):
  hour, min, am_pm = int(hour_min.split(':')[0]), int(hour_min.split(':')[1]), am_pm.upper()
  validate(hour, min, am_pm)

  hour = hour - 12 if hour == 12 and am_pm == 'AM' else hour
  hour = hour + 12 if hour != 12 and am_pm == 'PM' else hour
  date = datetime.now(pt).replace(hour=hour, minute=min, second=0, microsecond=0)
  now  = datetime.now(pt)

  if date < now:
    date = date + timedelta(days=1)
  return date.timestamp()

def validate(hour, min, am_pm):
  if hour > 12 or hour <= 0:
    raise ValueError('Hour must be within 1-12.')
  elif min < 0 or min > 59:
    raise ValueError('Minute must be within 0-59.')
  elif am_pm != 'AM' and am_pm != 'PM':
    raise ValueError('Must specify AM or PM.')

def select_reminds(requested_time, user_id='%%'):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM remind WHERE requested_time=? AND user_id LIKE ?', (requested_time, user_id))
  rows = c.fetchall()
  conn.close()
  return rows

def count_reminds(user_id='%%'):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('SELECT COUNT(*) FROM remind WHERE user_id LIKE ?', (user_id,))
  (count,) = c.fetchone()
  conn.close()
  return count

def insert_remind(requested_time, channel_id, user_id, message):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('INSERT INTO remind(requested_time, channel_id, user_id, message) VALUES (?,?,?,?)', (requested_time, channel_id, user_id, message))
  conn.commit()
  conn.close()

def delete_remind(requested_time, channel_id, user_id, message):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('DELETE FROM remind WHERE requested_time = ? AND channel_id = ? AND user_id = ? AND message = ?', (requested_time, channel_id, user_id, message))
  conn.commit()
  conn.close()

def delete_old_reminds(requested_time=0, channel_id=None, user_id=None, message=None):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('DELETE FROM remind WHERE requested_time <= ?', (requested_time,))
  conn.commit()
  conn.close()
