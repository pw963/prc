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

class GameKick(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="kick",
        aliases=["game-kick", "gamekick", "g-kick", "gkick"],
        usage = "`g.kick TheJPlayer123 3 Warnings`",
        help = "Game Punishments ##This command requires the guild to have a channel to log kicks (`set-channel` to set it up). The kick will be logged and a message embed will be sent to the kick logs channel. *The bot will set a footer to the embed sent if the user has 3 kicks or has exceeded.* The user that is specified must be a registered Roblox user. *All warnings will be cleared once the user is kicked.* ##`Username`, `Reason` ##`Manage Messages`"
    )
    @commands.has_permissions(manage_messages=True)
    async def kick(self, ctx, username=None, *, reason=None):
        if not settings.find_one({"guild":ctx.guild.id, "type":"Kicks"}):
            return await ctx.send(f"This guild doesn't have a kicks channel set! Set up one by using the command:\n`g.set-channel kicks [#channel]`")

        channel = discord.utils.get(ctx.guild.channels, id=settings.find_one({"guild":ctx.guild.id, "type":"Kicks"})["_id"])

        if username is None: return await ctx.send(f"Please specify a roblox user.")
        if reason is None: return await ctx.send(f"Please specify a reason for kicking this user.")

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
        
        avatar_image = await user.thumbnails.get_avatar_image(
            shot_type=ThumbnailType.avatar_headshot,
            size = ThumbnailSize.size_420x420,
            is_circular=False
        )

        punishments.insert_one({"type":"Kick", "time":getest(), "user":user.name, "display_name":user.display_name, "url": avatar_image, "guild":ctx.guild.id, "reason":reason})

        em = Embed(
            title=f"{user.name} ({user.display_name}) has been kicked",
            description=f"`{getest()}`",
            url=user.profile_url,
            color = discord.Color.red()
        )
        em.add_field(name="Reason", value=reason, inline=False)
        
        em.add_field(name="Count", value=f"{punishments.count_documents({'user':user.name, 'type':'Kick', 'guild':ctx.guild.id})}", inline=False)

        em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        em.set_thumbnail(url=avatar_image)
        
        if punishments.count_documents({"user":user.name, "type":"Kick", "guild":ctx.guild.id}) == 3:
            em.set_footer(text=f"This user now has 3 kicks, and should be banned.")

        if punishments.count_documents({"user":user.name, "type":"Kick", "guild":ctx.guild.id}) > 3:
            em.set_footer(text=f"This user has exceeded 3 kicks, and should be banned.")

        punishments.delete_many({"user":user.name, "type":"Warn", "guild":ctx.guild.id})

        await ctx.send(f"`{user.name}` has been kicked successfully. Logged in {channel.mention} `#{channel.name}`.")

        await channel.send(embed=em)


def setup(client):
    client.add_cog(GameKick(client))
