import discord
from discord.ext import commands

from services.jisho_service import search_jisho
from services.time_service import get_current_japan_time

class Japan(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def jisho_check(ctx):
    args = ctx.message.content.split()[1:]
    if not args:
      raise commands.CommandError(message='Missing input to search Jisho.')
    return True

  @commands.command(
    description='Search jisho for a translation. Input can be Japanese or English.',
    usage='jisho [SEARCH TERM]',
    checks=[jisho_check]
  )
  async def jisho(self, ctx, *args):
    query = ' '.join(args)
    output = search_jisho(query)
    await ctx.send(output)

  @commands.command(
    description='Get the current time in Japan.',
    usage='jst'
  )
  async def jst(self, ctx):
    await ctx.send(':japan: {0}'.format(get_current_japan_time()))
