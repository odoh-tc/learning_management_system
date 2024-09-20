from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ContentType(str, Enum):
    video = "video"
    text = "text"
    quiz = "quiz"

# class ContentBlockBase(BaseModel):
#     title: str
#     description: Optional[str] = None
#     type: ContentType
#     url: Optional[str] = None
#     content: Optional[str] = None


class ContentBlockBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: ContentType = Field(..., description="Type of content block: video, text, or quiz")
    url: Optional[str] = None
    content: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

class ContentBlockCreate(ContentBlockBase):
    section_id: int

class ContentBlockUpdate(ContentBlockBase):
    pass

class ContentBlockResponse(ContentBlockBase):
    id: int
    section_id: int
    student_content_blocks: Optional[List["StudentContentBlockResponse"]]

    class Config:
        orm_mode = True

from .student_content_block import StudentContentBlockResponse
