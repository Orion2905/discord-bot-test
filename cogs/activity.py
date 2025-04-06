import discord
from discord.ext import commands, tasks
from database import track_presence, get_top_users, get_or_create_presence

class ActivityTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.track_activity.start()
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Aggiungi al database se non esiste

        get_or_create_presence(member.id)

        print(f"🎉 {member.name} è stato registrato nel database.")


    @tasks.loop(seconds=60)
    async def track_activity(self):
        print("🔄 Inizio monitoraggio attività...")
        
        # Lista dei ruoli e soglie temporali
        soglie_ruoli = [
            ("Appena arrivato", 0),
            ("Attivo", 10),
            ("Molto Attivo", 60),
            ("Super Attivo", 300),
            ("Super Mega iper attivo", 4000),
        ]

        for guild in self.bot.guilds:
            for member in guild.members:
                print(f"Controllando {member.name}, {member.status}...")

                if member.status != discord.Status.offline and not member.bot:
                    print(f"🟢 {member.name} è attivo.")
                    track_presence(member.id)

                    # Tempo totale registrato
                    seconds = get_or_create_presence(member.id)
                    ruolo_assegnato = None

                    # Trova il ruolo corretto per il tempo attuale
                    for nome_ruolo, soglia in reversed(soglie_ruoli):
                        if seconds >= soglia:
                            ruolo_assegnato = nome_ruolo
                            break

                    if ruolo_assegnato:
                        # Rimuovi eventuali ruoli precedenti legati all'attività
                        for nome, _ in soglie_ruoli:
                            ruolo = discord.utils.get(guild.roles, name=nome)
                            if ruolo and ruolo in member.roles and nome != ruolo_assegnato:
                                await member.remove_roles(ruolo)
                                print(f"❌ Rimosso ruolo {nome} da {member.name}")

                        # Crea il ruolo se non esiste
                        ruolo_finale = discord.utils.get(guild.roles, name=ruolo_assegnato)
                        if not ruolo_finale:
                            try:
                                ruolo_finale = await guild.create_role(name=ruolo_assegnato, reason="Creato automaticamente dal bot")
                                print(f"🔧 Creato ruolo {ruolo_assegnato}")
                            except discord.Forbidden:
                                print(f"⚠️ Permessi insufficienti per creare ruoli in {guild.name}")
                                continue

                        # Assegna il ruolo corretto
                        if ruolo_finale not in member.roles:
                            try:
                                await member.add_roles(ruolo_finale)
                                print(f"🏅 {member.name} ha ricevuto il ruolo '{ruolo_assegnato}'")
                            except discord.Forbidden:
                                print(f"❌ Non posso assegnare il ruolo a {member.name}")


    @commands.command(name="classifica", help="Mostra i membri più attivi.")
    async def classifica(self, ctx):
        top_users = get_top_users()
        lines = []
        for i, (user_id, seconds) in enumerate(top_users, 1):
            member = ctx.guild.get_member(user_id)
            name = member.name if member else f"Utente {user_id}"
            minuti = seconds // 60
            lines.append(f"{i}. {name} - {minuti} minuti")

        await ctx.send("🏆 **Classifica Attività** 🏆\n" + "\n".join(lines))

async def setup(bot):
    await bot.add_cog(ActivityTracker(bot))
