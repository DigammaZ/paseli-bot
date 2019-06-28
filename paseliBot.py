from discord.ext import commands
from grind19 import grind19
import discord
import json

TOKEN = 'Token'


bot = commands.Bot('!')

amounts = {}

@bot.event
async def on_ready():
    global amounts
    try:
        with open('amounts.json') as f:             
            amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        amounts = {}

@bot.command(pass_context=True)
async def balance(ctx):
    id = ctx.message.author.id
    if id in amounts:
        amount = amounts[id]
        await bot.say("You have " + str(amount) + " WHOLE PASELI! That's, like, " + str(amount/5) +"x 5 Paseli!")
    else:
        await bot.say("You do not have a Paseli account.")

@bot.command(pass_context=True)
async def register(ctx, user: discord.Member = None):
    # Register for the 2MF Paseli System
    if user is None:
        id = ctx.message.author.id
    else:
        id = user.id

    if id not in amounts:
        amounts[id] = 100
        await bot.say("User is now registered in the Paseli Database!")
        _save()
    else:
        await bot.say("User already has a Paseli account.")


@bot.command(pass_context=True)
async def give(ctx, amount: int, otherUser: discord.Member):
    primary_id = ctx.message.author.id
    other_id = otherUser.id
    if amount < 0:
        await bot.say("Please do not steal Paseli")
        return
    if primary_id is other_id:
        if int(primary_id) == 191639004221931525:
            amounts[primary_id] += amount
            await bot.say("Tax fraud complete!")
        return

    if primary_id not in amounts:
        await bot.say("You do not have a Paseli account")
        return
    elif other_id not in amounts:
        await bot.say("The other party does not have a Paseli account")
        return
    elif amounts[primary_id] < amount:
        await bot.say("Insufficient Paseli, find a Recharge Kiosk")
        return
    else:
        amounts[primary_id] -= amount
        amounts[other_id] += amount
        await bot.say(otherUser.mention+" has been given "+str(amount) + " WHOLE PASELI!")
    _save()

@bot.command(pass_context=True)
async def grind(ctx,level: int = 19):
    if level == 19:
        song = grind19()
        song = "".join(song)
        await bot.say("Go play "+song)

def _save():
    with open('amounts.json', 'w+') as f:
        json.dump(amounts, f)

@bot.command()
async def save():
    _save()

bot.run(TOKEN)