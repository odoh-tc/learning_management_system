from pydantic import BaseModel
from typing import Optional, List

from schema.section import SectionResponse
from schema.student_course import StudentCourseResponse

# from .user import UserResponse  # Import UserResponse here

class CourseBase(BaseModel):
    title: str
    description: str
    category_id: Optional[int] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    sections: Optional[List[SectionResponse]]
    student_courses: Optional[List[StudentCourseResponse]]
    category_id: Optional[int]

    class Config:
        orm_mode = True
        exclude_unset = True
        from_attributes = True


class CourseCreateResponse(CourseBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True
        exclude_unset = True  # This line is added to prevent recursion



# from pydantic import BaseModel
# from typing import Optional, List, TYPE_CHECKING

# if TYPE_CHECKING:
#     from .user import UserResponse
#     from .section import SectionResponse
#     from .student_course import StudentCourseResponse
#     from .category import CategoryResponse

# class CourseBase(BaseModel):
#     title: str
#     description: str
#     category_id: Optional[int] = None

# class CourseCreate(CourseBase):
#     pass

# class CourseUpdate(CourseBase):
#     pass

# class CourseResponse(CourseBase):
#     id: int
#     created_by: Optional["UserResponse"] = None
#     sections: Optional[List["SectionResponse"]] = []
#     student_courses: Optional[List["StudentCourseResponse"]] = []
#     category: Optional["CategoryResponse"] = None

#     class Config:
#         orm_mode = True
#         from_attributes = True
#         exclude_unset = True  # This line is added to prevent recursion

# class CourseCreateResponse(CourseBase):
#     id: int
#     user_id: int

#     class Config:
#         orm_mode = True
#         from_attributes = True
#         exclude_unset = True  # This line is added to prevent recursion

