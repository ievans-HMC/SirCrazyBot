#!/usr/bin/python3
import os, random, re, asyncio

import discord
from dotenv import load_dotenv

async def bot_games(message):
    # Die roller
    if (match := re.match(r"roll\sd(\d+)", message.content,re.I)):
        response = await roll_die(match)
    # Start a Tower of Hanoi game
    elif (match := re.match(r"hanoi\s?(\d+)?\s?(newgame)?([LlMmRr]{2})?", 
                            message.content,re.I)):
        print(match.group(0), match.group(1), match.group(2),match.group(3))
        if hanoi_games.get(message.guild.id) and not match.group(2):
            response = "Someone has already started a game on this " \
                        "server. Use `hanoi newgame` to start a new one"
        elif height := match.group(1):
            height = int(height)
            response = await start_hanoi(height, message.guild.id)
        else:
            response = "how high do you want the tower?"
            hanoi_games[message.guild.id] = 1
    # get height of Tower of Hanoi game
    elif hanoi_games.get(message.guild.id) == 1 and \
        (match := re.match(r"(\d+)",message.content)):
        height = int(match.group(1))
        if height:
            response = await start_hanoi(height, message.guild.id)
        else:
            response = "The tower has to have at least one layer dummy"
    elif hanoi_games.get(message.guild.id):
        response = await take_hanoi_turn(match.group(3), message.guild.id)
    # If no conditions are met ignore message
    else:
        return None
    return response


import TowerOfHanoi
hanoi = 0
hanoi_games = {}

async def start_hanoi(height: int, id: int):
    response = "error"
    if (game := hanoi_games.get(id)):
        print(f"{game=}")
        if type(game) == TowerOfHanoi.TowerOfHanoi:
            response = game.response
        else:
            hanoi_games[id] = TowerOfHanoi.TowerOfHanoi(height)
            game = hanoi_games[id]
            response = game.response
    else:
        hanoi_games[id] = TowerOfHanoi.TowerOfHanoi(height)
        game = hanoi_games[id]
        response = game.response
    return response

async def take_hanoi_turn(command: str, id: int):
    game = hanoi_games[id]
    game.play(command)
    response = game.response
    hanoi_games[id] = game
    return response


async def roll_die(match: re.Match):
    number = match.group(1)
    die_number = int(number)
    if die_number < 2:
        response = "🎲 That die does not have enough faces, " \
                    "I can't roll it for you 🎲"
    elif die_number > 1:
        roll = random.randint(1,die_number)
        response = f"🎲 I rolled a {roll} with a " \
                    f"{die_number}-sided die 🎲"
        if roll == 69:
            response = response[:-2] + ". Nice! 🎲"
        elif roll == 420:
            response = response[:-2] + ". Dank! 🎲"
        elif roll == die_number:
            response = f"🎲 Nat {die_number}! Woohoo! 🎲"
        await asyncio.sleep(1)
        print(response)
    else:
        response = "I didn't understand that request"
    if len(response) > 2000:
        response = "🎲 The die has too many faces 🎲"
    return response

# ==============================================================================

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guild(s):')
    for guild in client.guilds:
        print(f" - {guild.name} (id: {guild.id})")


@client.event
async def on_message(message):
    # Prevent the bot from responding to itself
    if message.author == client.user:
        return
    # Checks the '#bot-games' channel for commands
    if message.channel.name == "bot-games":
        response = await bot_games(message)
    # Checks for mentions and sends a help message
    elif client.user in message.mentions:
        channel_name = "#bot-games"
        if (channel := discord.utils.get(message.guild.text_channels,
                                         name="bot-games")):
            channel_name = f"<#{channel.id}>"

        response = f"Use the {channel_name} channel to play games with me. " \
                    "If the channel does not exist on this server, ask an " \
                    "admin to create it.\n" \
                    "Available commands:\n" \
                    " - `roll d<number>` (Roll a die of the specified size)\n"\
                    " - `hanoi <number>` (Play a game of Tower of Hanoi with "\
                    "a specified tower height)"
    else:
        response = None
    if response:
        await message.channel.send(response)


if __name__ == "__main__":
    client.run(TOKEN)
