from services.db_service import select_reminds, show_reminds

def get_reminds(requested_time=0, user_id='%%', guild_id='%%'):
  if requested_time:
    rows = select_reminds(requested_time=requested_time, user_id=user_id)
  else:
    rows = show_reminds(user_id=user_id, guild_id=guild_id)
  if not rows:
    return []
  return [{
    'id': row[0],
    'requested_time': row[1],
    'channel_id': row[2],
    'user_id': row[3],
    'message': row[4],
    'guild_id': row[5]
  } for row in rows]
