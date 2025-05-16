import discord

class CreateEventModal(discord.ui.Modal):
    def __init__(
        self,
        *,
        title: str = "Registrar Novo Evento",
        timeout: Optional[float] = 30,
        ):
        super().__init__(title=title, timeout=timeout)
        
        self.event_name = TextInput(label="Título do Evento")
        self.description = TextInput(label="Descrição", style=discord.TextStyle.paragraph)
        self.date_time = TextInput(label="Data e hora", style=discord.TextStyle.paragraph)

        self.add_item(self.event_name)
        self.add_item(self.description)
        self.add_item(self.date_time)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        pass