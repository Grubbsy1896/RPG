# Sunday July 18th 2021
# data.py will be the file where data is handled in my new discod bot, RPG. 
# It will contain database management, as well as important functions.
# 
# 


# ------------
# > Imports
# ------------

import json
import os
import sys


import sqlite3
from typing_extensions import get_args

from discord import Member
#import player.Player as Player

# ------------
# > Defined Variables
# ------------

global ROOT_DIR
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------
# > Database Setup
# ------------

# This is an old bot I made's database.
# For this new bot I plan to employ dumping json strings to make it 
# much more expandible without touching the database too much.
# because to add new collumns I would have to probably just restart the db.
#
db = sqlite3.connect(os.path.join(ROOT_DIR + "/data/", "RPG.db"))
cur = db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS players (
        d_id TEXT PRIMARY KEY NOT NULL,
        p_name TEXT NOT NULL,
        cash INTEGER NOT NULL,
        xp INTEGER NOT NULL,
        level INTEGER NOT NULL,
        character TEXT NOT NULL, 
        skills TEXT NOT NULL,
        inventory TEXT NOT NULL,
        materials TEXT NOT NULL,
        equipped_gear TEXT NOT NULL
        )''')

# Character is where health, mana, race, and class will all be stored. Just like well every other part of the records it will be meant to be expandible. 

# ------------
# > Functions
# ------------

def open_json(path):
    if os.path.exists(path) != True:
        return False
    with open(path, 'r') as datafile:
        return json.load(datafile)

def save_json(path, data):
    if os.path.exists(path) != True:
        return False
    with open(path, 'w+') as datafile:
        json.dump(data, datafile, indent=4)

def save_player(player): # player must be a list of all the required things to dump.
    # Player MUST be a tuple
    # id, name, cash, xp, level, character dict, skills dict, inventory dict, materials dict, and gear dict.
    #   0   1     2     3    4       5           6       7          8       9
    # (id, name, cash, xp, level, character, skills, inventory, materials, gear)
    player = list(player)
    player[5] = str(json.dumps(player[5]))
    player[6] = str(json.dumps(player[6]))
    player[7] = str(json.dumps(player[7]))  # Holy shit, but like yeah...
    player[8] = str(json.dumps(player[8]))  # json.dumps dumps all the dicts as strings. easy loading.
    player[9] = str(json.dumps(player[9]))


    print("DEBUG ", player)
    player = tuple(player)
    p = cur.execute("INSERT OR REPLACE INTO players(d_id, p_name, cash, xp, level, character, skills, inventory, materials, equipped_gear) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", player)
    db.commit()

def load_player(player_id):
    p = cur.execute("SELECT * FROM players WHERE d_id=?", (player_id, )).fetchone()

    #   0   1     2     3    4       5           6       7          8       9
    # (id, name, cash, xp, level, character, skills, inventory, materials, gear)

    character = json.loads(str(p[5]))

    #  cash=0, xp=0, level=0, health=0, mana=0, skills={}, inventory={}, materials={}, equipped_gear={}, job=""

    name        = p[1]
    cash        = p[2]
    xp          = p[3]
    level       = p[4]
    health      = character['health']
    mana        = character['mana']
    max_mana    = character['max_mana']
    skillpoints = character['skillpoints']
    skills      = json.loads(p[6])
    inventory   = json.loads(p[7])
    materials   = json.loads(p[8])
    gear        = json.loads(p[9])
    job         = character['job']


    player = (player_id, name, cash, xp, level, health, mana, max_mana, skillpoints, skills, inventory, materials, gear, job)
    return player
