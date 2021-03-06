# Sunday July 18th 2021
# player.py is the file in which I will store the class for the discord player class.
# It will hopefully be a subclass.


from discord import Member
from data import save_player
from configuration import items

import random

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
    def __init__(self, id, name, cash=0, xp=0, level=0, health=100, mana=0, max_mana=10, skillpoints = 0, skills=None, inventory=None, materials=None, equipped_gear=None, job=""):
        
        self.id = id
        self.name = name
        self.cash = cash
        self.xp = xp
        self.level = level
        self.health = health
        self.mana = mana
        self.max_mana = max_mana
        self.skillpoints = skillpoints
        self.job = job


        self.skills = skills
        self.inventory = inventory
        self.materials = materials
        self.equipped_gear = equipped_gear

        if self.skills is None:
            self.skills = {}    
        else:
            self.skills = skills

        if self.inventory is None:
            self.inventory = {}    
        else:
            self.skills = skills

        if self.materials is None:
            self.materials = {}
        else:
            self.materials = materials
        
        if self.equipped_gear is None:
            self.equipped_gear = {}    
        else:
            self.equipped_gear = equipped_gear


        

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

    def add_material(self, material, amount):
        print("adding")
        print(self.materials, material, amount)
        if str(material) in self.materials: # This checks to avoid error, and to make sure to add to the player's materials if it's not there
            self.materials[str(material)] += amount
        else:
            
            try:
                self.materials[material] = amount 
            except Exception as e:
                print("OOPS", e)
    
    def add_item(self, iid): 
        
        # We need to know whether the id is a valid item id, and then proceed from there.

        if iid in items:
            # Congrats, we didn't fuck up... or something 
            
            item = items[iid]


            # For the most part, we're just copying values over.

            custom_item = {
                "name": item['name'],
                "flavor": item['flavor'],
                "category": item['category'],
                "type": item['type'],
                "rarity": item['rarity'],
                "value": item['value'],
                "base_stats": {},
                "original_owner": self.name,
                "enchantments": [],
                "forges": 0
            }

            # Constructing the base stats

            modifiers = []
            weights = []

            for i in item['mod_range']:
                modifiers.append(int(i))
                weights.append(int(item['mod_range'][i]))

            for stat in item['base_stats']:
                new_stat = random.choices(modifiers, weights)
                custom_item["base_stats"][stat] = item['base_stats'][stat] + new_stat[0]

            
            if custom_item['base_stats']['min_power'] > custom_item['base_stats']['max_power']:
                temp = custom_item['base_stats']['min_power']
                custom_item['base_stats']['min_power'] = custom_item['base_stats']['max_power']
                custom_item['base_stats']['max_power'] = temp


            # Adding Item To Player
            print(custom_item)

            # getting the item id to assign to the item.
            item_id = str(len(self.inventory)+1)
            if item_id in self.inventory:
                item_id = self.get_new_item_id()

            self.inventory[item_id] = custom_item

    def get_new_item_id(self, offset=0):
        inv = self.inventory
        if str(offset) in inv:
            self.get_new_item_id(offset+1)
        else:
            return offset







