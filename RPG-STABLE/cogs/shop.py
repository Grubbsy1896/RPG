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

        #print("BEFORE", buttons)
        for i in range(0, len(buttons)):
            try:
                buttons.remove([])
            except:
                pass

        return [embed, buttons]

    def shop_menu_2(self, shop, ind=0):
        store = str(shop).replace("menu", "")
        #print(store, shops)
        if store in shops:
            store_items = shops[store]['items']
            item_list = []

            # Constructing description string with some fancy code.
            d = "Select An Item In The Dropdown to view it's stats.\n"
            e = "????????????????????????????????????????????????????????????????????????????????????"
            desc = d + e #"???"*len(d)
            # I can edit the ??? to change it's character in the future. 

            embed = discord.Embed(title=f"{shops[store]['name']}", description=desc)
            Items = self.client.get_cog("Items")
            
            # This is me creating the 1 field of the embed that will display what item is being focused on. 
            i = list(store_items)[ind]
            embed.add_field(name=f"{items[i]['name']}", value=f"> {store_items[i]['price']} {self.client.currency}\n> {items[i]['category']}, {items[i]['type']} \n> {items[i]['flavor']} \n**Stats**: \n >>> {Items.construct_item_stats_string(i)}")

            # This is creating the select menu so that the user can choose what item to focus on and whatnot. 
            index = 0
            for i in store_items:
                add = True
                stock = store_items[i]['stock']
                stockstr = ""
                if str(stock) != "infinite":
                    if int(stock) >= 1:
                        add = True
                        stockstr = f", In Stock: {stock}"
                    else:
                        add = False
                
                if add:
                    item_list.append(SelectOption(label=f"{items[i]['name']}", description=f"{store_items[i]['price']} {self.client.currency}{stockstr}", value=f"buy|{i}|{store}|{index}"))

                # Ticking the tracked index up one ffs. 
                # Because I'm doing this not kosher but It'll get there someday. 
                index += 1 

            menu = Select(options=item_list, placeholder="Select An Item To Buy/Preview", custom_id="store")

            

            return [embed, menu]

    @commands.command()
    async def shop(self, ctx):

        data = self.shop_menu()
        #print(data)
        await ctx.send(content = "G_ Town Market", embed=data[0], components=data[1])


    @commands.Cog.listener()
    async def on_button_click(self, interaction: Interaction):
        global shops
        global items
        #print(interaction.__dict__)
        player = __main__.get_player("", interaction.user.id, interaction.user.name)

        if str(interaction.custom_id).startswith("menu"):

            message = self.shop_menu_2(interaction.custom_id)

            await interaction.respond(type=4, embed=message[0], components=[message[1]])
            # name = interaction.component.label[0].

        if str(interaction.custom_id).startswith("buy"):
            v = interaction.custom_id
            value = v.split("|")
            shop = value[2]
            item = value[1]

            # Working on adding items to players.

            player.cash -= shops[shop]['items'][item]['price']

            player.add_item(item)

            await interaction.respond(type=4, embed=discord.Embed(description=f"You buy {items[item]['name']} for {shops[shop]['items'][item]['price']} {self.client.currency}."))

            if shops[shop]['items'][item]['stock'] != "infinite":
                shops[shop]['items'][item]['stock'] -= 1
                __main__.save_json(f"{__main__.ROOT_DIR}/configurations/shops.json", shops)

                player.save_data()
        if str(interaction.custom_id).startswith("cancel"):
            await interaction.respond(type=7, ephemeral=True, content="Action Canceled.")



    @commands.Cog.listener()
    async def on_select_option(self, interaction: Interaction):
        #print(interaction.component)
        #print("Selected Item, ", interaction.component.label)
        #print(interaction.values)

        #print(interaction.custom_id)

        v = interaction.values[0]
        value = v.split("|")
        
        mode =     value[0]
        shop =     value[2]
        item =     value[1]
        inde = int(value[3])

        if interaction.custom_id == "store":

            price = shops[shop]['items'][item]['price']

            player = __main__.get_player("", interaction.user.id, interaction.user.name)

            #
            # Updating Store Page to reflect the proper data
            #

            data = self.shop_menu_2(shop, inde)
            embe = data[0]
            select = data[1]
            components = [select]

            if player.cash >= price:
                components.append([Button(style=ButtonStyle.green, label="Buy Item", custom_id=f"buy|{item}|{shop}"), Button(style=ButtonStyle.red, label="Cancel Purchase (Closes The Store)", custom_id="cancel")])

            await interaction.respond(type=7, embed=embe, components=components)
            #print("Damn ")

            # if player.cash >= price:
            #     await asyncio.sleep(1)
            #     await interaction.respond(type=4, content=f"You selected {items[item]['name']} from {shops[shop]['name']} for {price} {self.client.currency} \n Confirm Purchase?", components=[
            #         [Button(style=ButtonStyle.green, label="Yes", custom_id=f"buy|{item}|{shop}"), Button(style=ButtonStyle.red, label="Cancel Purchase", custom_id="cancel")]
            #     ])

            # else:
            #     await interaction.respond(type=4, embed=discord.Embed(title="", description="You cannot afford that item."))

def setup(client):
    client.add_cog(Shop(client))