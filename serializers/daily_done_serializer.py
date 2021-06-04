from services.db_service import select_daily_done


def get_daily_done(discord_id):
  rows = select_daily_done(discord_id=discord_id)
  if not rows:
    return []
  return [{
    'discord_id': row[0]
  } for row in rows]
