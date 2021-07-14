# Importing
import discord
from discord import Embed
from utils.converters import getest
from discord.ext import commands
from db.mongodb import settings
from db.mongodb import punishments
from ro_py import Client # Module to interact with Roblox
from ro_py import utilities
from ro_py.thumbnails import ThumbnailSize, ThumbnailType

roblox = Client() # Creating the client

class GameUnban(commands.Cog):
    def __init__(self, client):
        self.client = client
    # The 'gunban' command. If a user is banned (must be shown as banned in the bot's database), moderators can unban the user if there was a mistake. All previous punishments will be deleted.
    @commands.command(
        name="gunban",
        aliases=["gameunban", "game-unban", "g-unban"]
    )
    @commands.has_permissions(manage_messages=True)
    async def gunban(self, ctx, username=None, reason=None):
        if not settings.find_one({"guild":ctx.guild.id, "type":"Bans"}): # If there is no bans log channel set.
            return await ctx.send(f"This guild doesn't have a bans channel set! Set up one by using the command:\n`.set-channel bans [#channel]`")
        
        channel = discord.utils.get(ctx.guild.channels, id=settings.find_one({"guild":ctx.guild.id, "type":"Bans"})["_id"]) # Getting the bans log channel.

        if username is None: return await ctx.send(f"Please specify a roblox user.") # If there is no username specified
        if reason is None: return await ctx.send(f"Please specify a reason for unbanning this user.") # If there is no reason specified

        try:
            user = await roblox.get_user_by_username(username)
        except utilities.errors.UserDoesNotExistError:
            return await ctx.send(f"The user you tried to specify is not a registered roblox user.") # If the user specified is not a registered roblox user.
        
        if not punishments.find_one({"type":"Ban", "guild":ctx.guild.id, "id":user.id}): return await ctx.send(f"This user was never banned.") # If there is no ban log for the user.

        avatar_image = await user.thumbnails.get_avatar_image(
            shot_type=ThumbnailType.avatar_headshot,
            size = ThumbnailSize.size_420x420,
            is_circular=False
        ) # Getting the user's picture.

        punishments.delete_many({"guild":ctx.guild.id, "id":user.id}) # Deleting all previous punishments

        em = Embed(
            title=f"{user.name} ({user.display_name}) has been unbanned",
            description=f"`{getest()}`",
            url=user.profile_url,
            color = discord.Color.green()
        )
        em.add_field(name="Reason", value=reason, inline=False)

        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        em.set_thumbnail(url=avatar_image)
        
        await channel.send(embed=em)
# Adding the cog
def setup(client):
    client.add_cog(GameUnban(client))
