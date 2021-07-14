# Importing
import discord
from discord import Embed
from discord.ext import commands
from db.mongodb import settings # Loading the 'settings' collection.

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client # Initialization
    # The 'set-channel' command. Sets a settings for a channel, which will make the channel log punishments. The event the channel will log depends on the channel type that is specified (1st argument).
    # The channel that will receive the settings is the channel that is pinged (2nd argument)
    @commands.command(
        name="set-channel",
        aliases=["setchannel", "channel"]
    )
    @commands.has_permissions(manage_channels=True)
    async def set_channel(self, ctx, chType=None, channel: discord.TextChannel=None):
        if chType == None or channel == None: # If the channel type or the channel is not specified.

            em = Embed(
                description = "",
                color = discord.Color.blue()
            )

            arr = []
            for item in settings.find({"guild":ctx.guild.id}):
                arr.append(item) # Looking for how many settings the guild has in the collection, then adding their data to 'arr'.
            
            if len(arr) == 0: # If the guild has no settings set.
                em.description += f"Nothing yet."
                return await ctx.send("Correct usage: `.set-channel [warns | kicks | bans] [#channel]`", embed=em)
            else: # If there are settings set for the guild.
                for setting in settings.find({"guild":ctx.guild.id}): # Looping through the settings that the guild has.
                    em.description += f"**{setting['type']} Channel** `-` <#{setting['_id']}>\n" # Adding the setting's type, and the setting's channel.
                
                return await ctx.send("Correct usage: `.set-channel [warns | kicks | bans] [#channel]`", embed=em)
        else:
            if chType.lower() == "warns": # If the channel type specified is 'warns'
                if settings.find_one({"type":"Warns", "guild":ctx.guild.id}): settings.delete_one({"type":"Warns", "guild":ctx.guild.id}) # Checking if a setting for warns exists already. If it does, the original setting will be deleted
                settings.insert_one({"_id":channel.id, "type":"Warns", "guild":ctx.guild.id}) # Creating the new setting

                return await ctx.send(f"Successfully set `#{channel.name}` as the warnings channel. All warns will now be logged there.")
            
            elif chType.lower() == "kicks": # If the channel type specified is 'kicks'
                if settings.find_one({"type":"Kicks", "guild":ctx.guild.id}): settings.delete_one({"type":"Kicks", "guild":ctx.guild.id}) # Checking if a setting for kicks exists already. If it does, the original setting will be deleted
                settings.insert_one({"_id":channel.id, "type":"Kicks", "guild":ctx.guild.id}) # Creating new setting

                return await ctx.send(f"Successfully set `#{channel.name}` as the kicks channel. All kicks will now be logged there.")
            
            elif chType.lower() == "bans": # If the channel type specified is 'bans'
                if settings.find_one({"type":"Bans", "guild":ctx.guild.id}): settings.delete_one({"type":"Bans", "guild":ctx.guild.id}) # Checking if a setting for bans exists already. If it does, the original setting will be deleted
                settings.insert_one({"_id":channel.id, "type":"Bans", "guild":ctx.guild.id}) # Creating new setting

                return await ctx.send(f"Successfully set `#{channel.name}` as the bans channel. All bans will now be logged there.")
            
            else: # If the channel type specified is not 'kicks', 'bans', or 'warns'.
                return await ctx.send(f"Unknown channel type. Please choose warns, kicks, or bans.")
# Adding the cog
def setup(client):
    client.add_cog(Settings(client))
