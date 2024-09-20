from typing import List
from sqlalchemy.orm import Session
from schema.course import CourseCreate, CourseUpdate
from models import Course
from fastapi import HTTPException

def create_course(db: Session, course_data: dict) -> Course:
    # Check if course with the same title exists
    existing_course = db.query(Course).filter(Course.title == course_data['title']).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course with this title already exists")
    
    db_course = Course(**course_data)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, course_id: int, course: CourseUpdate) -> Course:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if updating to a title that already exists
    if course.title and course.title != db_course.title:
        existing_course = db.query(Course).filter(Course.title == course.title).first()
        if existing_course:
            raise HTTPException(status_code=400, detail="Another course with this title already exists")

    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course

def delete_course(db: Session, course_id: int) -> Course:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(db_course)
    db.commit()
    return db_course

def get_course(db: Session, course_id: int) -> Course:
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

def get_courses(db: Session, skip: int = 0, limit: int = 10) -> List[Course]:
    return db.query(Course).offset(skip).limit(limit).all()

def get_courses_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Course]:
    return db.query(Course).filter(Course.user_id == user_id).offset(skip).limit(limit).all()
