from pydantic import BaseModel

class StudentCourseBase(BaseModel):
    student_id: int
    course_id: int
    completed: bool = False

class StudentCourseCreate(StudentCourseBase):
    pass

class StudentCourseUpdate(BaseModel):
    course_id: int
    # completed: bool = False

class StudentCourseResponse(StudentCourseBase):
    id: int

    class Config:
        orm_mode = True
