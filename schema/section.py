from pydantic import BaseModel
from typing import List, Optional
from .content_block import ContentBlockResponse


class SectionBase(BaseModel):
    title: str
    description: str

class SectionCreate(SectionBase):
    course_id: int

class SectionUpdate(SectionBase):
    pass

class SectionResponse(SectionBase):
    id: int
    # content_blocks: Optional[List["ContentBlockResponse"]]
    content_blocks: Optional[List[ContentBlockResponse]]

    class Config:
        orm_mode = True
        from_attributes = True


# from .content_block import ContentBlockResponse
