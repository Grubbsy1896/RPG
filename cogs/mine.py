from discord.ext import commands, tasks
from discord.utils import *
import discord 
import __main__
import random

from discord_components import *

class Mine(commands.Cog):
    def __init__(self, client):
        self.client = client

        global emojis
        emojis = self.client.custom_emojis
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
    #     }

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

    # What generating ores should look like.
    # print(random.choices(ores, weights=ore_weights)) # random.choices because it's needed.

    #
    # > Cooldowns for mining
    # -- I do not need to save these on the player objects or in database because it's all going to be localized within this cog. 

    global cooldowns
    cooldowns = {}


    def mining(self, user, player, channel):
        # Defining Variables
        global cooldowns

        if channel != "mine":
            channel = self.client.get_channel(settings['commands']['mine']['channel'])
            if int(channel.id) == int(settings['commands']['mine']['channel']):
                cont = True
        elif channel == "mine":
            cont = True
        else:
            cont = False
        # integral to channel-specific 
        if cont:

            #
            # Getting the player's cooldown and actioning on it.
            # -- It's kinda like a gate.

            if str(user.id) in cooldowns:
                cooldown = cooldowns[str(user.id)]
            else:
                # At this point the player probably isn't logged for cooldowns, and we give them no cooldown because they shouldn't have mined yet.
                cooldowns[str(user.id)] = 0
                cooldown = -1


            if cooldown >= 0:
                cooldown_string = __main__.game_settings['cogs']['mine']['commands']['mine']['cooldown_message']
                cooldown_string = cooldown_string.replace("TIME", str(cooldown))
                return discord.Embed(title="", description=cooldown_string, colour= discord.Colour.from_rgb(255, 25, 25))

            #
            # > Getting Pickaxe Data/Stats
            #
            if 'pickaxe' in player.equipped_gear:
                pickaxe = player.equipped_gear['pickaxe']

                if str(pickaxe) in player.inventory and str(pickaxe) != "":
                    pickaxe = player.inventory[pickaxe]
                    min_power = pickaxe['min_power']
                    max_power = pickaxe['max_power']
                    gear_cooldown = pickaxe['cooldown']
                    pickaxe_name = f"{pickaxe['name']}"
                else:
                    # Default Data, if not yet saved.
                    min_power = 1
                    max_power = 3
                    gear_cooldown = 60
            else:
                # Giving the player data. If they do not have it. (For New PLayers)
                player.equipped_gear['pickaxe'] = ""
                min_power = 1
                max_power = 3

            # More room for future logic

            # Default Data
            if player.equipped_gear['pickaxe'] == "":
                pickaxe_name = "Borrowed Pickaxe"

            #
            # > Generating Mined Ores.
            #
            ore = random.choices(ores, ore_weights)[0]
            amount = random.randint(min_power, max_power)

            #
            # Editing Player Data
            #

            player.add_material(ore, amount)
            cooldowns[str(user.id)] = gear_cooldown
            player.save_data()

            # 
            # > Constructing Message
            #

            emoji = ''
            if str(ore).lower() in emojis:
                emoji = emojis[str(ore).lower()]
                emoji += " "

            color = settings['commands']['mine']['color'] 
            action_string = f"You mine {amount} {ore} with {pickaxe_name}"

            color = settings['commands']['mine']['color'] 
            action_string = f"You mine {amount} {str(emoji)}{ore} with {pickaxe_name}"

            mine_embed = discord.Embed(title="", description=action_string, colour = discord.Colour.from_rgb(color[0], color[1], color[2]))

            return mine_embed

    @commands.cooldown(1,     __main__.game_settings['cogs']['mine']['commands']['mine']['cooldown'], commands.BucketType.user)
    @commands.command(aliases=__main__.game_settings['cogs']['mine']['commands']['mine']['aliases'])
    async def mine(self, ctx):
        global ores
        global ore_weights
        player = __main__.get_player(ctx)
    
        # You can only mine in the specified channel.
        await ctx.send(embed = self.mining(ctx.author, player, "mine"))

    #
    # Events
    #
            
    @mine.error
    async def mine_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'You must wait {:.2f}s before mining again. Rest easy!'.format(error.retry_after)
            e = discord.Embed(title="", description = msg, colour= discord.Colour.from_rgb(255, 25, 25))
            await ctx.send(embed=e)

    @commands.Cog.listener()
    async def on_ready(self):

        # Creating the mine button 
        channel = self.client.get_channel(settings['commands']['mine']['channel'])

        amount = 100
        messages = []
        async for message in channel.history(limit=amount + 1):
                messages.append(message)

        await channel.delete_messages(messages)
    
        await channel.send(f"{settings['commands']['mine']['name']}", 
                            components = [ 
                                Button(style=ButtonStyle.red, label="Mine ⛏", custom_id="mine"),
                            ],
                            
            )

        self.update_cooldowns.start()

    @commands.Cog.listener()
    async def on_button_click(self, interaction: Interaction):
        #print(interaction.__dict__)
        player = __main__.get_player("", interaction.user.id, interaction.user.name)

        if interaction.custom_id == "mine":
            await interaction.respond(type=4, embed=self.mining(interaction.user, player, "mine"), ephemeral=True)

    #
    # Tasks
    #

    @tasks.loop(seconds=1)
    async def update_cooldowns(self):
        global cooldowns

        for c in cooldowns:
            cooldowns[c] -= 1

def setup(client):
    client.add_cog(Mine(client))