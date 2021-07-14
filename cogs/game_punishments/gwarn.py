# Importing
import discord
from discord import Embed
from utils.converters import getest
from discord.ext import commands
from db.mongodb import settings
from db.mongodb import punishments
from ro_py import Client # Module to interact with ROBLOX
from ro_py import utilities
from ro_py.thumbnails import ThumbnailSize, ThumbnailType # Will be used later to customize thumbnails

roblox = Client() # Creating the client.

class GameWarn(commands.Cog):
    def __init__(self, client):
        self.client = client
    # The 'gwarn' command. Will issue a warn to a registered user in roblox (1st argument). It must be a roblox username that is specified and not a ping/mention. Then the second argument, is the reason.
    # Once a user receives 3 warnings, the bot will set a footer to the notification alerting that the user already has 3 warnings and should be given a kick from the server.
    @commands.command(
        name="gwarn",
        aliases=["gamewarn", "game-warn", "g-warn"]
    )
    @commands.has_permissions(manage_messages=True)
    async def gwarn(self, ctx, username=None, *, reason=None):
        if not settings.find_one({"guild":ctx.guild.id, "type":"Warns"}): # If there is no warnings log channel set.
            return await ctx.send(f"This guild doesn't have a warns channel set! Set up one by using the command:\n`.set-channel warns [#channel]`")

        channel = discord.utils.get(ctx.guild.channels, id=settings.find_one({"guild":ctx.guild.id, "type":"Warns"})["_id"]) # Getting the channel.

        if username is None: return await ctx.send(f"Please specify a roblox user.") # If there is no username specified.
        if reason is None: return await ctx.send(f"Please specify a reason for warning this user.") # If there is no reason specified.

        try:
            user = await roblox.get_user_by_username(username)
        except utilities.errors.UserDoesNotExistError: # If the user specified is not a registered roblox user.
            return await ctx.send(f"The user you tried to specify is not a registered roblox user.")
        
        avatar_image = await user.thumbnails.get_avatar_image(
            shot_type=ThumbnailType.avatar_headshot,
            size = ThumbnailSize.size_420x420,
            is_circular=False
        ) # Getting the user's avatar thumbnail.
        # Inserting the punishment.
        punishments.insert_one({"type":"Warn", "time":getest(), "user":user.name, "display_name":user.display_name, "url": avatar_image, "guild":ctx.guild.id, "reason":reason})

        em = Embed(
            title=f"{user.name} ({user.display_name}) has been warned",
            description=f"`{getest()}`",
            url=user.profile_url,
            color = discord.Color.red()
        )
        em.add_field(name="Reason", value=reason, inline=False)
        
        em.add_field(name="Count", value=f"{punishments.count_documents({'user':user.name, 'type':'Warn', 'guild':ctx.guild.id})}", inline=False)

        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        em.set_thumbnail(url=avatar_image)
        
        if punishments.count_documents({"user":user.name, "type":"Warn", "guild":ctx.guild.id}) == 3: # If the amount of warns is 3.
            em.set_footer(text=f"This user now has 3 warnings, and should be kicked.")

        if punishments.count_documents({"user":user.name, "type":"Warn", "guild":ctx.guild.id}) > 3: # If the amount of warns exceeds 3.
            em.set_footer(text=f"This user has exceeded 3 warnings, and should be kicked.")

        await channel.send(embed=em)
        await ctx.send(f"`{user.name}` has been warned successfully. Logged in {channel.mention} `#{channel.name}`.")
# Adding the cog
def setup(client):
    client.add_cog(GameWarn(client))
