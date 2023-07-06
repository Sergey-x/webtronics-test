from datetime import datetime

import pydantic as pd


class PostResponseItem(pd.BaseModel):
    id: int
    dt_created: datetime | str
    dt_updated: None | datetime | str
    text: str
    is_available: bool
    author_id: int
    likes: int
