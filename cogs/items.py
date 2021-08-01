from discord.ext import commands, tasks
from discord.utils import *
import discord 
import __main__
import random

from discord_components import *


#
# This cog both serves as the cog for the shop functions 
#


class Items(commands.Cog):
    def __init__(self, client):
        self.client = client

        global emojis
        emojis = self.client.custom_emojis


    global settings
    #settings = __main__.game_settings['cogs']['shop']

    global items  
    items = __main__.items

    global admins
    admins = __main__.game_settings['game_masters']

    global stat_strings
    stat_strings = {
        "min_power": "Minimum Power",
        "max_power": "Maximum Power",
        "cooldown":  "Cooldown",
        "type_yield": "Ore Yield"
    }

    def construct_item_stats_string(self, item):
        global stat_strings
        try:
            item = items[item]
        except:
            return False    

        string = ""
        for stat in item['base_stats']:
            string += f"{stat_strings[stat]}: {item['base_stats'][stat]} \n"

        return string

    @commands.command()
    async def createitem(self, ctx, name_id, category="", type="", rarity=""):
        global admins
        if ctx.author.id in admins:

            base_stats = {}

            if str(type).lower() == "pickaxe":
                base_stats = {
                    "min_power": 0,
                    "max_power": 1,
                    "cooldown": 60,
                    "type_yield": 1
                }

            new_item = {
                "name": "",
                "flavor": "",
                "category": category,
                "type": type,
                "rarity": rarity,
                "base_stats" : base_stats,
                "mod_range": {"-1": 10, "0": 50, "1": 20, "2": 10, "3": 10},  # Weights
                "value": 100
            }

            items[name_id] = new_item
            __main__.save_json(f"{__main__.configspath}/item_settings.json", items)

            await ctx.send(f"Item has been succesfully created. Finish configuring it at {__main__.configspath}/item_settings.json \n\nAfterward, restart the bot to ensure it processes the changes.")
            return
        else:
            await ctx.send(f"You don't have permission to do this.")
        


def setup(client):
    client.add_cog(Items(client))