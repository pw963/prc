import discord
from discord import Embed
from discord.ext import commands
from datetime import datetime
import requests
import json
from ro_py import Client
from ro_py.thumbnails import ThumbnailSize, ThumbnailType

roblox = Client()

class Verify(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="verify",
        aliases=["getroles", "get-roles"],
        usage="`g.verify`",
        help=f"Verification ##This command will allow people to verify with `Bloxlink` to help moderators act more quickly and more efficiently when giving punishments. ##`None` ##`None`"
    )
    async def verify(self, ctx):
        await ctx.send(f"Hello, **{ctx.author.name}**! Let me see if I can retrieve your Roblox account information...")

        response_API = requests.get(f'https://api.blox.link/v1/user/{ctx.author.id}')
        data = response_API.text
        parse_json = json.loads(data)

        if parse_json['status'] == "error":
            await ctx.send(f"It seems like you don't have an account linked with **Bloxlink** yet!\nGo to <https://blox.link/> to verify and set this as your primary account.\n\n__Instructions__\n1. `Sign in with Discord`, if you haven't.\n2. Visit: <https://blox.link/verification/847154944125173830>\n3. Scroll down to `Link A New Account To This Server`, then follow the instructions in order to verify your account.\n4. Click `Set this as your primary account` box.\n5. Once you're done with that, check: https://blox.link/account, to see if you set up your account correctly.\n6. **Say `g.verify` again and it should work this time!**")

        elif parse_json["status"] == "ok":
            user = await roblox.get_user(int(parse_json["primaryAccount"]))
            sidenote = ""
            try: await ctx.author.edit(nick=f"{user.display_name} (@{user.name}) ✔")
            except: sidenote = f"*I didn't have enough permissions to change your nickname.*"

            em = Embed(
                title=f"Verification Successful",
                description = f"**{user.display_name} (@{user.name})**, you have been verified with **Bloxlink**!\n\nYour Discord account is now linked with your Roblox account{', and your nickname has been updated' if sidenote == '' else ''}. {sidenote}",
                color = discord.Color.red(),
                timestamp = datetime.utcnow()
            )

            avatar_image = await user.thumbnails.get_avatar_image(
                shot_type=ThumbnailType.avatar_headshot,
                size = ThumbnailSize.size_420x420,
                is_circular=False
            )

            em.set_thumbnail(url=avatar_image)
            await ctx.send(embed=em)

def setup(client):
    client.add_cog(Verify(client))
