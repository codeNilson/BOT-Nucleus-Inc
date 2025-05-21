import os
import logging
from logging.handlers import TimedRotatingFileHandler
import discord


def setup_discord_logger():
    log_path = os.getenv("LOG_PATH", "logs/discord.log")
    log_rotation_when = os.getenv("LOG_ROTATION_WHEN", "midnight")
    log_rotation_interval = int(os.getenv("LOG_ROTATION_INTERVAL", "1"))
    log_backup_count = int(os.getenv("LOG_BACKUP_COUNT", "7"))
    log_encoding = os.getenv("LOG_DEFAULT_ENCODING", "utf-8")
    log_level = os.getenv("LOG_LEVEL", "DEBUG")

    # os.makedirs(os.path.dirname(log_path), exist_ok=True)

    handler = TimedRotatingFileHandler(
        log_path,
        when=log_rotation_when,
        interval=log_rotation_interval,
        backupCount=log_backup_count,
        encoding=log_encoding,
    )

    handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s: %(message)s")

    discord.utils.setup_logging(handler=handler, formatter=formatter)
