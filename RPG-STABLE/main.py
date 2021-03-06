# July 18th 2021
# The RPG Bot
# main.py is the file in which everything will go to. it being the one file that will be run.

# --
# > Imports
# --

# Import Everything From Discord
import discord

from discord.ext import commands
from discord.ext import tasks, commands
from discord.ext.commands.bot import Bot
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions
from discord_components import DiscordComponents, Button, ButtonStyle

# General Imports 
import sys
import os
import asyncio
import random
import datetime

from random import randint
from datetime import date

# Import from other files
from configuration import * # bot_settings, print_players
from data import *
from player import *

# --
# > Declaring Variables
# --

# Setting up bot
token = bot_settings['token']
client = commands.Bot(command_prefix=bot_settings['prefix'])

# Declaring Globals

client.players = {}

client.custom_emojis = emojis

client.game_settings = game_settings

client.currency = str(game_settings['currency_name'])

###
### Confining Certain Cog Settings to a smaller variable to make them easier to use.
### -- -- This will be used in the base file for base cogs only. I hope that
### -- -- cogs added in the future will have their own config file. (Modded-in Cogs) 

# --
# > Functions
# --

def get_player(ctx, id=0, name=0):  # This 
    if id == name:
        id = ctx.author.id
        name = ctx.author.name
    else:
        pass
    #print(client.players)
    id = str(id)
    if id not in client.players:
        #print("Not found in _players, creating data.")
        data = None
        try:
            data = load_player(id)
            #print(data)
        except:
            pass

        if data:
            client.players[id] = Player(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12]) # Loading it
        else:
            client.players[id] = Player(id, name) # Creating it

    #print(client.players)
    return client.players[id]

# --
# > Commands
# --

@client.command()
async def test(ctx):
    # player = get_player(ctx)
    # player.cash += 1
    # await ctx.send(f"{player.name}: cash {player.cash}")
    # player.save_data()
    string = ""
    for command in client.commands:
        string += f"{command.name}, aliases: {command.aliases}"


# --
# > Events
# --

@client.event
async def on_ready(): # When the bot connects to discord it prints the following message.
    print(f"{client.user} has connected to discord.")
    DiscordComponents(client)


    # https://stackoverflow.com/questions/151199/how-to-calculate-number-of-days-between-two-given-dates
    day = date.today()
    d0 = date(2021, 7, 18)
    d1 = date(day.year, day.month, day.day)
    delta = d1 - d0
    days_since = delta.days

    await client.change_presence(activity=discord.Game(name=f"Day {days_since} of Development"))

# Running the bot.

client.load_extension("cogs.character") # "cogs.mine", 
client.load_extension("cogs.mine")
client.load_extension("cogs.items")
client.load_extension("cogs.shop")
client.run(token)    