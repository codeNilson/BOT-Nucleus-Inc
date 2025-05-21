import json
import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo
from contextlib import asynccontextmanager

import aiohttp
from api.zoho.token_manager import TokenManager
from logs.logger import LOGGER
from settings.configs import Config


class ZohoClient:
    def __init__(self):
        self.token_manager = TokenManager()

    async def create_event(
        self,
        *,
        title: str,
        start_date: datetime,
        description: str,
        emails: list[str],
        discord_event_link: str,
    ):

        data = {
            "reminders": [{"action": "popup", "minutes": -60}],
            "dateandtime": {
                "timezone": "America/Sao_Paulo",
                "start": self._format_zoho_date(start_date),
                "end": self._format_zoho_date(start_date),
            },
            "title": title,
            "attendees": [
                {"email": email, "status": "NEEDS-ACTION"} for email in emails
            ],
            "richtext_description": description
            + f": \n\nLink do evento no Discord: ${discord_event_link}",
            "conference": "none",
        }

        formatted_data = json.dumps(data)
        encoded_data = urllib.parse.quote(formatted_data)

        endpoint = f"https://calendar.zoho.com/api/v1/calendars/{Config.ZOHO_CALENDAR_UID}/events?eventdata={encoded_data}"

        await self._make_request(endpoint=endpoint, data=encoded_data)

    async def _make_request(self, endpoint: str, data: str):
        access_token = await self.token_manager.get_access_token()  # type: ignore
        headers = {"Authorization": f"Bearer {access_token}"}

        async with self._get_session(headers) as session:
            async with session.post(endpoint, data=data) as response:
                if response.status == 200:
                    LOGGER.info("Successfully created event on Zoho Calendar.")
                    return
                LOGGER.error("Failed to create event. Status code: %s", response.status)

    @asynccontextmanager
    async def _get_session(self, headers):
        async with aiohttp.ClientSession(headers=headers) as session:
            yield session

    def _format_zoho_date(self, date: datetime) -> str:
        """
        Formata a data para o formato esperado pela API do Zoho.
        """
        date_utc = date.astimezone(ZoneInfo("UTC"))
        return date_utc.strftime("%Y%m%dT%H%M%SZ")
