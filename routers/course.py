from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schema.course import CourseCreate, CourseUpdate, CourseResponse
from services.auth import get_current_user
from services.course import create_course, update_course, delete_course, get_course, get_courses, get_courses_by_user
from models import User

router = APIRouter()

@router.post("/", response_model=CourseResponse)
def create_new_course(
    course: CourseCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    course_data = course.dict()
    course_data['user_id'] = current_user.id
    new_course = create_course(db=db, course_data=course_data)
    return new_course

@router.put("/{course_id}", response_model=CourseResponse)
def update_existing_course(
    course_id: int, 
    course: CourseUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_course = get_course(db=db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user.role not in ['admin', 'teacher'] or (current_user.role == 'teacher' and db_course.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_course = update_course(db=db, course_id=course_id, course=course)
    return updated_course

@router.delete("/{course_id}", response_model=CourseResponse)
def delete_existing_course(
    course_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_course = get_course(db=db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return delete_course(db=db, course_id=course_id)

@router.get("/{course_id}", response_model=CourseResponse)
def get_a_course(
    course_id: int, 
    db: Session = Depends(get_db)
):
    db_course = get_course(db=db, course_id=course_id)
    return db_course

@router.get("/", response_model=List[CourseResponse])
def read_courses(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    return get_courses(db=db, skip=skip, limit=limit)

@router.get("/user/{user_id}", response_model=List[CourseResponse])
def created_courses_by_user(
    user_id: int, 
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    courses = get_courses_by_user(db=db, user_id=user_id, skip=skip, limit=limit)
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found for this user")
    return courses
