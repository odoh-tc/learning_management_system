from pydantic import BaseModel
from typing import List, Optional

# Import CourseResponse here to avoid NameError
from .course import CourseResponse

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

# class CategoryResponse(CategoryBase):
#     id: int
#     courses: Optional[List["CourseResponse"]]

#     class Config:
#         orm_mode = True

class CategoryResponse(BaseModel):
    id: int
    name: str
    # courses: Optional[List[CourseResponse]]  # Use CourseResponse directly here

    class Config:
        orm_mode = True


# from .course import CourseResponse
