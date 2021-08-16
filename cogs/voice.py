import discord
import json
from discord.ext import commands
from discord.utils import get


class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open('data/data.json') as file:
            data = json.load(file)
            cv = data[str(member.guild.id)]['createvoicechannel']
            temptalkcategory = data[str(member.guild.id)]['temptalkcategory']
            temptalkname = data[str(member.guild.id)]['temptalkname']
        if(before.channel != None):
            if(before.channel.name == cv):
                return
            if(before.channel.category.name == temptalkcategory):
                if(len(before.channel.members) == 0):
                    await before.channel.delete()
        if(after.channel != None):
            if(after.channel.name == cv):
                category = get(after.channel.guild.categories, name=temptalkcategory)
                channel = await after.channel.guild.create_voice_channel(name=temptalkname, category=category)
                if channel is not None:
                    await member.move_to(channel)
                    await channel.set_permissions(member, manage_channels=True, mute_members=True, deafen_members=True, manage_permissions=True)


def setup(client):
    client.add_cog(Voice(client))
