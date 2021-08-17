import discord
import json
from discord.ext import commands
from discord.utils import get
 

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('data/data.json') as file:
            data = json.load(file)
        data[str(guild.id)] = {}
        with open('data/data.json', 'w') as file:
            json.dump(data, file)

    @commands.command(brief='sets a specific setting')
    async def settings(self, ctx, action, setting=None, *, param=None):
        with open('data/data.json') as file:
            data = json.load(file)

        listOfSettings = ['createvoicechannel', 'temptalkname', 'temptalkcategory', None]
        if(setting not in listOfSettings):
            embed=discord.Embed(
                title='Error',
                description=f'{setting} is an unknown setting. Use `-setting list` to get a full list of all settings',
                color=discord.Color.from_rgb(255, 0, 0)
            )
            await ctx.send(embed=embed)
            return

        if(action == 'set'):
            data[str(ctx.guild.id)][setting] = param
            embed=discord.Embed(
                title='Settings',
                description=f'{setting} -> {param}',
                color=discord.Color.from_rgb(0, 0, 255)
            )
            with open('data/data.json', 'w') as file:
                json.dump(data, file)

        elif(action == 'get'):
            try:
                embed=discord.Embed(
                    title='Settings',
                    description=f'{setting} -> {data[str(ctx.guild.id)][setting]}',
                    color=discord.Color.from_rgb(0, 0, 255)
                )
            except KeyError:
                embed=discord.Embed(
                    title='Error',
                    description='You have to set the setting before accessing them',
                    color=discord.Color.from_rgb(255, 0, 0)
                )
        
        elif(action == 'list'):
            embed=discord.Embed(
                title='Settings',
                description='This is a list of all settings of the Bot',
                color=discord.Color.from_rgb(0, 0, 255)
            )
            embed.add_field(name="createvoicechannel", value="The Channel you join to create a new channel", inline=False)
            embed.add_field(name="temptalkname", value="The standart name of a channel", inline=False)
            embed.add_field(name="temptalkcategory", value="The category, where the channels get created", inline=False)

        else:
            embed=discord.Embed(
                title='Error',
                description='You can either `set` or `get` a specific setting',
                color=discord.Color.from_rgb(255, 0, 0)
            )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Settings(client))
