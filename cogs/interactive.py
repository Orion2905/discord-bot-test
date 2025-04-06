import discord
from discord.ext import commands

class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Premi qui!", style=discord.ButtonStyle.primary, emoji="🔘")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Hai premuto il pulsante, {interaction.user.mention}!", ephemeral=True)

class MySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Opzione 1", description="Questa è la prima opzione.", emoji="1️⃣"),
            discord.SelectOption(label="Opzione 2", description="Questa è la seconda opzione.", emoji="2️⃣"),
            discord.SelectOption(label="Opzione 3", description="Questa è la terza opzione.", emoji="3️⃣"),
        ]

        super().__init__(placeholder="Scegli un'opzione...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hai scelto {self.values[0]}", ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(MySelect())

class Interactive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="pulsante", help="Mostra un pulsante interattivo.")
    async def pulsante(self, ctx):
        view = ButtonView()
        await ctx.send("Clicca il pulsante qui sotto!", view=view)
    
    @commands.command(name="menu", help="Mostra un menu a tendina interattivo.")
    async def menu(self, ctx):
         view = DropdownView()
         await ctx.send("Seleziona un'opzione:", view=view)

async def setup(bot):
    await bot.add_cog(Interactive(bot))