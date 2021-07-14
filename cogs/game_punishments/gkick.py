# Importing
import discord
from discord import Embed
from utils.converters import getest
from discord.ext import commands
from db.mongodb import settings
from db.mongodb import punishments
from ro_py import Client # Package to interact with roblox
from ro_py import utilities
from ro_py.thumbnails import ThumbnailSize, ThumbnailType

roblox = Client()

class GameKick(commands.Cog):
    def __init__(self, client):
        self.client = client
    # The 'gkick' command. Logs a kick for a registered roblox user (1st argument). There must be a reason given (2nd argument), and if the user reaches 3 kicks or exceeds 3 kicks, the message log will have a footer alerting that the user must be banned.
    @commands.command(
        name="gkick",
        aliases=["game-kick", "gamekick", "g-kick"]
    )
    @commands.has_permissions(manage_messages=True)
    async def gkick(self, ctx, username=None, *, reason=None):
        if not settings.find_one({"guild":ctx.guild.id, "type":"Kicks"}): # If there is no kicks log channel set
            return await ctx.send(f"This guild doesn't have a kicks channel set! Set up one by using the command:\n`.set-channel kicks [#channel]`")

        channel = discord.utils.get(ctx.guild.channels, id=settings.find_one({"guild":ctx.guild.id, "type":"Kicks"})["_id"]) # getting the kicks channel log channel

        if username is None: return await ctx.send(f"Please specify a roblox user.") # If there is no username specified
        if reason is None: return await ctx.send(f"Please specify a reason for kicking this user.") # If there is no reason

        try:
            user = await roblox.get_user_by_username(username)
        except utilities.errors.UserDoesNotExistError:
            return await ctx.send(f"The user you tried to specify is not a registered roblox user.") # If the user specified does not exist on roblox.
        
        avatar_image = await user.thumbnails.get_avatar_image(
            shot_type=ThumbnailType.avatar_headshot,
            size = ThumbnailSize.size_420x420,
            is_circular=False
        ) # Getting the user's picture
        # Logging the kick
        punishments.insert_one({"type":"Kick", "time":getest(), "user":user.name, "display_name":user.display_name, "url": avatar_image, "guild":ctx.guild.id, "reason":reason, "id":user.id})
        
        em = Embed(
            title=f"{user.name} ({user.display_name}) has been kicked",
            description=f"`{getest()}`",
            url=user.profile_url,
            color = discord.Color.red()
        )
        em.add_field(name="Reason", value=reason, inline=False)
        
        em.add_field(name="Count", value=f"{punishments.count_documents({'id':user.id, 'type':'Kick', 'guild':ctx.guild.id})}", inline=False)

        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        em.set_thumbnail(url=avatar_image)
        
        if punishments.count_documents({"id":user.id, "type":"Kick", "guild":ctx.guild.id}) == 3: # If the user has 3 kicks
            em.set_footer(text=f"This user now has 3 kicks, and should be banned.")

        if punishments.count_documents({"id":user.id, "type":"Kick", "guild":ctx.guild.id}) > 3: # if the user exceeds 3 kicks
            em.set_footer(text=f"This user has exceeded 3 kicks, and should be banned.")

        punishments.delete_many({"id":user.id, "type":"Warn", "guild":ctx.guild.id}) # Deleting all the warns after 1 kick.

        await ctx.send(f"`{user.name}` has been kicked successfully. Logged in {channel.mention} `#{channel.name}`.")

        await channel.send(embed=em)

# Adding the cog
def setup(client):
    client.add_cog(GameKick(client))
