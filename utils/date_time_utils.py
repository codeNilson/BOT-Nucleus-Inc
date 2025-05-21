from datetime import datetime
from zoneinfo import ZoneInfo
from logs.logger import LOGGER


def parse_date_time(date_time: str) -> datetime:
    """
    Recebe uma string contendo data e hora e converte para date_time [...]
    """
    try:
        parsed_date_time = datetime.strptime(date_time, "%d/%m/%Y %H:%M")
    except ValueError as exc:
        LOGGER.debug("Falha a converter a data e hora.")
        raise ValueError("Formato inválido. Use o formato: DD/MM/AAAA HH:MM") from exc
    date_time_with_timezone = parsed_date_time.replace(
        tzinfo=ZoneInfo("America/Sao_Paulo")
    )
    # como converter para UTC
    # date_time_with_timezone = date_time_with_timezone.astimezone(ZoneInfo("UTC"))
    return date_time_with_timezone
