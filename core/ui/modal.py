from datetime import datetime
from typing import Optional
import discord
from discord.ui import TextInput
from discord.errors import HTTPException

from utils.date_time_utils import parse_date_time


class CreateEventModal(discord.ui.Modal):
    """
    Modal personalizado para registrar um novo evento via Discord.

    Campos:
    - Título do evento
    - Descrição
    - Data e hora
    """

    def __init__(
        self,
        channel: discord.VoiceChannel,
        *,
        title: str = "Registrar Novo Evento",
        timeout: Optional[float] = 30,
    ):
        super().__init__(title=title, timeout=timeout)

        self.channel = channel
        self.event_name = TextInput(
            label="Título do Evento",
        )
        self.date_time = TextInput(
            label="Data e hora",
            placeholder=datetime.now().strftime("%d/%m/%Y %H:%M"),
        )
        self.description = TextInput(
            label="Descrição",
            style=discord.TextStyle.paragraph,
            required=False,
        )

        self.add_item(self.event_name)
        self.add_item(self.date_time)
        self.add_item(self.description)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Método chamado quando o modal é enviado.
        Args:
            self: Instância do modal.
            interaction: Interação do Discord.
        Returns:
            None
        """
        guild = interaction.guild
        try:
            await guild.create_scheduled_event(
                name=self.event_name.value,
                start_time=parse_date_time(self.date_time.value),
                description=self.description.value,
                entity_type=discord.EntityType.voice,
                privacy_level=discord.PrivacyLevel.guild_only,
                channel=self.channel,
            )
        except ValueError:
            await interaction.response.send_message(
                "❌ O campo 'Data e hora' não está no formato correto.\
                \nPor favor, use o formato: DD/MM/AAAA HH:MM",
                ephemeral=True,
            )
            return
        except HTTPException as exc:
            if exc.status == 400 and exc.code == 50035:
                await interaction.response.send_message(
                    f"❌ O campo 'Data e hora' não podem estar no passado.\nData e hora informados: {self.date_time.value}.",
                    ephemeral=True,
                )
                return
        msg = f"Título: {self.event_name.value}\nDescrição: {self.description.value}\nData e hora: {self.date_time.value}."
        await interaction.response.send_message(msg, ephemeral=True)
