import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
from random import randint
import re

from constants import CELI_ID, DIGAMMA_ID

class Paseli(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.daily_done = set([])
    self.sched = AsyncIOScheduler(daemon=True)
    self.sched.add_job(func=self.reset_daily, trigger='cron', max_instances=1, hour=0)
    self.sched.start()
    try:
      with open('amounts.json') as f:
        self.amounts = json.load(f)
    except FileNotFoundError:
      print('Could not load `amounts.json`.')
      self.amounts = {}

  def save(self):
    with open('amounts.json', 'w+') as f:
      json.dump(self.amounts, f)

  def reset_daily(self):
    self.daily_done = set([])

  @commands.command(
    description='Check your Paseli balance.',
    usage='balance'
  )
  async def balance(self, ctx):
    user_id = str(ctx.message.author.id)
    if user_id in self.amounts:
      amount = self.amounts[user_id]
      divisor = randint(1, 10)
      await ctx.send('You have {0} WHOLE PASELI! That\'s, like, {1} x {2} Paseli!'.format(amount, round(amount/divisor, 2), divisor))
    else:
      await ctx.send('You do not have a Paseli account.')

  @commands.command(
    description='Register for a Paseli account.',
    usage='register'
  )
  async def register(self, ctx):
    user_id = str(ctx.message.author.id)
    if user_id not in self.amounts:
      self.amounts[user_id] = 100
      await ctx.send('User is now registered in the Paseli Database!')
      self.save()
    else:
      await ctx.send('User already has a Paseli account.')

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

  @commands.command(
    description='Give Paseli to another registered user.',
    usage='give [AMOUNT] [@RECIPIENT]',
    checks=[give_check]
  )
  async def give(self, ctx, amount: int, other_user: discord.Member):
    primary_id = str(ctx.message.author.id)
    other_id = str(other_user.id)
    if amount < 0:
      await ctx.send('Please do not steal Paseli.')
    elif primary_id == other_id:
      if primary_id == str(CELI_ID) or primary_id == str(DIGAMMA_ID):
        self.amounts[primary_id] += amount
        await ctx.send('Tax fraud complete!')
        self.save()
      else:
        await ctx.send('You are not allowed to commit tax fraud.')
    elif primary_id not in self.amounts:
      await ctx.send('You do not have a Paseli account.')
    elif other_id not in self.amounts:
      await ctx.send('The other party does not have a Paseli account.')
    elif self.amounts[primary_id] < amount:
      await ctx.send('Insufficient Paseli, find a Recharge Kiosk.')
    else:
      self.amounts[primary_id] -= amount
      self.amounts[other_id] += amount
      await ctx.send('{0} has been given {1} WHOLE PASELI!'.format(other_user.mention, amount))
      self.save()

  @commands.command(
    description='Take Paseli from another registered user. Only for Robbie.',
    usage='take [AMOUNT] [@VICTIM]',
    checks=[give_check]
  )
  async def take(self, ctx, amount: int, other_user: discord.Member):
    primary_id = str(ctx.message.author.id)
    other_id = str(other_user.id)
    if primary_id != str(DIGAMMA_ID):
      await ctx.send('You are not allowed to take Paseli.')
    elif amount < 0:
      await ctx.send('use the give command lmao')
    elif primary_id == other_id:
        await ctx.send('what no')
    elif primary_id not in self.amounts:
      await ctx.send('You do not have a Paseli account.')
    elif other_id not in self.amounts:
      await ctx.send('The other party does not have a Paseli account.')
    else:
      if amount > self.amounts[other_id]:
        await ctx.send('{0} WHOLE PASELI has been stolen from {1}!'.format(self.amounts[other_id], other_user.mention))
        self.amounts[primary_id] += self.amounts[other_id]
        self.amounts[other_id] = 0
      else:
        await ctx.send('{0} WHOLE PASELI has been stolen from {1}!'.format(amount, other_user.mention))
        self.amounts[primary_id] += amount
        self.amounts[other_id] -= amount
      self.save()

  @commands.command(
    description='Get 5 Paseli daily.',
    usage='daily'
  )
  async def daily(self, ctx):
    primary_id = str(ctx.message.author.id)
    if primary_id not in self.amounts:
      await ctx.send('You do not have a Paseli account.')
    elif primary_id not in self.daily_done:
      await ctx.send('You gained 5 WHOLE PASELI.')
      self.amounts[primary_id] += 5
      self.daily_done.add(primary_id)
      self.save()
    else:
      await ctx.send('You\'ve already redeemed your daily Paseli.')
