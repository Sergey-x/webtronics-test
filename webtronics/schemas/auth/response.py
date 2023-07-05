import pydantic as pd


class JWTPair(pd.BaseModel):
    access_token: str
    refresh_token: str
