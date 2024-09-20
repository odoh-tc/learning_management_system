# from pydantic import BaseModel, EmailStr
# from enum import Enum
# from typing import List, Optional

# from .course import CourseResponse  # Adjust the import path as necessary


# class Role(str, Enum):
#     admin = "admin"
#     teacher = "teacher"
#     student = "student"

# class UserBase(BaseModel):
#     email: EmailStr
#     username: str
#     role: Role
#     is_active: bool

# class UserCreate(UserBase):
#     password: str

# class AdminResponse(UserBase):
#     id: int
#     profile: Optional["ProfileResponse"]


#     class Config:
#         orm_mode = True
#         from_attributes = True  # Add this line

# class TeacherResponse(UserBase):
#     id: int
#     profile: Optional["ProfileResponse"]
#     created_courses: Optional[List[CourseResponse]]

#     class Config:
#         orm_mode = True
#         from_attributes = True  # Add this line


# class UserResponse(UserBase):
#     profile: Optional["ProfileResponse"]


#     class Config:
#         orm_mode = True
#         from_attributes = True  # Add this line



# class StudentResponse(UserBase):
#     id: int
#     profile: Optional["ProfileResponse"]
#     student_courses: Optional[List["StudentCourseResponse"]]
#     student_content_blocks: Optional[List["StudentContentBlockResponse"]]

#     class Config:
#         orm_mode = True
#         from_attributes = True  # Add this line


# from .profile import ProfileResponse
# from .course import CourseResponse
# from .student_course import StudentCourseResponse
# from .student_content_block import StudentContentBlockResponse


from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List, Optional

from schema.student_content_block import StudentContentBlockResponse
from schema.student_course import StudentCourseResponse

from .profile import ProfileResponse
from .course import CourseResponse  # Import CourseResponse here


class Role(str, Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: Role

class UserCreate(UserBase):
    password: str

class AdminResponse(UserBase):
    id: int
    is_active: bool  # Include in responses

    profile: Optional[ProfileResponse]

    class Config:
        orm_mode = True
        from_attributes = True

class TeacherResponse(UserBase):
    id: int
    is_active: bool  # Include in responses

    profile: Optional[ProfileResponse]
    # created_courses: Optional[List["CourseResponse"]]  # Import CourseResponse here
    created_courses: List[CourseResponse]


    class Config:
        orm_mode = True
        from_attributes = True

class UserResponse(UserBase):
    # id: int
    is_active: bool  # Include in responses
    profile: Optional[ProfileResponse]

    class Config:
        orm_mode = True
        from_attributes = True


# class UserResponse(UserBase):
#     profile: Optional[ProfileResponse]

#     class Config:
#         orm_mode = True
#         from_attributes = True

class StudentResponse(UserBase):
    id: int
    is_active: bool  # Include in responses

    profile: Optional[ProfileResponse]
    student_courses: Optional[List["StudentCourseResponse"]]
    student_content_blocks: Optional[List["StudentContentBlockResponse"]]

    class Config:
        orm_mode = True
        from_attributes = True

