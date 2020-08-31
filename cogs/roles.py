import discord
from discord.ext import commands
import asyncio

from services.embed_service import make_location_role_embed

class Roles(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.main_role_names = set([
      'Dance Rush Main',
      'DDR Main',
      'Gitadora Main',
      'Groove Coaster Main',
      'IIDX Main',
      'Pop\'n Main',
      'Pump Main',
      'SDVX Main'
    ])
    self.main_roles = {}
    self.location_role_names = set([
      'PHM', 'MPM', 'MVM', 'LWM', '池袋'
    ])
    self.location_roles = {}

  def cache_main_roles(self, guild):
    if guild.id not in self.main_roles:
      self.main_roles[guild.id] = []
      for role in guild.roles:
        if role.name in self.main_role_names:
          self.main_roles[guild.id].append(role)
        self.main_roles[guild.id].sort(key=lambda role: role.name)

  def get_main_role(self, ctx):
    main_role = list(set(ctx.author.roles) & set(self.main_roles[ctx.guild.id]))
    return main_role[0] if main_role else None

  def cache_location_roles(self, guild):
    if guild.id not in self.location_roles:
      self.location_roles[guild.id] = {}
      for role in guild.roles:
        if role.name in self.location_role_names:
          self.location_roles[guild.id][role.name] = role

  @commands.command(
    description='Manage your main game role.',
    usage='gamerole'
  )
  async def gamerole(self, ctx, *args):
    self.cache_main_roles(ctx.guild)
    current_main_role = self.get_main_role(ctx)

    def main_role_option_check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in list(range(len(self.main_roles[ctx.guild.id]) + 1))

    if current_main_role:
      await ctx.send('Your current main game role: **{0}**.\nEnter 0 to delete your main game role.\nEnter one of the numbers to change your main game role.'.format(current_main_role))
    else:
      await ctx.send('You currently do not have a main game role.\nEnter one of the numbers to add a main game role.')
    await ctx.send('\n'.join(['**{0}**: {1}'.format(i+1, v) for i, v in enumerate(self.main_roles[ctx.guild.id])]))
    
    response = await discord.Client.wait_for(self=self.bot, event='message', timeout=30, check=main_role_option_check)
    if response:
      if current_main_role:
        await ctx.author.remove_roles(current_main_role)
        await ctx.send('Deleted current main game role of **{0}**.'.format(current_main_role))
      choice = int(response.content)-1
      if choice != -1:
        desired_role = self.main_roles[ctx.guild.id][choice]
        await ctx.author.add_roles(desired_role)
        await ctx.send('Added main game role of **{0}**.'.format(desired_role))
      await response.delete()

  @commands.command(
    description='Manage your Round 1 location roles.',
    usage='locationrole'
  )
  async def locationrole(self, ctx, *args):
    self.cache_location_roles(ctx.guild)

    def location_role_reaction_check(reaction, user):
      return user == ctx.author

    message = await ctx.send(embed=make_location_role_embed())
    await message.add_reaction('🍚')
    await message.add_reaction('🍘')
    await message.add_reaction('🍙')
    await message.add_reaction('🎑')
    await message.add_reaction('🌾')

    try:
      reaction, user = await discord.Client.wait_for(self=self.bot, event='reaction_add', timeout=30.0, check=location_role_reaction_check)
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
        reaction, user = await discord.Client.wait_for(self=self.bot, event='reaction_add', timeout=30.0, check=location_role_reaction_check)
    except asyncio.TimeoutError:
      pass

  async def add_or_remove_location_role(self, ctx, user, location):
    for role in user.roles:
      if role.name == location:
        await ctx.author.remove_roles(role)
        await ctx.send('Role for {0} removed.'.format(location))
        return
    await ctx.author.add_roles(self.location_roles[ctx.guild.id][location])
    await ctx.send('Role for {0} added.'.format(location))
