# Importing
import discord
from discord import Embed
from utils.converters import getest
from discord.ext import commands
from db.mongodb import settings
from db.mongodb import punishments
from ro_py import Client # Module to interact with roblox
from ro_py import utilities
from ro_py.thumbnails import ThumbnailSize, ThumbnailType

roblox = Client() # Creating the client

class GameBan(commands.Cog):
    def __init__(self, client):
        self.client = client
    # The 'gban' command. Will ban a specified user (1st argument), with a reason (2nd argument). All of the user's previous punishments will be cleared, though the user can be unbanned with 'gunban'.
    @commands.command(
        name="gban",
        aliases=["gameban", "game-ban", "g-ban"]
    )
    @commands.has_permissions(manage_messages=True)
    async def gban(self, ctx, username=None, *, reason=None):
        if not settings.find_one({"guild":ctx.guild.id, "type":"Bans"}): # If there is no bans log channel set.
            return await ctx.send(f"This guild doesn't have a bans channel set! Set up one by using the command:\n`.set-channel bans [#channel]`")
         
        channel = discord.utils.get(ctx.guild.channels, id=settings.find_one({"guild":ctx.guild.id, "type":"Bans"})["_id"]) # Getting the bans log channel.

        if username is None: return await ctx.send(f"Please specify a roblox user.") # If there is no username specified
        if reason is None: return await ctx.send(f"Please specify a reason for banning this user.") # If there is no reason specified

        try:
            user = await roblox.get_user_by_username(username)
        except utilities.errors.UserDoesNotExistError:
            return await ctx.send(f"The user you tried to specify is not a registered roblox user.") # If the user specified could not be found on roblox
        
        avatar_image = await user.thumbnails.get_avatar_image(
            shot_type=ThumbnailType.avatar_headshot,
            size = ThumbnailSize.size_420x420,
            is_circular=False
        ) # Getting the user's picture

        # Random space idk why
    
        em = Embed(
            title=f"{user.name} ({user.display_name}) has been banned",
            description=f"`{getest()}`",
            url=user.profile_url,
            color = discord.Color.red()
        )
        em.add_field(name="Reason", value=reason, inline=False)

        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        em.set_thumbnail(url=avatar_image)

        punishments.delete_many({"id":user.id, "guild":ctx.guild.id}) # Deleting all of their earlier punishments.
        await ctx.send(f"`{user.name}` has been banned successfully. Logged in {channel.mention} `#{channel.name}`.")
        await channel.send(embed=em)
        # Inserting the ban
        punishments.insert_one({"type":"Ban", "time":getest(), "user":user.name, "display_name":user.display_name, "url": avatar_image, "guild":ctx.guild.id, "reason":reason, "id":user.id})
# Adding the cog
def setup(client):
    client.add_cog(GameBan(client))
