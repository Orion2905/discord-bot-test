import discord
from discord.ext import commands

class Utility(commands.Cog):
    """Comandi di utilità"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", help="Mostra informazioni sul bot.")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Informazioni sul Bot",
            description="Un bot fantastico creato per aiutarti!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Autore", value="OrionDev", inline=False)
        embed.add_field(name="Versione", value="1.0.0", inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
