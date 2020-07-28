from discord.ext import commands
from grind19 import grind19
from jisho import search_jisho
from discordCredentials import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from remind import attempt_create_remind, send_and_delete_reminds
import discord
import json
import re
import os

bot = commands.Bot('!')
scheduler = AsyncIOScheduler(daemon=True)

amounts = {}

@bot.event
async def on_ready():
  global amounts
  try:
    with open('amounts.json') as f:             
      amounts = json.load(f)
  except FileNotFoundError:
    print('Could not load `amounts.json`.')
    amounts = {}
  scheduler.add_job(func=send_and_delete_reminds, trigger='cron', args=[bot], max_instances=1, second=0)
  scheduler.start()

@bot.command()
async def balance(ctx):
  id = ctx.message.author.id
  if id in amounts:
    amount = amounts[id]
    await ctx.send('You have {0} WHOLE PASELI! That\'s, like, {1} x 5 Paseli!'.format(amount, amount/5))
  else:
    await ctx.send('You do not have a Paseli account.')

@bot.command()
async def register(ctx, user: discord.Member = None):
  # Register for the 2MF Paseli System
  if user is None:
    id = ctx.message.author.id
  else:
    id = user.id

  if id not in amounts:
    amounts[id] = 100
    await ctx.send('User is now registered in the Paseli Database!')
    _save()
  else:
    await ctx.send('User already has a Paseli account.')


@bot.command()
async def give(ctx, amount: int, other_user: discord.Member):
  primary_id = ctx.message.author.id
  other_id = other_user.id
  if amount < 0:
    await ctx.send('Please do not steal Paseli.')
    return
  if primary_id is other_id:
    if primary_id == DIGAMMA:
      amounts[primary_id] += amount
      await ctx.send('Tax fraud complete!')
    return

  if primary_id not in amounts:
    await ctx.send('You do not have a Paseli account.')
  elif other_id not in amounts:
    await ctx.send('The other party does not have a Paseli account.')
  elif amounts[primary_id] < amount:
    await ctx.send('Insufficient Paseli, find a Recharge Kiosk.')
  else:
    amounts[primary_id] -= amount
    amounts[other_id] += amount
    await ctx.send('{0} has been given {1} WHOLE PASELI!'.format(other_user.mention, amount))
    _save()

@bot.command()
async def grind(ctx, level: int = 19):
  if level == 19:
    await ctx.send('Go play {0}.'.format(grind19()))

@bot.command()
async def jisho(ctx, *args):
  if not args:
    await ctx.send('You cannot query nothing.')
  else:
    query = ' '.join(args)
    output = search_jisho(query)
    await ctx.send(output)

@bot.command()
async def remind(ctx, *args):
  regex = re.search('^[0-9]*[0-9]:[0-9][0-9] [AaPp][Mm] ', ' '.join(args))
  if not regex:
    await ctx.send('Usage: `::remind <HH:MM> <AM/PM> <msg>`')
  else:
    try:
      output = attempt_create_remind(ctx=ctx, hour_min=args[0], am_pm=args[1], msg=' '.join(args[2:]))
      await ctx.send(output)
    except ValueError as e:
      await ctx.send(e)

@bot.command()
async def no(ctx, *args):
  folder = os.path.dirname(os.path.realpath('__file__'))
  await ctx.send(file=discord.File(os.path.join(folder, 'no.png')))

@bot.event
async def on_message(message):
  if message.content.lower() == 'dying is unhealthy':
    folder = os.path.dirname(os.path.realpath('__file__'))
    channel = discord.Client.get_channel(self=bot, id=message.channel.id)
    await channel.send(file=discord.File(os.path.join(folder, 'no.png')))
  await bot.process_commands(message)

def _save():
  with open('amounts.json', 'w+') as f:
    json.dump(amounts, f)

@bot.command()
async def save():
  _save()

bot.run(TOKEN)