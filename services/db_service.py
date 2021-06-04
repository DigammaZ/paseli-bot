import sqlite3

USER_GENERATED_DB = 'user_generated.db'


def select_reminds(requested_time, user_id='%%'):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM remind WHERE requested_time=? AND user_id LIKE ?', (requested_time, user_id))
  rows = c.fetchall()
  conn.close()
  return rows


def show_reminds(user_id='%%', guild_id='%%'):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM remind WHERE user_id LIKE ? AND guild_id LIKE ? ORDER BY requested_time ASC',
            (user_id, guild_id))
  rows = c.fetchall()
  conn.close()
  return rows


def count_reminds(user_id='%%', guild_id='%%'):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('SELECT COUNT(*) FROM remind WHERE user_id LIKE ? AND guild_id LIKE ?', (user_id, guild_id))
  (count,) = c.fetchone()
  conn.close()
  return count


def insert_remind(requested_time, channel_id, user_id, message, guild_id):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('INSERT INTO remind(requested_time, channel_id, user_id, message, guild_id) VALUES (?,?,?,?,?)',
            (requested_time, channel_id, user_id, message, guild_id))
  conn.commit()
  conn.close()


def delete_remind(requested_time, channel_id, user_id, message, guild_id):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute(
    'DELETE FROM remind WHERE requested_time = ? AND channel_id = ? AND user_id = ? AND message = ? AND guild_id = ?',
    (requested_time, channel_id, user_id, message, guild_id))
  conn.commit()
  conn.close()


def delete_old_reminds(requested_time=0):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('DELETE FROM remind WHERE requested_time <= ?', (requested_time,))
  conn.commit()
  conn.close()


def insert_daily_done(discord_id):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('INSERT INTO daily_done(discord_id) VALUES (?)', (discord_id,))
  conn.commit()
  conn.close()


def select_daily_done(discord_id):
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('SELECT * FROM daily_done WHERE discord_id = ?', (discord_id,))
  rows = c.fetchall()
  conn.close()
  return rows


def delete_daily_done():
  conn = sqlite3.connect(USER_GENERATED_DB)
  c = conn.cursor()
  c.execute('DELETE FROM daily_done')
  conn.commit()
  conn.close()
