import discord
from discord import app_commands, ui
from discord.ext import commands

import asyncio
import json
import os
import sqlite3

from cogs.libs.roles import ServerConfig

GUILD = discord.Object(id=1009880371220992000)
config = json.loads(open("tempConfig.json").read())

class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents= intents, application_id="1021178176254267393")

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.command(name='clear', help='this command will clear msgs')
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit=amount)

@bot.event
async def on_message(message: discord.Message):
    if message.channel.id == ServerConfig["Register-Channel"]:
        print(" ")
        await message.delete()
    await bot.process_commands(message)

    if message.author == bot.user:
        return
    # await message.channel.send("Hello")
    
    

async def load():
    for file in os.listdir('./cogs'):
        filename = file[:-3]
        ext = os.path.splitext(file)[-1].lower()
        if ext == '.py':
            await bot.load_extension(f'cogs.{filename}')

async def main():
    await load()
    await bot.start(config["token"])

asyncio.run(main())
