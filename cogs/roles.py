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
    self.main_role_names = map(lambda x: x.role_name, RHYTHM_GAMES)
    self.main_roles = {}
    self.location_role_names = map(lambda x: x.role_name, LOCATIONS)
    self.location_roles = {}
    self.guild = None

  def cache_roles(self):
    if not self.main_roles and not self.location_roles:
      self.guild = discord.Client.get_guild(self=self.bot, id=TWO_MF_GUILD_ID)
      for role in self.guild.roles:
        if role.name in self.main_role_names:
          self.main_roles[role.name] = role
        if role.name in self.location_role_names:
          self.location_roles[role.name] = role

  def get_main_role(self, ctx):
    main_role = list(set(ctx.author.roles) & set(self.main_roles[ctx.guild.id]))
    return main_role[0] if main_role else None

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
      matches = list(filter(lambda x: x.emote == payload.emoji.name, RHYTHM_GAMES))
      if matches:
        await self.add_or_remove_game_role(channel, payload, matches[0].role_name)

  @commands.command(
    description='Manage your main game role.',
    usage='gamerole'
  )
  async def gamerole(self, ctx):
    current_main_role = self.get_main_role(ctx)

    def main_role_option_check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in list(
        range(len(self.main_roles[ctx.guild.id]) + 1))

    if current_main_role:
      await ctx.send(
        'Your current main game role: **{0}**.\nEnter 0 to delete your main game role.\nEnter one of the numbers to '
        'change your main game role.'.format(
          current_main_role))
    else:
      await ctx.send('You currently do not have a main game role.\nEnter one of the numbers to add a main game role.')
    await ctx.send('\n'.join(['**{0}**: {1}'.format(i + 1, v) for i, v in enumerate(self.main_roles[ctx.guild.id])]))

    response = await discord.Client.wait_for(self=self.bot, event='message', timeout=30, check=main_role_option_check)
    if response:
      if current_main_role:
        await ctx.author.remove_roles(current_main_role)
        await ctx.send('Deleted current main game role of **{0}**.'.format(current_main_role))
      choice = int(response.content) - 1
      if choice != -1:
        desired_role = self.main_roles[ctx.guild.id][choice]
        await ctx.author.add_roles(desired_role)
        await ctx.send('Added main game role of **{0}**.'.format(desired_role))
      await response.delete()

  @commands.command(
    description='Manage your Round 1 location roles.',
    usage='locationrole'
  )
  async def locationrole(self, ctx):

    def location_role_reaction_check(reaction, user):
      return user == ctx.author

    message = await ctx.send(embed=make_location_role_embed())
    await message.add_reaction('🍚')
    await message.add_reaction('🍘')
    await message.add_reaction('🍙')
    await message.add_reaction('🎑')
    await message.add_reaction('🌾')

    try:
      reaction, user = await discord.Client.wait_for(self=self.bot, event='reaction_add', timeout=30.0,
                                                     check=location_role_reaction_check)
      while reaction:
        if reaction.emoji == '🍚':
          await self.add_or_remove_location_role(ctx, user, 'PHM')
        elif reaction.emoji == '🍘':
          await self.add_or_remove_location_role(ctx, user, 'MPM')
        elif reaction.emoji == '🍙':
          await self.add_or_remove_location_role(ctx, user, 'LWM')
        elif reaction.emoji == '🎑':
          await self.add_or_remove_location_role(ctx, user, 'MVM')
        elif reaction.emoji == '🌾':
          await self.add_or_remove_location_role(ctx, user, '池袋')
        reaction, user = await discord.Client.wait_for(self=self.bot, event='reaction_add', timeout=30.0,
                                                       check=location_role_reaction_check)
    except asyncio.TimeoutError:
      pass

  async def add_or_remove_location_role(self, channel, payload, location):
    member = self.guild.get_member(user_id=payload.user_id)
    for role in member.roles:
      if role.name == location:
        await member.remove_roles(role)
        msg = await channel.send('Role for {0} removed.'.format(location))
        await asyncio.sleep(5)
        await msg.delete()
        return
    await member.add_roles(self.location_roles[location])
    msg = await channel.send('Role for {0} added.'.format(location))
    await asyncio.sleep(5)
    await msg.delete()
