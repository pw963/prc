import discord
from discord.ext import commands
from discord import Embed

class On_Member_Join(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.channels, id=878318471090405386)

        em = Embed(
            description = f"Hey {member.mention}, welcome to **{member.guild.name}**!",
            color = discord.Color.from_rgb(90, 221, 250)
        )
        await channel.send(embed=em)

def setup(client):
    client.add_cog(On_Member_Join(client))
