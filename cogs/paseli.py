import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from random import randint
import re

from constants import CELI_ID, DIGAMMA_ID

from serializers.daily_done_serializer import get_daily_done

from services.db_service import delete_daily_done, insert_daily_done
from services.paseli_service import get_amounts, save


async def amounts_check(ctx):
  try:
    get_amounts()
  except FileNotFoundError:
    ctx.send('Could not load `amounts.json`.')


async def balance_check(ctx):
  amounts = get_amounts()
  user_id = str(ctx.message.author.id)
  if user_id not in amounts:
    raise commands.CommandError(message='You do not have a Paseli account.')
  return True


async def registered_check(ctx):
  amounts = get_amounts()
  user_id = str(ctx.message.author.id)
  if user_id in amounts:
    raise commands.CommandError(message='You already have a Paseli account.')
  return True


async def give_check(ctx):
  split = ctx.message.content.split()
  try:
    int(split[1])
  except ValueError:
    raise commands.CommandError('You must input an integer for the amount.')
  regex = re.search('<@!*[0-9]+>', split[2])
  if not regex:
    raise commands.CommandError('You must @ another user.')
  return True


async def digamma_take_check(ctx):
  user_id = ctx.message.author.id
  if user_id != DIGAMMA_ID:
    raise commands.CommandError(message='You are not allowed to take Paseli.')
  return True


async def daily_done_check(ctx):
  user_id = str(ctx.message.author.id)
  if get_daily_done(user_id):
    raise commands.CommandError(message='You\'ve already redeemed your daily Paseli.')
  return True


class Paseli(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.sched = AsyncIOScheduler(daemon=True)
    self.sched.add_job(func=delete_daily_done, trigger='cron', max_instances=1, hour=0)
    self.sched.start()

  @commands.command(
    description='Check your Paseli balance.',
    usage='balance',
    checks=[amounts_check, balance_check]
  )
  async def balance(self, ctx):
    user_id, amounts = str(ctx.message.author.id), get_amounts()
    amount, divisor = amounts[user_id], randint(1, 10)
    await ctx.send('You have {0} WHOLE PASELI! That\'s, like, {1} x {2} Paseli!'.format(amount, round(amount / divisor,
                                                                                                      2), divisor))

  @commands.command(
    description='Register for a Paseli account.',
    usage='register',
    checks=[amounts_check, registered_check]
  )
  async def register(self, ctx):
    user_id, amounts = str(ctx.message.author.id), get_amounts()
    amounts[user_id] = 100
    await ctx.send('User is now registered in the Paseli Database!')
    save(amounts)

  @commands.command(
    description='Give Paseli to another registered user.',
    usage='give [AMOUNT] [@RECIPIENT]',
    checks=[amounts_check, balance_check, give_check]
  )
  async def give(self, ctx, amount: int, other_user: discord.Member):
    primary_id, other_id = str(ctx.message.author.id), str(other_user.id)
    amounts = get_amounts()
    if amount < 0:
      await ctx.send('Please do not steal Paseli.')
    elif primary_id == other_id:
      if primary_id == str(CELI_ID) or primary_id == str(DIGAMMA_ID):
        amounts[primary_id] += amount
        await ctx.send('Tax fraud complete!')
        save(amounts)
      else:
        await ctx.send('You are not allowed to commit tax fraud.')
    elif other_id not in amounts:
      await ctx.send('The other party does not have a Paseli account.')
    elif amounts[primary_id] < amount:
      await ctx.send('Insufficient Paseli, find a Recharge Kiosk.')
    else:
      amounts[primary_id] -= amount
      amounts[other_id] += amount
      await ctx.send('{0} has been given {1} WHOLE PASELI!'.format(other_user.mention, amount))
      save(amounts)

  @commands.command(
    description='Take Paseli from another registered user. Only for Robbie.',
    usage='take [AMOUNT] [@VICTIM]',
    checks=[amounts_check, balance_check, give_check, digamma_take_check]
  )
  async def take(self, ctx, amount: int, other_user: discord.Member):
    primary_id, other_id = str(ctx.message.author.id), str(other_user.id)
    amounts = get_amounts()
    if amount < 0:
      await ctx.send('use the give command lmao')
    elif primary_id == other_id:
      await ctx.send('what no')
    elif other_id not in amounts:
      await ctx.send('The other party does not have a Paseli account.')
    else:
      if amount > amounts[other_id]:
        await ctx.send('{0} WHOLE PASELI has been stolen from {1}!'.format(amounts[other_id], other_user.mention))
        amounts[primary_id] += amounts[other_id]
        amounts[other_id] = 0
      else:
        await ctx.send('{0} WHOLE PASELI has been stolen from {1}!'.format(amount, other_user.mention))
        amounts[primary_id] += amount
        amounts[other_id] -= amount
      save(amounts)

  @commands.command(
    description='Get 5 Paseli daily.',
    usage='daily',
    checks=[amounts_check, balance_check, daily_done_check]
  )
  async def daily(self, ctx):
    primary_id = str(ctx.message.author.id)
    amounts = get_amounts()
    await ctx.send('You gained 5 WHOLE PASELI.')
    amounts[primary_id] += 5
    insert_daily_done(primary_id)
    save(amounts)
