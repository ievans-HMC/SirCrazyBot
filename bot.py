#!/usr/bin/python3
import os, sys, random, re, asyncio, traceback

import discord
from dotenv import load_dotenv

import TowerOfHanoi
hanoi_games = {}

async def bot_games(message):
    response = ""
    # Die roller
    if (match := re.match(r"roll\sd(\d+)", message.content,re.I)):
        response = await roll_die(int(match.group(1)))
    # Start a Tower of Hanoi game
    elif (match := re.match(r"hanoi\s?(newgame)?\s?(\d+)?\s?([LlMmRr]{2})?", 
                            message.content,re.I)):
        if hanoi_games.get(message.guild.id) and \
            not (match.group(1) or match.group(3)):
            
            response = ("Not a valid move, please use `hanoi LMR`. If you want "
                        "to start a new game please use "
                        "`hanoi newgame [height]`"
                    )
        # If a game of Tower of Hanoi is in progress take turn
        elif hanoi_games.get(message.guild.id) and match.group(3):
            response = await take_hanoi_turn(match.group(3), message.guild.id)
        else:
            height = match.group(2)
            if height:
                height = int(height)
                if height > 12:
                    height = 12
                    response = "I'm sorry, but due to Discord's character " \
                               "limit, I can't make a tower taller than 12\n\n"     
            else:
                height = 4
                response = "No height specified, using the default height of " \
                          f"{height}\n"
            response += await start_hanoi(height, message.guild.id)
    # If no conditions are met ignore message
    else:
        return None
    return response

# ==============================================================================
# Tower of Hanoi
# ==============================================================================


async def start_hanoi(height: int, id: int):
    hanoi_games[id] = TowerOfHanoi.TowerOfHanoi(height)
    game = hanoi_games[id]
    game.start_game()
    response = game.response
    return response

async def take_hanoi_turn(command: str, id: int):
    game = hanoi_games[id]
    game.take_turn(command)
    response = game.response
    if game.game_over():
        del hanoi_games[id]
    else:
        hanoi_games[id] = game
    return response

# ==============================================================================
# Die Roller
# ==============================================================================

async def roll_die(val: int):
    if val < 2:
        response = "🎲 That die does not have enough faces, " \
                    "I can't roll it for you 🎲"
    elif val > 1:
        roll = random.randint(1,val)
        response = f"🎲 I rolled a {roll} with a " \
                    f"{val}-sided die 🎲"
        if roll == 69:
            response = response[:-2] + ". Nice! 🎲"
        elif roll == 420:
            response = response[:-2] + ". Dank! 🎲"
        elif roll == val:
            response = f"🎲 Nat {val}! Woohoo! 🎲"
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
    response = None
    # Prevent the bot from responding to itself
    if message.author == client.user:
        return
    # Checks the '#bot-games' channel for commands
    if message.channel.name == "bot-games":
        response = await bot_games(message)
    # Checks for mentions and sends a help message
    if client.user in message.mentions:
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

        if re.search(r"(github)", message.content, re.I):
            response = "Check out the GitHub: " \
                       "https://github.com/ievans-HMC/SirCrazyBot"
    if response:
        await message.channel.send(response)
        print(response)

@client.event
async def on_error(event, *args, **kwargs):
    message = f"error in event: {event}\n" \
              f"{args[0]}\n" \
              f"{traceback.format_exc()}"

    # Notify creators in case of error
    Isaiah = discord.utils.get(client.users,id=105053596957052928)
    Kevin = discord.utils.get(client.users,id=177222295507435520)
    if type(args[0].channel) != discord.DMChannel:
        await Isaiah.send(message)
        await Kevin.send(message)

if __name__ == "__main__":
    client.run(TOKEN)