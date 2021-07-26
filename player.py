# Sunday July 18th 2021
# player.py is the file in which I will store the class for the discord player class.
# It will hopefully be a subclass.


from discord import Member
from data import save_player

import sqlite3

#
# Cash will be representative of the currency someone has
# Xp will be experience points, representative of progress/actions taken. 
# level is also self explenatory. 
# skills will be a dict, or list, or whatever, this is gameplay stuff but essentially a thing that I'm future proofing.
# inventory is the items the player will hold. materials will be specific inventory for items for crafting and trading.
# equipped gear, once again, will be a dict, simply for the sake of keeping things simple when dumping data to the database.
# job is the employement/class of the player. such as wizard, knight, etc. 
#

class Player(): # Subclassing Discord's Member.
    def __init__(self, id, name, cash=0, xp=0, level=0, health=100, mana=0, max_mana=10, skillpoints = 0, skills={}, inventory={}, materials={}, equipped_gear={}, job=""):
        
        self.id = id
        self.name = name
        self.cash = cash
        self.xp = xp
        self.level = level
        self.health = health
        self.mana = mana
        self.max_mana = max_mana
        self.skillpoints = skillpoints
        self.skills = skills
        self.inventory = inventory
        self.materials = materials
        self.equipped_gear = equipped_gear
        self.job = job
    
        

    def save_data(self):
        # Everything spaced out for readability
        # id, name, cash, xp, level, character dict, skills dict, inventory dict, materials dict, and gear dict
        id = self.id
        name = self.name
        cash = self.cash
        xp = self.xp
        level = self.level
        character = {
            "health": self.health, 
            "mana": self.mana,
            "max_mana": self.max_mana,   
            "job": self.job,
            "skillpoints": self.skillpoints
        }
        skills = self.skills
        materials = self.materials
        inventory = self.inventory
        gear = self.equipped_gear

        save_player(
                (
                id,        
                name, 
                cash, 
                xp, 
                level, 
                character,  # For readability purposes.
                skills, 
                inventory, 
                materials, 
                gear
                )
            )


    def next_level(self, level="self"):

        if level == "self":
            xp_req = (((self.level+1)*100)+(10*self.level))

        elif isinstance(level, int):
            if level < 0:
                xp_req = 0
            else:
                xp_req = (((self.level+1)*100)+(10*self.level))
        else:
            xp_req = 0

        return xp_req

    def level_up(self):
        xp_req = self.next_level()
        if self.xp <= xp_req:
            self.level += 1
            return True
        return False      

    def add_material(self, material, amount=0):

        if str(material) in self.materials: # This checks to avoid error, and to make sure to add to the player's materials if it's not there
            self.materials[str(material)] += amount
        else:
            self.materials[str(material)] = amount

# When I save player data I will have to construct a dict of mana, health, and whatnot as well as putting job/race in there as well.
#
#


# I need to finish it but yeah.