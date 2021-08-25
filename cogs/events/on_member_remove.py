import discord
from discord.ext import commands
from discord import Embed

class On_Member_Remove(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, id=878318513981366352)

        await channel.send(f"**{member}** has left the server. 😔")

def setup(client):
    client.add_cog(On_Member_Remove(client))
