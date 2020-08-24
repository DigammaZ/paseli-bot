import discord
from discord.ext import commands

from services.sdvx_service import grind19

class Sdvx(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    description='Grind an SDVX song.',
    usage='grind'
  )
  async def grind(self, ctx, level: int = 19):
    if level == 19:
      await ctx.send('Go play {0}.'.format(grind19()))
