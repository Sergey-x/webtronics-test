import pydantic as pd


class CreatePostRequestSchema(pd.BaseModel):
    text: str = pd.Field(description="Текст")


class UpdatePostRequestSchema(pd.BaseModel):
    text: str
