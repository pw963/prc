from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name="help",
        aliases=["commands"],
        usage = "`g.help [command name]`",
        help = "Help ##This command will display the available commands and when provided a command name, information about that specific command will be displayed. ##(Optional, actually) `command name` ##`None`"
    )
    async def ghelp(self, ctx, *args):
        if len(args) == 0:
            return await ctx.send(
                "**Prefix**: `g.`\nSpecify a command you want to get information from (`set-channel`, `warn`, `kick`, `ban`, `unban`, `github`)."
            )
        
        else:
            if args and (search := args[0]):
                if found_command := self.client.get_command(search):
                    arg = found_command.help

                    await ctx.send(
                        f"```yaml\n{arg.split('##')[0]}\n```\n__`{found_command.name}`__:\n{arg.split('##')[1]}\n**__Required Arguments__**: {arg.split('##')[2]}\n**__Required Permissions__**: {arg.split('##')[3]}\n**__Usage (Example)__**: {str(found_command.usage)}"
                    )
                else:
                    return await ctx.send(f"Command Not Found.")

def setup(client):
    client.add_cog(Help(client))
