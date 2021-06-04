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

  async def temp_check(ctx):
    args = ctx.message.content.split()[1:]
    if not args:
      raise commands.CommandError(message='Missing input for temperature conversion.')
    try:
      float(args[0])
    except ValueError:
      raise commands.CommandError(message='Input must be a number.')
    return True

  @commands.command(
    description='Convert a temperature in Celsius to Fahrenheit.',
    usage='c2f [temperature in C]',
    checks=[temp_check]
  )
  async def c2f(self, ctx, *args):
    temp_in_c = float(args[0])
    temp_in_f = temp_in_c * 1.8 + 32
    await ctx.send('{0} °F'.format(round(temp_in_f, 2)))

  @commands.command(
    description='Convert a temperature in Fahrenheit to Celsius.',
    usage='f2c [temperature in F]',
    checks=[temp_check]
  )
  async def f2c(self, ctx, *args):
    temp_in_f = float(args[0])
    temp_in_c = (temp_in_f - 32) / 1.8
    await ctx.send('{0} °C'.format(round(temp_in_c, 2)))
