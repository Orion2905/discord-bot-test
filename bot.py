import discord
from discord.ext import commands
import database

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        super().__init__(command_prefix="$", intents=intents)
    
    async def on_ready(self):
        database.initialize_db()
        print("Il bot è pronto all'utilizzo!")

        for guild in self.guilds:
            await self.tree.sync(guild=guild)
            print(f"Comandi sincronizzati per il server: {guild.name}")
    
    async def setup_hook(self):
        for cog in ["cogs.general", "cogs.moderation", "cogs.utility", "cogs.interactive", "cogs.activity"]:
            await self.load_extension(cog)

bot = MyBot()