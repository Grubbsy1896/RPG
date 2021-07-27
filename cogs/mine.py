from discord.ext import commands
from discord.utils import *
import discord 
import __main__
import random

from discord_components import *

class Mine(commands.Cog):
    def __init__(self, client):
        self.client = client


    # default_mine_settings = {
    #     "materials": {
    #             "Iron":     10, 
    #             "Diamond":  4,  
    #             "Copper":   15, 
    #             "Coal":     15, 
    #             "Gold":     10, 
    #             "Lead":     10, 
    #             "Silver":   10,       
    #             "Tin":      10, 
    #             "Stone":    15, 
    #             "Ruby":     1
    #         }, # I want the total to be 100, 0 left.
    #     "cooldown": 30,
    #     "channel": 869268774379982910,
    #     "NULL": None
    # }

    global settings
    settings = __main__.game_settings['cogs']['mine']

    oredict = settings['commands']['mine']['materials']

    global ores
    global ore_weights

    ores        = []
    ore_weights = []

    for ore in oredict:
        ores.append(ore)
        ore_weights.append(oredict[ore])

    # print(random.choices(ores, weights=weights)) # random.choices because it's needed.


    @commands.cooldown(1,     __main__.game_settings['cogs']['mine']['commands']['mine']['cooldown'], commands.BucketType.user)
    @commands.command(aliases=__main__.game_settings['cogs']['mine']['commands']['mine']['aliases'])
    async def mine(self, ctx):
        global ores
        global ore_weights
        player = __main__.get_player(ctx)
        

        # You can only mine in the specified channel.

        if int(ctx.channel.id) == int(settings['commands']['mine']['channel']):


            #
            # > Getting Pickaxe Data/Stats
            #
            print("Fuck 1")
            if 'pickaxe' in player.equipped_gear:
                print("Fuck 2")
                pickaxe = player.equipped_gear['pickaxe']
                print("Fuck 3")

                if str(pickaxe) in player.inventory and str(pickaxe) != "":
                    print("Fuck 4")
                    pickaxe = player.inventory[pickaxe]
                    min_power = pickaxe['min_power']
                    max_power = pickaxe['max_power']
                    pickaxe_name = f"{pickaxe['name']}"
                else:
                    print("Fuck 5, where we should be")
                    min_power = 1
                    max_power = 3
            else:
                print("Fuck 6 and a half")
                player.equipped_gear['pickaxe'] = ""
                min_power = 1
                max_power = 3

            # More room for future logic

            if player.equipped_gear['pickaxe'] == "":
                pickaxe_name = "Borrowed Pickaxe"

            #
            # > Generating Mined Ores.
            #
            ore = random.choices(ores, ore_weights)[0]
            amount = random.randint(min_power, max_power)

            # 
            # > Constructing Message
            #
            color = settings['commands']['mine']['color'] 
            action_string = f"You mine {amount} {ore} with {pickaxe_name}"

            mine_embed = discord.Embed(title="", description=action_string, colour = discord.Colour.from_rgb(color[0], color[1], color[2]))
            
            print("WHY")
            await ctx.send(embed=mine_embed)

            #
            # > Saving Data
            #
            player.add_material(ore, amount) # < - 
            print("FUCK SHIT PISS CUNT")
            player.save_data()


    @mine.error
    async def mine_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'You must wait {:.2f}s before mining again. Rest easy!'.format(error.retry_after)
            e = discord.Embed(title="", description = msg, colour= discord.Colour.from_rgb(255, 25, 25))
            await ctx.send(embed=e)

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.client.get_channel(settings['commands']['mine']['channel'])
        await channel.send("I'm made of stone, end my misery!!!", 
                            components = [ 
                                Button(style=ButtonStyle.blue, label="Attempt To Kill Me!!!", custom_id="mine"),
                            ],
                            
            )

        # res = await self.client.wait_for("button_click")
        # if res.channel == channel:
        #     await res.respond(
        #         type=InteractionType.ChannelMessageWithSource,
        #         content=f'{res.component.label} clicked'
        # )

    @commands.Cog.listener()
    async def on_button_click(self, interaction: Interaction):
        print(interaction.__dict__)
        if interaction.custom_id == "mine":
            await interaction.respond(type=4, content="YOU HIT ME!", ephemeral=True)

def setup(client):
    client.add_cog(Mine(client))