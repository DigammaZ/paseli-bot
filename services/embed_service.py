import discord
import random

from constants import PREFIX

from models.locations import LOCATIONS
from models.rhythm_games import RHYTHM_GAMES

from services.time_service import get_time_from_epoch

COLORS = [0xfd5e53, 0xeaebff, 0xe0fefe, 0xd3eeff, 0xffd6f3]

#########################
# MISC PLUGIN CONSTANTS #
#########################

PASELI_URL = 'https://img.konami.com/amusement/paseli/img/index/charge_paseli_icon.png'


#############################
# MISC PLUGIN EMBED METHODS #
#############################

def make_help_embed(commands):
  embed = discord.Embed(title='Help', description='Available commands. Don\'t forget the prefix `{0}`.'.format(PREFIX),
                        color=random.choice(COLORS))
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
    embed.add_field(name='Remind {0} at {1}'.format(i + 1, get_time_from_epoch(result['requested_time'])),
                    value=result['message'], inline=False)
  return embed


#########################
# ROLE PLUGIN CONSTANTS #
#########################

ROUND_1_LOGO_URL = 'https://static.wixstatic.com/media/83891d_a7f0ffee16ed41aea52a7d8ee7574379~mv2.png'


#############################
# ROLE PLUGIN EMBED METHODS #
#############################

def make_location_role_embed():
  embed = discord.Embed(title='Round 1 Location Roles', description='React to add or remove a role. You may have '
                                                                    'multiple.',
                        color=random.choice(COLORS))
  embed.set_thumbnail(url=ROUND_1_LOGO_URL)
  for location in LOCATIONS:
    embed.add_field(name='{0} {1}'.format(location.emote, location.role_name), value=location.full_name, inline=False)
  return embed


def make_main_role_embed():
  embed = discord.Embed(title='Main Rhythm Game Roles', description='React to add or remove a role. You may only have '
                                                                    'one.',
                        color=random.choice(COLORS))
  embed.set_thumbnail(url=random.choice(list(map(lambda x: x.logo_url, RHYTHM_GAMES))))
  for game in RHYTHM_GAMES:
    embed.add_field(name='{0} {1}'.format(game.emote, game.role_name), value=game.name, inline=False)
  return embed
