import bot
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    bot.bot.run(TOKEN)
