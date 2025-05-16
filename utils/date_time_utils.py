from datetime import datetime
from zoneinfo import ZoneInfo

def parse_date_time(date_time:str) -> str:
    """
    Recebe uma string contendo data e hora e converte para date_time [...]
    """
    date_time = datetime.strptime(date_time, "%d/%m/%Y %H:%M")
    date_time_with_timezone = date_time.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))
    date_time_utc = date_time_with_timezone.astimezone(ZoneInfo("UTC"))
    return date_time_utc.strftime("%d/%m/%YT%H:%M:%SZ")