import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    ZOHO_CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
    ZOHO_CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
    ZOHO_REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
    ZOHO_REDIRECT_URI = os.getenv("ZOHO_REDIRECT_URI")
    ZOHO_CALENDAR_UID = os.getenv("ZOHO_CALENDAR_UID")
    ZOHO_ENDPOINT = (
        f"https://accounts.zoho.com/oauth/v2/token"
        f"?refresh_token={ZOHO_REFRESH_TOKEN}"
        f"&client_id={ZOHO_CLIENT_ID}"
        f"&client_secret={ZOHO_CLIENT_SECRET}"
        f"&grant_type=refresh_token"
        f"&scope=ZohoCalendar.event.ALL"
    )
