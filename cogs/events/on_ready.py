import discord
from discord.ext import commands
from db.mongodb import checks
from datetime import datetime, timedelta
import asyncio

class On_Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def collect_data(self):
        while True:
            currTime = datetime.utcnow() - timedelta(hours=4)

            for doc in checks.find({"guild":793248462446919772}):
                if currTime >= doc["expires"] and doc["status"] =="incomplete":
                    checks.update_one({"message":doc["message"]}, {"$set":{"status":"complete"}})

                    guild = self.client.get_guild(793248462446919772)

                    channel = self.client.get_channel(doc["channel"])
                    role = discord.utils.get(guild.roles, id=864225432151523338)
                    string = ""
                    arr = []
                    for user in role.members:
                        if user.id not in doc["reacted"]:
                            string += f"{user.mention}, "
                            
                            arr.append(user)
                    
                    if len(arr) == role.members:
                        await channel.send(f"Everyone has reacted to the activity check!")
                    
                    else:
                        await channel.send(f"{string} has not reacted to activity check #{doc['count']}!")

            await asyncio.sleep(1)


    @commands.Cog.listener()
    async def on_ready(self):
        print("Ready.")
        await self.collect_data()
        self.client.loop.create_task(self.status_change)


def setup(client):
    client.add_cog(On_Ready(client))
