# June 18th 2021
# configuration.py is used to load the config data for my RPG bot.


# --
# > Imports
# --
import json
import os
import sys

from data import open_json, save_json, ROOT_DIR



# --
# > Declaring Variables
# --
configspath = f"{ROOT_DIR}/configurations/"



# --
# > Functions
# --

def load_settings(path):
    settings = open_json(path)

    if settings == False:
        print(f"Cannot Read settings.json, please make it at {path}")
        print("Insert {} into the file and save it and try again.")
        raise FileExistsError

    if len(settings) == 0:
        settings = {
            "token": "TOKEN",
            "prefix": "!"
        }
        save_json(path, settings)

    return settings

def load_items_config(path):
    items_config = open_json(path)

    if items_config == False:
        print(f"Cannot Read items_config.json, please make it at {path}")
        print("Insert {} into the file and save it and try again.")
        raise FileExistsError

    if len(items_config) == 0:
        items_config = {
        }
        save_json(path, items_config)

    return items_config

def load_mine_config(path):
    mine_config = open_json(path)

    if mine_config == False:
        print(f"Cannot Read mine.json, please make it at {path}")
        print("Insert {} into the file and save it and try again.")
        raise FileExistsError

    if len(mine_config) == 0:
        mine_config = {

        }
        save_json(path, mine_config)

    return mine_config

def load_emoji_config(path):
    emoji_config = open_json(path)

    if emoji_config == False:
        print(f"Cannot Read emojis.json, please make it at {path}")
        print("Insert {} into the file and save it and try again.")
        raise FileExistsError

    if len(emoji_config) == 0:
        emoji_config = {
            "Format": "Just put the emoji ID",
            "info": "Make sure to get the emoji id from developer mode, and right clicking on the emoji.",
            "health": "",
            "mana": "",
            "cash": "", 
            "mine": "",
            "xp": "",
            "level": ""
        }
        save_json(path, emoji_config)

    return emoji_config

def load_game_settings(path):
    game_config = open_json(path)

    if game_config == False:
        print(f"Cannot Read game_settings.json, please make it at {path}")
        print("Insert {} into the file and save it and try again.")
        raise FileExistsError

    if len(game_config) == 0:
        game_config = {
            "Info": "This is where we store settings for all the different portions of the game.",
            "currency_name": "Coins",
            "cogs": {
                "character": {
                    "commands": {
                        "profile": {
                            "aliases": ["character", "rpg", "CHARACTER", "PROFILE", "RPG"],
                            "color": (10, 10, 10)
                        },
                    },
                },
            },
        }
        save_json(path, game_config)

    return game_config

# --
# > Executing Setup
# --

bot_settings = load_settings(f"{configspath}/bot_settings.json")

game_settings = load_game_settings(f"{configspath}/game_settings.json")


emojis = load_emoji_config(f"{configspath}/emojis.json")
