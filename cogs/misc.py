import discord
from discord.ext import commands
import os

from constants import CELI_ID, DIGAMMA_ID

from services.embed_service import make_help_embed

HELP_PASELI_TITLE = 'Paseli'
HELP_PASELI_VALUE = ("```ini\n"
                   "balance\n"
                   "register\n"
                   "give [AMOUNT] [RECIPIENT]\n"
                   "```")

HELP_SDVX_TITLE = 'SDVX'
HELP_SDVX_VALUE = ("```ini\n"
                   "grind\n"
                   "```")


HELP_JAPAN_TITLE = 'Japan'
HELP_JAPAN_VALUE = ("```ini\n"
                   "jisho [SEARCH TERM]\n"
                   "jst\n"
                   "```")

HELP_REMIND_TITLE = 'Remind'
HELP_REMIND_VALUE = ("```ini\n"
                   "remind HH:MM [AM/PM] [MESSAGE]\n"
                   "show\n"
                   "```")

HELP_MISC_TITLE = 'Miscellaneous'
HELP_MISC_VALUE = ("```ini\n"
                   "no\n"
                   "```")

class Miscellaneous(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.remove_command('help')

  @commands.command()
  async def setplaying(self, ctx, *args):
    if args and ctx.author.id == CELI_ID or DIGAMMA_ID:
      s = ' '.join(args)
      await discord.Client.change_presence(self=self.bot, activity=discord.Game(name=s))

  @commands.command()
  async def no(self, ctx, *args):
    folder = os.path.dirname(os.path.realpath('__file__'))
    await ctx.send(file=discord.File(os.path.join(folder, 'assets/no.png')))

  @commands.command()
  async def help(self, ctx, *args):
    await ctx.send(embed=make_help_embed({
      HELP_PASELI_TITLE: HELP_PASELI_VALUE,
      HELP_SDVX_TITLE: HELP_SDVX_VALUE,
      HELP_REMIND_TITLE: HELP_REMIND_VALUE,
      HELP_JAPAN_TITLE: HELP_JAPAN_VALUE,
      HELP_MISC_TITLE: HELP_MISC_VALUE
    }))

  @commands.Cog.listener()
  async def on_message(self, message):
    if 'dying is unhealthy' in message.content.lower():
      folder = os.path.dirname(os.path.realpath('__file__'))
      channel = discord.Client.get_channel(self=self.bot, id=message.channel.id)
      await channel.send(file=discord.File(os.path.join(folder, 'assets/no.png')))
