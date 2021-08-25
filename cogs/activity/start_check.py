import discord
from discord.ext import commands
from discord import Embed
from db.mongodb import checks
from utils.converters import getest
from datetime import datetime, timedelta

class Start_Check(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name=f"start-check", aliases=["startcheck"])
    @commands.has_permissions(manage_roles=True)
    async def start_check(self, ctx):

        await ctx.message.delete()

        role = discord.utils.get(ctx.guild.roles, id=864225432151523338)

        delta = timedelta(hours=4)
        Time = datetime.utcnow() - delta
        Time += timedelta(hours=24)

        checks.insert_one({"guild":ctx.guild.id, "author":ctx.author.id, "expires":Time, "reacted":[], "channel":ctx.channel.id, "status":"incomplete"})

        em = Embed(
            title=f"Activity Check #{checks.count_documents({'guild':ctx.guild.id})}",
            description = f"{ctx.author.mention} has began an activity check! You have **24 hours** to react below, else you will be marked as absent.",
            color = discord.Color.red()
        ).set_footer(text=f"{getest()}")

        em.set_author(name=ctx.guild.name)

        msg = await ctx.send(f"{role.mention}", embed=em)
        await msg.add_reaction("✅")
        checks.update_one({"guild":ctx.guild.id, "expires":Time}, {"$set":{"message":msg.id}})
        checks.update_one({"guild":ctx.guild.id, "expires":Time}, {"$set":{"count":checks.count_documents({'guild':ctx.guild.id})}})

def setup(client):
    client.add_cog(Start_Check(client))
