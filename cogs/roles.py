import discord
from discord.ext import commands

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

  @commands.command(
    description='Manage your main game role.',
    usage='mainrole'
  )
  async def mainrole(self, ctx, *args):
    self.cache_main_roles(ctx.guild)
    current_main_role = self.get_main_role(ctx)

    def main_role_option_check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel and int(msg.content) in list(range(len(self.main_roles[ctx.guild.id]) + 1))

    if current_main_role:
      await ctx.send('Your current main game role: {0}.\nEnter 0 to delete your main game role.\nEnter one of the numbers to change your main game role.'.format(current_main_role))
    else:
      await ctx.send('You currently do not have a main game role.\nEnter one of the numbers to add a main game role.')
    await ctx.send('\n'.join(['{0}: {1}'.format(i+1, v) for i, v in enumerate(self.main_roles[ctx.guild.id])]))
    
    response = await discord.Client.wait_for(self=self.bot, event='message', timeout=30, check=main_role_option_check)
    if response:
      if current_main_role:
        await ctx.author.remove_roles(current_main_role)
        await ctx.send('Deleted current main game role of {0}.'.format(current_main_role))
      choice = int(response.content)-1
      if choice != -1:
        desired_role = self.main_roles[ctx.guild.id][choice]
        await ctx.author.add_roles(desired_role)
        await ctx.send('Added main game role of {0}.'.format(desired_role))
      await response.delete()
