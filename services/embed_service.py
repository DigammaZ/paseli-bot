import discord
import random

COLORS = [0xfd5e53, 0xeaebff, 0xe0fefe, 0xd3eeff, 0xffd6f3]

from services.time_service import get_time_from_epoch

#########################
# MISC PLUGIN CONSTANTS #
#########################

PASELI_URL = 'https://img.konami.com/amusement/paseli/img/index/charge_paseli_icon.png'

#############################
# MISC PLUGIN EMBED METHODS #
#############################

def make_help_embed(commands):
  embed = discord.Embed(title='Help', description='Available commands. Don\'t forget the prefix `!`.', color=random.choice(COLORS))
  embed.set_thumbnail(url=PASELI_URL)
  for key, value in commands.items():
    embed.add_field(name=key, value=value, inline=False)
  return embed

###############################
# REMIND PLUGIN EMBED METHODS #
###############################

def make_remind_embed(results):
  embed = discord.Embed(title='Your reminds', description='Enter 0 to delete a remind', color=random.choice(COLORS))
  for i, result in enumerate(results):
    embed.add_field(name='Remind {0} at {1}'.format(i+1, get_time_from_epoch(result['requested_time'])), value=result['message'], inline=False)
  return embed
