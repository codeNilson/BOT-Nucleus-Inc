import os
from discord import Intents
from discord.ext import commands
from core.nucleus_bot import NucleusBot


def main():
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", None)

    intents = Intents.all()

    bot = NucleusBot(
        command_prefix=commands.when_mentioned,
        intents=intents,
    )

    if not DISCORD_TOKEN:
        raise ValueError(
            "O token do Discord não foi encontrado. Defina a variável de ambiente DISCORD_TOKEN."
        )
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
