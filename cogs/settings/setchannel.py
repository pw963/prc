import discord
from discord import Embed
from discord.ext import commands
from db.mongodb import settings

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="set-channel",
        aliases=["setchannel", "channel"],
        usage = "`g.set-channel warns #warnings`",
        help = "Settings ##Sets the channel specified to log punishments for the specified type (warns | kicks | bans). Once set, it may be updated by running the command again. ##`Punishment Type`, `Channel` ##`Manage Channels`"
    )
    @commands.has_permissions(manage_channels=True)
    async def set_channel(self, ctx, chType=None, channel: discord.TextChannel=None):
        if chType == None or channel == None:

            noData = Embed(
                description = "",
                color = discord.Color.blue()
            )

            arr = []
            for item in settings.find({"guild":ctx.guild.id}):
                arr.append(item)
            
            if len(arr) == 0:
                noData.description += f"Nothing yet."
                return await ctx.send("Correct usage: `g.set-channel [warns | kicks | bans] [#channel]`", embed=noData)
            else:
                for setting in settings.find({"guild":ctx.guild.id}):
                    noData.description += f"**{setting['type']} Channel** `-` <#{setting['_id']}>\n"
                
                return await ctx.send("Correct usage: `g.set-channel [warns | kicks | bans] [#channel]`", embed=noData)
        else:
            if chType.lower() == "warns":
                if settings.find_one({"type":"Warns", "guild":ctx.guild.id}): settings.delete_one({"type":"Warns", "guild":ctx.guild.id})
                settings.insert_one({"_id":channel.id, "type":"Warns", "guild":ctx.guild.id})

                return await ctx.send(f"Successfully set `#{channel.name}` as the warnings channel. All warns will now be logged there.")
            
            elif chType.lower() == "kicks":
                if settings.find_one({"type":"Kicks", "guild":ctx.guild.id}): settings.delete_one({"type":"Kicks", "guild":ctx.guild.id})
                settings.insert_one({"_id":channel.id, "type":"Kicks", "guild":ctx.guild.id})

                return await ctx.send(f"Successfully set `#{channel.name}` as the kicks channel. All kicks will now be logged there.")
            
            elif chType.lower() == "bans":
                if settings.find_one({"type":"Bans", "guild":ctx.guild.id}): settings.delete_one({"type":"Bans", "guild":ctx.guild.id})
                settings.insert_one({"_id":channel.id, "type":"Bans", "guild":ctx.guild.id})

                return await ctx.send(f"Successfully set `#{channel.name}` as the bans channel. All bans will now be logged there.")
            
            else:
                return await ctx.send(f"Unknown channel type. Please choose warns, kicks, or bans.")

def setup(client):
    client.add_cog(Settings(client))
