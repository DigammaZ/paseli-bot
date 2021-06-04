import discord
import random

from constants import PREFIX

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
  embed = discord.Embed(title='Round 1 Location Roles', description='React to add or remove a role.',
                        color=random.choice(COLORS))
  embed.set_thumbnail(url=ROUND_1_LOGO_URL)
  embed.add_field(name=':rice: PHM', value='Puente Hills Mall', inline=False)
  embed.add_field(name=':rice_cracker: MPM', value='Main Place Mall', inline=False)
  embed.add_field(name=':rice_ball: LWM', value='Lakewood Mall', inline=False)
  embed.add_field(name=':rice_scene: MVM', value='Moreno Valley Mall', inline=False)
  embed.add_field(name=':ear_of_rice: 池袋', value='Ikebukuro, Tokyo, Japan', inline=False)
  embed.add_field(name='Not Listed', value='Sucks 2 suck jk ask someone to add your main arcade', inline=False)
  return embed
