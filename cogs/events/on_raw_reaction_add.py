import discord
from discord.ext import commands
from db.mongodb import checks

class On_Raw_Reaction_Add(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not checks.find_one({"message":payload.message_id}): return

        msg = checks.find_one({"message":payload.message_id})

        if payload.user_id != self.client.user.id and str(payload.emoji) == u"\u2705" and payload.message_id == msg["message"]:
            if msg["status"] == "incomplete":

                if payload.member not in msg["reacted"]:
                    arr = msg["reacted"]
                    arr.append(payload.member.id)
                    checks.update_one({"message":payload.message_id}, {"$set":{"reacted":arr}})

def setup(client):
    client.add_cog(On_Raw_Reaction_Add(client))
