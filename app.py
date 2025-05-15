import os
from discord import Intents
from discord.ext import commands
from core.nucleus_bot import NucleusBot

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = Intents.all()

bot = NucleusBot(
    command_prefix=commands.when_mentioned,
    intents=intents,
)

bot.run(DISCORD_TOKEN)
