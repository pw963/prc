import discord
from discord import Embed
from utils.converters import getest
from discord.ext import commands
from db.mongodb import settings
from db.mongodb import punishments
from ro_py import Client
from ro_py import utilities
from ro_py.thumbnails import ThumbnailSize, ThumbnailType
import requests, json

roblox = Client()

class GameWarn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="warn",
        aliases=["gamewarn", "game-warn", "g-warn", "gwarn"],
        usage = "`g.warn TheJPlayer123 Full Killing`",
        help="Game Punishments ##This command requires the guild to have a channel to log warnings (`set-channel` to set it up). If there is, then the warning will be logged and a message log will be sent in the warning logs channel. *The bot will set a footer to the embed sent if the user has 3 warnings or has exceeded.* The user that is specified must be an existing Roblox user, else the command will not work. ##`Username`, `Reason` ##`Manage Messages`"
    )
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, username=None, *, reason=None):
        if not settings.find_one({"guild":ctx.guild.id, "type":"Warns"}):
            return await ctx.send(f"This guild doesn't have a warns channel set! Set up one by using the command:\n`g.set-channel warns [#channel]`")

        channel = discord.utils.get(ctx.guild.channels, id=settings.find_one({"guild":ctx.guild.id, "type":"Warns"})["_id"])

        if username is None: return await ctx.send(f"Please specify a roblox user.")
        if reason is None: return await ctx.send(f"Please specify a reason for warning this user.")

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
        
        if punishments.count_documents({"user":user.name, "type":"Warn", "guild":ctx.guild.id}) == 3:
            em.set_footer(text=f"This user now has 3 warnings, and should be kicked.")

        if punishments.count_documents({"user":user.name, "type":"Warn", "guild":ctx.guild.id}) > 3:
            em.set_footer(text=f"This user has exceeded 3 warnings, and should be kicked.")

        await channel.send(embed=em)
        await ctx.send(f"`{user.name}` has been warned successfully. Logged in {channel.mention} `#{channel.name}`.")

def setup(client):
    client.add_cog(GameWarn(client))
