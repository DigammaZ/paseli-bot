import discord
from datetime import datetime

from serializers.remind_serializer import get_reminds

from services.db_service import count_reminds, insert_remind, delete_old_reminds
from services.time_service import get_nearest_datetime

REMIND_LIMIT = 10


# returns message to show in discord
def create_remind(ctx, time, ampm, message):
  try:
    requested_time = get_nearest_datetime(time, ampm)
  except ValueError as e:
    return e

  count = count_reminds(user_id=ctx.author.id, guild_id=ctx.guild.id)
  if count >= REMIND_LIMIT:
    return 'You already have {0} reminds.'.format(REMIND_LIMIT)
  else:
    insert_remind(requested_time=requested_time, channel_id=ctx.channel.id, user_id=ctx.author.id, message=message,
                  guild_id=ctx.guild.id)
    return 'You have {0} reminds remaining. Reminding at {1} {2}.'.format(REMIND_LIMIT - count - 1, time, ampm)


async def send_and_delete_reminds(bot):
  timestamp = datetime.now().replace(second=0, microsecond=0).timestamp()
  reminds = get_reminds(requested_time=timestamp)
  for remind in reminds:
    channel = discord.Client.get_channel(self=bot, id=remind['channel_id'])
    await channel.send('<@{0}> {1}'.format(remind['user_id'], remind['message']))
  delete_old_reminds(requested_time=timestamp)
