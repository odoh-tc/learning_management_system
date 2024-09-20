from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
from schema.student_course import StudentCourseCreate, StudentCourseUpdate, StudentCourseResponse
from services.auth import get_current_user
from services.student_course import (
    get_course_progress,
    update_student_course,
    delete_student_course,
    get_student_course,
    get_student_courses_by_student,
    get_student_courses_by_course
)
from models import User
from typing import List

router = APIRouter()

# @router.post("/student_courses/", response_model=StudentCourseResponse)
# def create_new_student_course(student_course: StudentCourseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     if current_user.role != 'student':
#         raise HTTPException(status_code=403, detail="Not enough permissions")
#     return create_student_course(db=db, student_course=student_course)

# @router.put("/student_courses/{student_course_id}", response_model=StudentCourseResponse)
# def update_existing_student_course(student_course_id: int, student_course: StudentCourseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     db_student_course = get_student_course(db=db, student_course_id=student_course_id)
#     if not db_student_course:
#         raise HTTPException(status_code=404, detail="Student course not found")
#     if current_user.role == 'student' and db_student_course.student_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not allowed to update this course")
#     return update_student_course(db=db, student_course_id=student_course_id, student_course=student_course)

@router.put("/student_courses/{student_course_id}", response_model=StudentCourseResponse)
def update_existing_student_course(
    student_course_id: int,
    student_course: StudentCourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_student_course = get_student_course(db=db, student_course_id=student_course_id)
    if not db_student_course:
        raise HTTPException(status_code=404, detail="Student course not found")
    
    # Allow admins and teachers to update any student course
    if current_user.role == 'student' and db_student_course.student_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to update this course")
    
    # Update the student course
    updated_student_course = update_student_course(db=db, student_course_id=student_course_id, student_course=student_course)
    
    return updated_student_course



@router.get("/student_courses/progress/{student_id}/{course_id}")
def get_course_progress_endpoint(
    student_id: int,
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Allow admins and teachers to view progress for any student
    if current_user.role not in ['student', 'admin', 'teacher'] and current_user.id != student_id:
        raise HTTPException(status_code=403, detail="Not allowed to access this progress")

    # Get and return the course progress
    progress_data = get_course_progress(db=db, student_id=student_id, course_id=course_id)
    return progress_data




@router.delete("/student_courses/{student_course_id}", status_code=204)
def delete_existing_student_course(student_course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_student_course = get_student_course(db=db, student_course_id=student_course_id)
    if not db_student_course:
        raise HTTPException(status_code=404, detail="Student course not found")
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not enough permissions")
    delete_student_course(db=db, student_course_id=student_course_id)
    return Response(status_code=204)


@router.get("/student_courses/{student_course_id}", response_model=StudentCourseResponse)
def read_student_course(student_course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_student_course = get_student_course(db=db, student_course_id=student_course_id)
    if not db_student_course:
        raise HTTPException(status_code=404, detail="Student course not found")
    return db_student_course

@router.get("/student_courses/student/{student_id}", response_model=List[StudentCourseResponse])
def read_student_courses_by_student(student_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ['student', 'admin']:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return get_student_courses_by_student(db=db, student_id=student_id)

@router.get("/student_courses/course/{course_id}", response_model=List[StudentCourseResponse])
def read_student_courses_by_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ['teacher', 'admin']:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return get_student_courses_by_course(db=db, course_id=course_id)
