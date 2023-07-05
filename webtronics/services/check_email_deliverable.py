import neverbounce_sdk
from settings import SETTINGS


async def check_email_deliverable(email: str) -> bool:
    client = neverbounce_sdk.client(api_key=SETTINGS.NEVERBOUNCE_API_KEY, timeout=30)
    resp = client.single_check(email)
    verified: bool = resp["result"] == "valid"
    return verified
