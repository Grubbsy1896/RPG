from discord.ext import commands

import __main__

class Mine(commands.Cog):
    def __init__(self, client):
        self.client = client


    default_mine_settings = {
        "materials": {
                "Iron":     10, 
                "Diamond":  4,  
                "Copper":   15, 
                "Coal":     15, 
                "Gold":     10, 
                "Lead":     10, 
                "Silver":   10,       
                "Tin":      10, 
                "Stone":    15, 
                "Ruby":     1
            }, # I want the total to be 100, 0 left.
        "cooldown": 30,
        "channel": 869268774379982910,
        "NULL": None
    }


    
    # print(random.choices(ores, weights=weights)) # random.choices because it's needed.

    @commands.command()
    async def mine(self, ctx):
        player = __main__.get_player(ctx)
        
        await ctx.send(f"{player.name} now has {player.cash}")
        player.save_data()


def setup(client):
    client.add_cog(Mine(client))