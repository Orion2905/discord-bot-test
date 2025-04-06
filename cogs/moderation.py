import discord
from discord.ext import commands

class Moderation(commands.Cog):
    """Comandi di moderazione"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", help="Espelle un utente dal server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} è stato espulso.")

    @commands.command(name="ban", help="Banna un utente.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} è stato bannato dal server.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
