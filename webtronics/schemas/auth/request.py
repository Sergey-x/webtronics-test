import pydantic as pd
from settings import SETTINGS


class BaseCredentialsRequestSchema(pd.BaseModel):
    email: str
    password: str = pd.Field(min_length=SETTINGS.MIN_PSW_LEN)
    # TODO: add validators


class SignUpRequestSchema(BaseCredentialsRequestSchema):
    pass


class SignInRequestSchema(BaseCredentialsRequestSchema):
    pass
