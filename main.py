import discord
from config.globals import extensions
from discord.ext import commands
import os
from webserver import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True

client = commands.Bot(command_prefix="g.", case_insensitive=True, intents = intents)

@client.command(
    name="reload",
    usage="`g.reload cogs.verification.verify`",
    help = f"Hidden Command ##This command allows the bot owner to reload commands. ##`Extension` ##`Bot Owner`"
)
@commands.is_owner()
async def reload(ctx, arg):
    try:
        client.unload_extension(f"{arg}")
        client.load_extension(f"{arg}")
        await ctx.send(f"✅ Successfully loaded " + arg)
    except: await ctx.send(f"⚠ An error occured.")


@client.command(
    name="github",
    aliases=["code", "repository", "rep"],
    help=f"Code ##This command will provide the URL for the bot's code repository on GitHub. ##`None` ##`None`",
    usage=f"`g.github`"
)
async def github(ctx):
    await ctx.send(f"**{client.user.name}**'s Code Repository: <https://github.com/pw963/prc/>")

if __name__ == "__main__":
    client.remove_command('help')
    for ext in extensions:
        try: client.load_extension(ext)
        except: client.load_extension(ext)
        print(f"Loaded: {ext}")

keep_alive()
client.run(os.environ["TOKEN"])
