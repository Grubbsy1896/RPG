from discord.ext import commands, tasks
from discord.utils import *
import discord 
import __main__
import random

from discord_components import *


#
# This cog both serves as the cog for the shop functions 
#


class Shop(commands.Cog):
    def __init__(self, client):
        self.client = client

        global emojis
        emojis = self.client.custom_emojis


    #global settings
    #settings = __main__.game_settings['cogs']['shop']

    global shops
    shops = __main__.shops

    global items 
    items = __main__.items

    def shop_menu(self):
        global shops
        #Button(style=ButtonStyle.green, label="Materials", custom_id="materials"

        buttons = [[], [], [], [], []]

        embed = discord.Embed(title="Shops")

        for shop in shops:

            # we need to create an embed field, and a button.

            embed.add_field(name=f"{shops[shop]['name']}", value=f"{shops[shop]['description']}")

            # adding button
            if len(buttons[0]) < 5:
                buttons[0].append(Button(style=ButtonStyle.gray, label=f"{shops[shop]['name']}", custom_id=f"menu{shop}"))
            elif len(buttons[1]) < 5:
                buttons[1].append(Button(label=f"{shops[shop]['name']}", custom_id=f"menu{shops[shop]['name']}"))
            elif len(buttons[2]) < 5:
                buttons[2].append(Button(label=f"{shops[shop]['name']}", custom_id=f"menu{shops[shop]['name']}"))

        print("BEFORE", buttons)
        for i in range(0, len(buttons)):
            try:
                buttons.remove([])
            except:
                pass

        return [embed, buttons]

    def shop_menu_2(self, shop):
        store = str(shop).replace("menu", "")
        print(store, shops)
        if store in shops:
            store_items = shops[store]['items']
            item_list = []

            embed = discord.Embed(title=f"{shops[store]['name']}")
            Items = self.client.get_cog("Items")
            for i in store_items:
                embed.add_field(name=f"{items[i]['name']}", value=f"{store_items[i]['price']} {self.client.currency} \n{items[i]['flavor']} \n**Stats**: \n {Items.construct_item_stats_string(i)}")
                item_list.append(SelectOption(label=f"{items[i]['name']}", description=f"{store_items[i]['price']} {self.client.currency}", value=i))
            menu = Select(options=item_list)

            

            return [embed, menu]

    @commands.command()
    async def shop(self, ctx):

        data = self.shop_menu()
        print(data)
        await ctx.send(content = "Shop", embed=data[0], components=data[1])


    @commands.Cog.listener()
    async def on_button_click(self, interaction: Interaction):
        global shops
        global items
        #print(interaction.__dict__)
        player = __main__.get_player("", interaction.user.id, interaction.user.name)

        if str(interaction.custom_id).startswith("menu"):

            message = self.shop_menu_2(interaction.custom_id)

            await interaction.respond(type=4, embed=message[0], components=[message[1]])
            # name = interaction.component[0].


def setup(client):
    client.add_cog(Shop(client))