import discord
from discord import Embed
from utils.converters import getest
from discord.ext import commands
from db.mongodb import settings
from db.mongodb import punishments
from ro_py import Client
from ro_py import utilities
from ro_py.thumbnails import ThumbnailSize, ThumbnailType
import requests
import json

roblox = Client()

class GameUnban(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(
        name="unban",
        aliases=["gameunban", "game-unban", "g-unban", "gunban"],
        usage = "`g.unban TheJPlayer123 Wrongly banned`",
        help = "Game Punishments ##This command requires the guild to have a channel to log bans (`set-channel` to set it up). All the punishments will be cleared and a message embed will be sent to the ban logs channel. The user that is specified must be marked as banned in the bot's database and must be a registered Roblox user. ##`Username`, `Reason` ##`Manage Messages`"
    )
    async def unban(self, ctx, username=None, *, reason=None):
        if not settings.find_one({"guild":ctx.guild.id, "type":"Bans"}):
            return await ctx.send(f"This guild doesn't have a bans channel set! Set up one by using the command:\n`g.set-channel bans [#channel]`")
        
        channel = discord.utils.get(ctx.guild.channels, id=settings.find_one({"guild":ctx.guild.id, "type":"Bans"})["_id"])

        if username is None: return await ctx.send(f"Please specify a roblox user.")
        if reason is None: return await ctx.send(f"Please specify a reason for unbanning this user.")


        if ctx.message.mentions:
            response_API = requests.get(f'https://api.blox.link/v1/user/{ctx.message.mentions[0].id}')
            data = response_API.text
            parse_json = json.loads(data)

            if parse_json["status"] == "ok":
                user1 = await roblox.get_user(int(parse_json["primaryAccount"]))
                username = user1.name
            else:
                return await ctx.send(f"The user you tried mentioning isn't a verified Bloxlink user.")

        try:
            user = await roblox.get_user_by_username(username)
        except utilities.errors.UserDoesNotExistError:
            return await ctx.send(f"The user you tried to specify is not a registered roblox user.")
        
        if not punishments.find_one({"type":"Ban", "guild":ctx.guild.id}): return await ctx.send(f"This user was never banned.")

        avatar_image = await user.thumbnails.get_avatar_image(
            shot_type=ThumbnailType.avatar_headshot,
            size = ThumbnailSize.size_420x420,
            is_circular=False
        )

        punishments.delete_many({"guild":ctx.guild.id, "user":user.name})

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
        await ctx.send(f"`{user.name}` has been unbanned successfully. Logged in {channel.mention} `#{channel.name}`.")

def setup(client):
    client.add_cog(GameUnban(client))
