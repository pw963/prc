# Importing
from discord.ext import commands
import discord
from discord.ext import commands
from dotenv import load_dotenv
from config.globals import extensions
import os

load_dotenv()

# Setting the Intents
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True

client = commands.Bot(command_prefix=".", case_insensitive=True, intents = intents)

# Reload command, when I'm lazy to restart the entire program.
@client.command(
    name="reload"
)
async def reload(ctx, ext):
    try:
        client.unload_extension(ext)
        client.load_extension(ext)
        return await ctx.send("Reloaded")
    except:
        return await ctx.send(f"Not a valid extension.")

# Very basic command, so I decided not to make a cog for it.
@client.command(
    name="code",
    aliases=["github", "repository", "rep"]
)
async def code(ctx):
    await ctx.send(f"View the bot's repository here: https://github.com/pw963/prc")
    
# Loading
if __name__ == "__main__":

    client.remove_command("help")

    for ext in extensions:
        try: client.load_extension(ext)
        except: client.load_extension(ext) # Happens to me sometimes. They didn't load properly so if that happened, they would be loaded, which would work.
        print(f"{ext} loaded.")

client.run(os.environ["TOKEN"]) # Logging in with "TOKEN" from the .env file
