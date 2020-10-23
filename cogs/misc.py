import discord
from discord.ext import commands
import os

from constants import CELI_ID, DIGAMMA_ID, PREFIX, WELCOME_CHANNEL_ID, TWO_MF_GUILD_ID

from services.embed_service import make_help_embed

class Miscellaneous(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.remove_command('help')
    self.command_usage_dict = {}
    self.command_description_dict = {}

  def init_command_description_dict(self):
    if not self.command_description_dict:
      for command in self.bot.commands:
        self.command_description_dict[command.name] = command.description

  def init_command_usage_dict(self):
    if not self.command_usage_dict:
      for command in self.bot.commands:
        if command.cog.qualified_name not in self.command_usage_dict:
          self.command_usage_dict[command.cog.qualified_name] = command.usage
        else:
          self.command_usage_dict[command.cog.qualified_name] += '\n{0}'.format(command.usage)
      for cog_name, usage in self.command_usage_dict.items():
        self.command_usage_dict[cog_name] = '```ini\n{0}\n```'.format(usage)

  async def celi_digamma_check(ctx):
    if ctx.author.id not in [CELI_ID, DIGAMMA_ID]:
      raise commands.CommandError(message='You are not allowed to access this command.')
    return True

  async def set_playing_check(ctx):
    args = ctx.message.content.split()[1:]
    if not args:
      raise commands.CommandError(message='Missing input to set as playing.')
    return True

  @commands.command(
    description='Set the playing status of the bot.',
    usage='setplaying [STRING]',
    checks=[celi_digamma_check, set_playing_check]
  )
  async def setplaying(self, ctx, *args):
    s = ' '.join(args)
    await discord.Client.change_presence(self=self.bot, activity=discord.Game(name=s))

  @commands.command(
    description='Get the Velvet no... image.',
    usage='no'
  )
  async def no(self, ctx, *args):
    folder = os.path.dirname(os.path.realpath('__file__'))
    await ctx.send(file=discord.File(os.path.join(folder, 'assets/no.png')))

  @commands.command(
    description='Say bye.',
    usage='adios'
  )
  async def adios(self, ctx, *args):
    folder = os.path.dirname(os.path.realpath('__file__'))
    await ctx.send(file=discord.File(os.path.join(folder, 'assets/adios.png')))

  @commands.command(
    description='Get the help message with proper usage instructions.',
    usage='help [optional COMMAND]'
  )
  async def help(self, ctx, *args):
    if args:
      self.init_command_description_dict()
      query = ' '.join(args)
      try:
        description = self.command_description_dict[query]
        await ctx.send(description)
      except KeyError:
        await ctx.send('There is no command called {0}.'.format(query))
    else:
      self.init_command_usage_dict()
      await ctx.send(embed=make_help_embed(self.command_usage_dict))

  @commands.Cog.listener()
  async def on_message(self, message):
    if 'dying is unhealthy' in message.content.lower():
      folder = os.path.dirname(os.path.realpath('__file__'))
      channel = discord.Client.get_channel(self=self.bot, id=message.channel.id)
      await channel.send(file=discord.File(os.path.join(folder, 'assets/no.png')))

  @commands.Cog.listener()
  async def on_member_join(self, member):
    if member.guild.id == TWO_MF_GUILD_ID:
      channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
      await channel.send("Welcome {0}!\nUse the commands {1}gamerole and {1}locationrole to give yourself roles.".format(member.name, PREFIX))
