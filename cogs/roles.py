import discord
from discord.ext import commands
import asyncio

from constants import ROLES_CHANNEL_ID, LOCATION_ROLES_MSG_ID, MAIN_ROLES_MSG_ID, TWO_MF_GUILD_ID

from models.locations import LOCATIONS
from models.rhythm_games import RHYTHM_GAMES

from services.embed_service import make_location_role_embed, make_main_role_embed


class Roles(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.main_role_names = list(map(lambda x: x.role_name, RHYTHM_GAMES))
    self.main_roles = {}
    self.location_role_names = list(map(lambda x: x.role_name, LOCATIONS))
    self.location_roles = {}
    self.guild = None

  def cache_roles(self):
    if not self.main_roles or not self.location_roles or not self.guild:
      self.guild = discord.Client.get_guild(self=self.bot, id=TWO_MF_GUILD_ID)
      for role in self.guild.roles:
        if role.name in self.main_role_names:
          self.main_roles[role.name] = role
        if role.name in self.location_role_names:
          self.location_roles[role.name] = role

  @commands.command(
    description='Initialize role embed messages.',
    usage='initrolesembed'
  )
  async def initrolesembed(self, ctx):
    location_roles_msg = await ctx.send(embed=make_location_role_embed())
    main_roles_msg = await ctx.send(embed=make_main_role_embed())

    for emote in list(map(lambda x: x.emote, LOCATIONS)):
      await location_roles_msg.add_reaction(emote)

    for emote in list(map(lambda x: x.emote, RHYTHM_GAMES)):
      await main_roles_msg.add_reaction(emote)

    await ctx.message.delete()

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    await self.handle_react(payload)

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    await self.handle_react(payload)

  async def handle_react(self, payload):
    self.cache_roles()
    channel = self.bot.get_channel(ROLES_CHANNEL_ID)
    if payload.message_id == LOCATION_ROLES_MSG_ID:
      matches = list(filter(lambda x: x.emote == payload.emoji.name, LOCATIONS))
      if matches:
        await self.add_or_remove_location_role(channel, payload, matches[0].role_name)

    elif payload.message_id == MAIN_ROLES_MSG_ID:
      matches = list(filter(lambda x: x.emote_id == payload.emoji.id, RHYTHM_GAMES))
      if matches:
        await self.add_or_remove_game_role(channel, payload, matches[0].role_name)

  def get_main_role(self, member):
    main_role = list(set(member.roles) & set(self.main_roles.values()))
    return main_role[0] if main_role else None


  async def add_or_remove_game_role(self, channel, payload, game):
    member = self.guild.get_member(user_id=payload.user_id)
    for role in member.roles:
      if role.name == game:
        await member.remove_roles(role)
        msg = await channel.send('{0} role removed for <@{1}>.'.format(game, payload.user_id))
        await asyncio.sleep(5)
        await msg.delete()
        return

    current_main_role = self.get_main_role(member)
    if current_main_role:
      await member.remove_roles(current_main_role)
      await member.add_roles(self.main_roles[game])
      msg = await channel.send('{0} role replaced with {1} role for <@{2}>.'.format(current_main_role.name, game, payload.user_id))
    else:
      await member.add_roles(self.main_roles[game])
      msg = await channel.send('{0} role added for <@{1}>.'.format(game, payload.user_id))
    await asyncio.sleep(5)
    await msg.delete()

  async def add_or_remove_location_role(self, channel, payload, location):
    member = self.guild.get_member(user_id=payload.user_id)
    for role in member.roles:
      if role.name == location:
        await member.remove_roles(role)
        msg = await channel.send('{0} role removed for <@{1}>.'.format(location, payload.user_id))
        await asyncio.sleep(5)
        await msg.delete()
        return
    await member.add_roles(self.location_roles[location])
    msg = await channel.send('{0} role added for <@{1}>.'.format(location, payload.user_id))
    await asyncio.sleep(5)
    await msg.delete()
