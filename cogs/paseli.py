import discord
from discord.ext import commands
import json
from random import randint

from constants import CELI_ID, DIGAMMA_ID

NO_PASELI_ACCOUNT = 'You do not have a Paseli account.'
USER_REGISTERED_SUCCESS = 'User is now registered in the Paseli Database!'
USER_ALREADY_REGISTERED = 'User already has a Paseli account.'
DO_NOT_STEAL_PASELI = 'Please do not steal Paseli.'
TAX_FRAUD_SUCCESS = 'Tax fraud complete!'
TAX_FRAUD_FAILURE = 'You are not allowed to commit tax fraud.'
OTHER_PARTY_NO_PASELI_ACCOUNT = 'The other party does not have a Paseli account.'
INSUFFICIENT_FUNDS = 'Insufficient Paseli, find a Recharge Kiosk.'

class Paseli(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    try:
      with open('amounts.json') as f:
        self.amounts = json.load(f)
    except FileNotFoundError:
      print('Could not load `amounts.json`.')
      self.amounts = {}

  def save(self):
    with open('amounts.json', 'w+') as f:
      json.dump(self.amounts, f)

  @commands.command()
  async def balance(self, ctx):
    user_id = str(ctx.message.author.id)
    if user_id in self.amounts:
      amount = self.amounts[user_id]
      divisor = randint(1, 10)
      await ctx.send('You have {0} WHOLE PASELI! That\'s, like, {1} x {2} Paseli!'.format(amount, round(amount/divisor, 2), divisor))
    else:
      await ctx.send(NO_PASELI_ACCOUNT)

  @commands.command()
  async def register(self, ctx):
    user_id = str(ctx.message.author.id)
    if user_id not in self.amounts:
      self.amounts[user_id] = 100
      await ctx.send(USER_REGISTERED_SUCCESS)
      self.save()
    else:
      await ctx.send(USER_ALREADY_REGISTERED)

  @commands.command()
  async def give(self, ctx, amount: int, other_user: discord.Member):
    primary_id = str(ctx.message.author.id)
    other_id = str(other_user.id)
    if amount < 0:
      await ctx.send(DO_NOT_STEAL_PASELI)
      return

    if primary_id == other_id:
      if primary_id == str(CELI_ID) or primary_id == str(DIGAMMA_ID):
        self.amounts[primary_id] += amount
        await ctx.send(TAX_FRAUD_SUCCESS)
        self.save()
      else:
        await ctx.send(TAX_FRAUD_FAILURE)
      return

    if primary_id not in self.amounts:
      await ctx.send(NO_PASELI_ACCOUNT)
    elif other_id not in self.amounts:
      await ctx.send(OTHER_PARTY_NO_PASELI_ACCOUNT)
    elif self.amounts[primary_id] < amount:
      await ctx.send(INSUFFICIENT_FUNDS)
    else:
      self.amounts[primary_id] -= amount
      self.amounts[other_id] += amount
      await ctx.send('{0} has been given {1} WHOLE PASELI!'.format(other_user.mention, amount))
      self.save()
