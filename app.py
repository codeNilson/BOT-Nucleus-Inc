from discord import Intents
from discord.ext import commands
from core.nucleus_bot import NucleusBot
from logs.config import setup_discord_logger
from logs.logger import LOGGER

from settings.configs import Config


def get_discord_token() -> str:
    """
    Obtém o token do Discord a partir da variável de ambiente DISCORD_TOKEN.
    Se a variável de ambiente não estiver definida, levanta um ValueError.
    """

    DISCORD_TOKEN = Config.DISCORD_TOKEN

    if not DISCORD_TOKEN:
        LOGGER.error(
            "O token do Discord não foi encontrado. Defina a variável de ambiente DISCORD_TOKEN."
        )
        raise ValueError(
            "O token do Discord não foi encontrado. Defina a variável de ambiente DISCORD_TOKEN."
        )
    return DISCORD_TOKEN


def start_bot() -> None:
    """
    Inicia o bot do Discord.
    """
    intents = Intents.all()

    bot = NucleusBot(
        command_prefix=commands.when_mentioned,
        intents=intents,
    )

    discord_token = get_discord_token()

    bot.run(discord_token)


def main():
    """
    Função principal que configura o logger e inicia o bot do Discord.
    """

    setup_discord_logger()

    start_bot()


if __name__ == "__main__":
    main()
