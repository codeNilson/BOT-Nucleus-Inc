import os
import logging
from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger("nucleus-inc")
LOGGER.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))
