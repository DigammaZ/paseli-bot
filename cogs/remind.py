import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import re

from serializers.remind_serializer import get_reminds

from services.db_service import delete_remind
from services.embed_service import make_remind_embed
from services.remind_service import create_remind, send_and_delete_reminds


class Remind(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.reminds = {}
    self.sched = AsyncIOScheduler(daemon=True)
    self.sched.add_job(func=send_and_delete_reminds, trigger='cron', args=[self.bot], max_instances=1, second=0)
    self.sched.start()

  async def remind_check(ctx):
    args = ' '.join(ctx.message.content.split()[1:])
    regex = re.search('^[0-9]*[0-9]:[0-9][0-9] [AaPp][Mm] [\w]', args)
    if not regex:
      raise commands.CommandError('Remind creation syntax is incorrect.')
    return True

  @commands.command(
    description='Set a remind up to 24 hours in the future.',
    usage='remind [HH:MM] [AM/PM] [MESSAGE]',
    checks=[remind_check]
  )
  async def remind(self, ctx, *args):
    await ctx.send(create_remind(ctx, args[0], args[1], ' '.join(args[2:len(args)])))

  async def process_remind_response(self, ctx, response):
    choice = response.content
    if choice == '0':
      await self.process_delete(ctx)

  async def process_delete(self, ctx):
    def delete_remind_check(msg):
      return msg.channel == ctx.channel and msg.author == ctx.author and msg.content.isdigit()

    delete_message = await ctx.send('Choose the number of the remind you want to delete.')
    delete_choice = await discord.Client.wait_for(self=self.bot, event='message', timeout=10, check=delete_remind_check)
    remind = self.reminds[ctx.message.author.id][int(delete_choice.content) - 1]
    delete_remind(remind['requested_time'], remind['channel_id'], remind['user_id'], remind['message'],
                  remind['guild_id'])
    await delete_message.delete()
    await delete_choice.delete()
    await ctx.send('Remind with message `{0}` deleted.'.format(remind['message']))

  @commands.command(
    description='Manage reminds.',
    usage='show'
  )
  async def show(self, ctx):
    reminds = get_reminds(user_id=ctx.author.id, guild_id=ctx.guild.id)
    if not reminds:
      await ctx.send('You have no reminds.')
      return
    self.reminds[ctx.message.author.id] = reminds

    def remind_option_check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel and msg.content in ['0', '1']

    embed = await ctx.send(embed=make_remind_embed(reminds))
    response = await discord.Client.wait_for(self=self.bot, event='message', timeout=30, check=remind_option_check)
    while response:
      await response.delete()
      await self.process_remind_response(ctx, response)
      reminds = get_reminds(user_id=ctx.author.id, guild_id=ctx.guild.id)
      if not reminds:
        await embed.delete()
        await ctx.send('You have no reminds remaining.')
        return
      self.reminds[ctx.message.author.id] = reminds
      await embed.edit(embed=make_remind_embed(reminds))
      response = await discord.Client.wait_for(self=self.bot, event='message', timeout=30, check=remind_option_check)
