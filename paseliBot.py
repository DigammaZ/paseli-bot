from discord.ext import commands
from grind19 import grind19
from jisho import search_jisho
from discordCredentials import *
from remind import poll, attempt_create_remind
import discord
import json
import re
import os

bot = commands.Bot('!')

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
  await poll(bot)

@bot.command(pass_context=True)
async def balance(ctx):
  id = ctx.message.author.id
  if id in amounts:
    amount = amounts[id]
    await bot.say('You have {0} WHOLE PASELI! That\'s, like, {1} x 5 Paseli!'.format(amount, amount/5))
  else:
    await bot.say('You do not have a Paseli account.')

@bot.command(pass_context=True)
async def register(ctx, user: discord.Member = None):
  # Register for the 2MF Paseli System
  if user is None:
    id = ctx.message.author.id
  else:
    id = user.id

  if id not in amounts:
    amounts[id] = 100
    await bot.say('User is now registered in the Paseli Database!')
    _save()
  else:
    await bot.say('User already has a Paseli account.')


@bot.command(pass_context=True)
async def give(ctx, amount: int, other_user: discord.Member):
  primary_id = ctx.message.author.id
  other_id = other_user.id
  if amount < 0:
    await bot.say('Please do not steal Paseli.')
    return
  if primary_id is other_id:
    if primary_id == DIGAMMA:
      amounts[primary_id] += amount
      await bot.say('Tax fraud complete!')
    return

  if primary_id not in amounts:
    await bot.say('You do not have a Paseli account.')
  elif other_id not in amounts:
    await bot.say('The other party does not have a Paseli account.')
  elif amounts[primary_id] < amount:
    await bot.say('Insufficient Paseli, find a Recharge Kiosk.')
  else:
    amounts[primary_id] -= amount
    amounts[other_id] += amount
    await bot.say('{0} has been given {1} WHOLE PASELI!'.format(other_user.mention, amount))
    _save()

@bot.command(pass_context=True)
async def grind(ctx, level: int = 19):
  if level == 19:
    await bot.say('Go play {0}.'.format(grind19()))

@bot.command(pass_context=True)
async def jisho(ctx, *args):
  if not args:
    await bot.say('You cannot query nothing.')
  else:
    query = ' '.join(args)
    output = search_jisho(query)
    await bot.say(output)

@bot.command(pass_context=True)
async def remind(ctx, *args):
  regex = re.search('^[0-9]*[0-9]:[0-9][0-9] [AaPp][Mm] ', ' '.join(args))
  if not regex:
    await bot.say('Usage: `::remind <HH:MM> <AM/PM> <msg>`')
  else:
    try:
      output = attempt_create_remind(ctx=ctx, hour_min=args[0], am_pm=args[1], msg=' '.join(args[2:]))
      await bot.say(output)
    except ValueError as e:
      await bot.say(e)

@bot.command(pass_context=True)
async def no(ctx, *args):
  folder = os.path.dirname(os.path.realpath('__file__'))
  await bot.send_file(ctx.message.channel, os.path.join(folder, 'no.png'))

@bot.event
async def on_message(message):
  if message.content.lower() == 'dying is unhealthy':
    folder = os.path.dirname(os.path.realpath('__file__'))
    await bot.send_file(message.channel, os.path.join(folder, 'no.png'))

def _save():
  with open('amounts.json', 'w+') as f:
    json.dump(amounts, f)

@bot.command()
async def save():
  _save()

bot.run(TOKEN)