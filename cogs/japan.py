import discord
from discord.ext import commands

from services.jisho_service import search_jisho
from services.time_service import get_current_japan_time

JISHO_USAGE_MSG = 'You cannot query nothing.'

class Japan(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def jisho(self, ctx, *args):
    if not args:
      await ctx.send(JISHO_USAGE_MSG)
    else:
      query = ' '.join(args)
      output = search_jisho(query)
      await ctx.send(output)

  @commands.command()
  async def jst(self, ctx):
    await ctx.send(':japan: {0}'.format(get_current_japan_time()))
