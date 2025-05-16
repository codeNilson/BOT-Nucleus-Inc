from datetime import datetime
from zoneinfo import ZoneInfo


def parse_date_time(date_time: str) -> datetime:
    """
    Recebe uma string contendo data e hora e converte para date_time [...]
    """
    try:
        date_time = datetime.strptime(date_time, "%d/%m/%Y %H:%M")
    except ValueError as exc:
        raise ValueError(
            "Formato inválido. Use o formato: DD/MM/AAAA HH:MM"
        ) from exc
    date_time_with_timezone = date_time.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))
    # date_time_utc = date_time_with_timezone.astimezone(ZoneInfo("UTC"))
    return date_time_with_timezone
