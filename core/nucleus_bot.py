from discord import Interaction
from discord import Intents
from discord.ext import commands
from errors.api_connection_error import APIConnectionError
from logs.logger import LOGGER


class NucleusBot(commands.Bot):
    def __init__(
        self,
        command_prefix=commands.when_mentioned,
        intents: Intents = Intents.default(),
    ):
        super().__init__(command_prefix=command_prefix, intents=intents)
        super().tree.on_error = self.on_app_commands_error

    async def on_ready(self):
        LOGGER.debug("Bot está online como %s", self.user.name)  # type: ignore
        print(f"Bot está online como {self.user.name}#{self.user.discriminator}")  # type: ignore

    async def on_app_commands_error(self, interaction: Interaction, error):
        """Método chamado quando um erro ocorre em um comando de aplicativo (slash command)."""
        if isinstance(error, APIConnectionError):
            await interaction.response.send_message(
                "❌ Erro de conexão com a API do ZOHO. Por favor, tente novamente mais tarde."
            )

        elif isinstance(error, Exception):
            await interaction.response.send_message(
                "❌ Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.",
                ephemeral=True,
            )

    async def setup_hook(self):
        """Método chamado antes do bot se conectar, para preparar carregamentos e sincronizações."""

        LOGGER.debug("Método setup_hook chamado.")

        # Carrega as extensões (cogs) do bot
        await self.load_extension("core.cogs.nucleus_admin_cog")

        # Registra os comandos de aplicativo (slash commands) no Discord
        await self.tree.sync()

        print("Comandos de aplicativo sincronizados.")
