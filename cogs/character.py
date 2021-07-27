import __main__
import discord
from discord.ext import commands
from discord.utils import get
from discord_components import *

class Character(commands.Cog):
    def __init__(self, client):
        self.client = client

        global emojis
        emojis = self.client.custom_emojis

        global game_settings 
        game_settings = self.client.game_settings['cogs']['character']


    def construct_embed(self, user, player):
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

    @commands.cooldown(1, __main__.game_settings['cogs']['character']['commands']['profile']['cooldown'], commands.BucketType.user)
    @commands.command(aliases=__main__.game_settings['cogs']['character']['commands']['profile']['aliases'])
    async def profile(self, ctx):
        player = __main__.get_player(ctx)
        
        embed = self.construct_embed(ctx.author, player)

        await ctx.send(embed=embed)
    
    @commands.command()
    async def materials(self, ctx):
        player = __main__.get_player(ctx)
        await ctx.send(f"{player.materials}")

    @commands.command()
    async def devfuck(self, ctx):
        players = self.client.players
        for player in players:
            player = players[player]
            await ctx.send({key:value for key, value in player.__dict__.items() if not key.startswith('__') and not callable(key)})

    @profile.error
    async def profile_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
            e = discord.Embed(title="", description = msg, colour= discord.Colour.from_rgb(255, 25, 25))
            await ctx.send(embed=e)


    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.client.get_channel(game_settings['commands']['profile']['channel'])
        await channel.send("Request Profile Information", 
                            components = [ 
                                Button(style=ButtonStyle.blue, label="View Info", custom_id="profile"),
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
        if interaction.custom_id == "profile":
            player = __main__.get_player("", interaction.user.id, interaction.user.name)
            content = self.construct_embed(interaction.user, player)
            await interaction.respond(type=4, embed=content, ephemeral=True)



def setup(client):
    client.add_cog(Character(client))




# so let's say I'm at 200xp 

# im lvl 1, 

# 100/110 xp 

# it's 

# actually technically

# 200/210

# so I just sub the prev level req for display reasons.