import discord
from discord.ext import commands
from discord import app_commands
from core.components.modal import CreateEventModal
from logs.logger import LOGGER


class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.startswith("ping"):
            LOGGER.debug("Comando de ping recebido de %s", message.author.name)
            await message.channel.send("Pong!")

    @app_commands.command(name="create_event", description="Cria um novo evento")
    async def create_event(
        self,
        interaction: discord.Interaction,
        channel: discord.VoiceChannel,
    ):
        LOGGER.debug(
            "Comando de criar evento recebido de %s no canal %s",
            interaction.user.name,
            channel.name,
        )
        modal = CreateEventModal(channel)
        await interaction.response.send_modal(modal)


async def setup(bot: commands.Bot):
    """Função de configuração do cog Admin. Chamado por .load_extension() no setup_hook do bot."""
    await bot.add_cog(AdminCog(bot))
