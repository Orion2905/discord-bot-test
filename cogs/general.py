import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say", help="Il bot ripete ciò che dici.")
    async def say(self, ctx, *, message: str):
        await ctx.send(message)
    
    @commands.hybrid_command(name="test", description="Ripete il messaggio dell'utente!")
    async def test(self, ctx: commands.Context, *, message: str):
        await ctx.send(f"🔊 {message}")

    @commands.command(name="cicicic", help="Il bot ripete ciò che dici.")
    async def cicicic(self, ctx, *, message: str):
        await ctx.send(message)
    

async def setup(bot):
    await bot.add_cog(General(bot))