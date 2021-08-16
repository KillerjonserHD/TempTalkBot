import discord
from discord import Intents
from discord.ext import commands, tasks
import os
from discord.utils import get
from itertools import cycle

###
token = "PLACE TOKEN HERE"
prefix = "-"
###

client = commands.Bot(command_prefix=prefix, intents=Intents.all())


@client.event
async def on_ready():
    print("Bot is now ready")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-help"))

@client.event
async def on_command_error(ctx, error):
    embed=discord.Embed(
        title = "Error",
        description = f"{error}",
        color = 0xff0000
    )
    await ctx.send(embed=embed)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(token)
