from pydantic import BaseModel
from typing import Optional

class StudentContentBlockBase(BaseModel):
    content_block_id: int

class StudentContentBlockCreate(StudentContentBlockBase):
    pass

class StudentContentBlockUpdate(BaseModel):
    completed: Optional[bool] = None
    url: Optional[str] = None
    feedback: Optional[str] = None
    grade: Optional[int] = None

class StudentContentBlockResponse(StudentContentBlockBase):
    id: int
    student_id: int
    completed: bool
    url: Optional[str] = None
    feedback: Optional[str] = None
    grade: Optional[int] = None

    class Config:
        orm_mode = True
