import __main__
import discord
from discord.ext import commands
from discord.utils import get
from discord_components import *

class Character(commands.Cog): # This is cog
    def __init__(self, client):
        self.client = client

        global emojis
        emojis = self.client.custom_emojis

        global game_settings 
        game_settings = self.client.game_settings['cogs']['character']


    # Returns an embed
    def construct_profile(self, user, player):
        # Getting vars.
        global game_settings
        profile_string = " > [ Ｐｒｏｆｉｌｅ ] "
        author_image = user.avatar_url
        color = game_settings['commands']['profile']['color']
        

        # xp vars
        # 
        xp = player.xp

        prev_req = player.next_level(player.level-1)
        curr_req = player.next_level() 

        prog_xp = player.xp - prev_req

        # I want to subtract the player's current xp amount and get the xp from their current level, to the next level.

        # Strings to add together
        health_string = f"{emojis['health']} Health: {player.health} "
        mana_string   = f"{emojis['mana']} Mana:   {player.mana} "
        cash_string   = f"{emojis['cash']} {self.client.currency}:   {player.cash} "
        level_string  = f"{emojis['xp']} XP:     {prog_xp}/{curr_req}"
        xp_string     = f"{emojis['level']} Level:  {player.level} "

        field_1 = f"{health_string} \n{mana_string} \n{cash_string} \n{level_string} \n{xp_string}" # Basic Info, health, mana, coins, etc.

        field_2 = f"Gear Coming Soon!"

        field_3 = f"Skills Coming Soon!"
        
        # Stats | Armor | Skills
        # Populating Embed
        embed = discord.Embed(title="", description=f"{profile_string}", colour= discord.Colour.from_rgb(color[0], color[1], color[2]))
        embed.set_author(name=f"{player.name}", icon_url=author_image, url=author_image)

        embed.add_field(name="----- [ Stats ] -----",  value=field_1)
        embed.add_field(name="----- [ Gear ] -----",   value=field_2)
        embed.add_field(name="----- [ Skills ] -----", value=field_3)

        return embed

    # Returns an embed
    def construct_materials(self, user, player): # getting the materials embed.
        global game_settings

        author_image = user.avatar_url
        color = game_settings['commands']['materials']['color']

        mat_string = ""
        for material in player.materials:
            emoji = ''
            if str(material).lower() in emojis:
                emoji = emojis[str(material).lower()]
            
            amount = player.materials[material]

            if amount >= 1:
                mat_string += f"{amount}x {emoji}{material} \n"   # Constructing the total string. 
        
        embed = discord.Embed(title="", description=mat_string, colour= discord.Colour.from_rgb(color[0], color[1], color[2]))
        embed.set_author(name=f"{player.name}", icon_url=author_image, url=author_image)

        return embed

    # Returns an embed and buttons in a list size 2
    def construct_inventory(self, user, player, index=0):

        author_image = user.avatar_url

        stat_strings = {
            "min_power": "Minimum Power",
            "max_power": "Maximum Power",
            "cooldown":  "Cooldown",
            "type_yield": "Ore Yield"
        }

        invlist = []

        for i in player.inventory:
            invlist.append(i)
        
        n = 5
        pages = [invlist[i:i + n] for i in range(0, len(invlist), n)]

        if index < len(pages) and index >= 0:
            # So we're in the pages list, most likely...

            page = pages[index]

            invbed = discord.Embed()

            for item in page:
                item = player.inventory[item]
                string  = ""
                string += f"*{item['flavor']}* \n"
                string += f"{item['category']}, {item['type']} \n"
                string += f"{item['rarity']} \n"
                string += f"-- Stats -- \n"
                for stat in item['base_stats']:
                    string += f"**{stat_strings[stat]}**: {item['base_stats'][stat]} \n"
                invbed.add_field(name=f"{item['name']}", value=string)

            # Constructing Buttons To Add.

            prev = False
            nxtp = False
            if index == 0:
                prev = True
            if index == len(pages)-1:
                nxtp = True

            #print("Prev, ", prev, "   Next, ", nxtp)
            buttons = [Button(label="Prev", style=ButtonStyle.gray, custom_id=f"invpage|{index-1}",disabled=prev), 
                       Button(label="Next", style=ButtonStyle.gray, custom_id=f"invpage|{index+1}",disabled=nxtp)]

            return [invbed, buttons]


        else:
            return [discord.Embed(title="No Items."), [Button(style=ButtonStyle.grey, label="Profile", custom_id="profile")]]


    #
    # Commands
    #

    @commands.cooldown(1, __main__.game_settings['cogs']['character']['commands']['profile']['cooldown'], commands.BucketType.user)
    @commands.command(aliases=__main__.game_settings['cogs']['character']['commands']['profile']['aliases'])
    async def profile(self, ctx):
        player = __main__.get_player(ctx)
        
        embed = self.construct_profile(ctx.author, player)

        await ctx.send(embed=embed, components= [
                [Button(style=ButtonStyle.green, label="Materials", custom_id="materials"),
                Button(style=ButtonStyle.grey, label="Profile", custom_id="profile")]
            ])
    
    @commands.command()
    async def materials(self, ctx):
        player = __main__.get_player(ctx)
        embed = self.construct_materials(ctx.author, player)
        await ctx.send(embed=embed, components= [
                [Button(style=ButtonStyle.green, label="Materials", custom_id="materials"),
                Button(style=ButtonStyle.grey, label="Profile", custom_id="profile")]
            ])

    @commands.command()
    async def inventory(self, ctx):
        player = __main__.get_player(ctx)
        embed = self.construct_inventory(ctx.author, player)
        await ctx.send(embed=embed[0], components= [
                embed[1],
                [Button(style=ButtonStyle.green, label="Materials", custom_id="materials"),
                Button(style=ButtonStyle.grey, label="Profile", custom_id="profile")]
            ])
            
    @profile.error
    async def profile_error(self, ctx, error): # Cooldown Error When !profile is run too much
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            e = discord.Embed(title="", description = msg, colour= discord.Colour.from_rgb(255, 25, 25))
            await ctx.send(embed=e)

    #
    # Events
    #
    
    @commands.Cog.listener()
    async def on_ready(self):
        #
        # Clearing the channel configured for the button for the profile.
        #
        channel = self.client.get_channel(game_settings['commands']['profile']['channel'])
        amount = 100
        messages = []
        async for message in channel.history(limit=amount + 1):
                messages.append(message)

        await channel.delete_messages(messages)

        # Sending the button
        await channel.send("Request Profile Information", 
                            components = [ 
                                Button(style=ButtonStyle.blue, label="View Info", custom_id="profilesend"),
                            ],     
            )

    @commands.Cog.listener()
    async def on_button_click(self, interaction: Interaction):

        if str(interaction.custom_id).startswith("profile"): # this is to save copy pasting the entire function again.
            type = 7 # Editing
            if str(interaction.custom_id).endswith("send"):
                type = 4 # Sending

            player = __main__.get_player("", interaction.user.id, interaction.user.name)
            content = self.construct_profile(interaction.user, player)

            await interaction.respond(type=type, embed=content, ephemeral=True, components= [  # Sending the button
                [Button(style=ButtonStyle.green, label="Materials", custom_id="materials"),
                Button(style=ButtonStyle.grey, label="Profile", custom_id="profile"),
                Button(style=ButtonStyle.red, label="Inventory", custom_id="invpage|0")]
            ])

        if interaction.custom_id == "materials": # materials
            player = __main__.get_player("", interaction.user.id, interaction.user.name)
            content = self.construct_materials(interaction.user, player)
            await interaction.respond(type=7, embed=content)

        if str(interaction.custom_id).startswith("invpage"):
            player = __main__.get_player("", interaction.user.id, interaction.user.name)
            if player.id == interaction.author.id: 
                l = str(interaction.custom_id).split("|")
                index = int(l[1])
                content = self.construct_inventory(interaction.user, player, index)
                await interaction.respond(type=4, embed=content[0], components=[content[1]])
            else:
                content = self.construct_inventory(interaction.user, player)
                await interaction.respond(type=4, embed=content[0], components=[content[1]])


def setup(client):
    client.add_cog(Character(client))


# so let's say I'm at 200xp 

# im lvl 1, 

# 100/110 xp 

# it's 

# actually technically

# 200/210

# so I just sub the prev level req for display reasons.