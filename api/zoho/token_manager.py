from contextlib import asynccontextmanager
from datetime import datetime, timedelta

import aiohttp
from settings.configs import Config
from logs.logger import LOGGER
from errors.api_connection_error import APIConnectionError


class TokenManager:
    def __init__(self):
        self.tokens = {
            "access_token": None,
            "expires_in": None,
        }

    async def get_access_token(self) -> str:
        if self._access_token_is_expired():
            LOGGER.info("Access token expired, refreshing...")
            await self._update_access_token()
        return self.tokens["access_token"]  # type: ignore

    def _access_token_is_expired(self):
        """Verifica se o token de acesso está expirado ou não."""
        if (
            self.tokens["expires_in"] is None
            or self.tokens["expires_in"] < datetime.now()
        ):
            return True
        return False

    async def _update_access_token(self):
        async with self._get_session() as session:
            async with session.post(Config.ZOHO_ENDPOINT) as response:
                if response.status == 200:
                    LOGGER.info("Successfully retrieved access token.")

                    # Pega a resposta JSON e transforma em um dicionário
                    data: dict = await response.json()

                    # Atualiza o token de acesso e o tempo de expiração
                    self.tokens["access_token"] = data.get("access_token")
                    token_timeout: int = data.get("expires_in")  # type: ignore

                    # Guarda em expires_in o tempo atual + o tempo de expiração
                    # para comparação em _access_token_is_expired()
                    self.tokens["expires_in"] = datetime.now() + timedelta(  # type: ignore
                        seconds=token_timeout
                    )
                    return
                # Se a resposta não for 200, lança um erro que será tratado
                # no método on_app_commands_error do bot
                LOGGER.error("Failed to retrieve access token: %s.", response.status)
                raise APIConnectionError(
                    f"Failed to retrieve access token: {response.status}."
                )

    @asynccontextmanager
    async def _get_session(self, headers=None):
        headers = headers or {"Authorization": f"Bearer {Config.ZOHO_REFRESH_TOKEN}"}
        async with aiohttp.ClientSession(headers=headers) as session:
            yield session
