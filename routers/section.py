from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schema.section import SectionCreate, SectionUpdate, SectionResponse
from services.auth import get_current_user
from services.section import create_section, update_section, delete_section, get_section, get_sections_by_course
from models import Course, User, Section

router = APIRouter()

@router.post("/", response_model=SectionResponse)
def create_new_section(section: SectionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the user has the right permissions
    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Check if the course exists
    course = db.query(Course).filter(Course.id == section.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if a section with the same title already exists for this course
    existing_section = db.query(Section).filter(Section.title == section.title, Section.course_id == section.course_id).first()
    if existing_section:
        raise HTTPException(status_code=400, detail="A section with this title already exists for this course")
    
    return create_section(db=db, section=section)


@router.put("/{section_id}", response_model=SectionResponse)
def update_existing_section(section_id: int, section: SectionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the section exists
    db_section = get_section(db=db, section_id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Check if the user has the right permissions
    if current_user.role not in ['admin', 'teacher'] or (current_user.role == 'teacher' and db_section.course.created_by.id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return update_section(db=db, section_id=section_id, section=section)

@router.delete("/{section_id}", response_model=SectionResponse)
def delete_existing_section(section_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the section exists
    db_section = get_section(db=db, section_id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Check if the user has the right permissions
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return delete_section(db=db, section_id=section_id)

@router.get("/{section_id}", response_model=SectionResponse)
def read_section(section_id: int, db: Session = Depends(get_db)):
    db_section = get_section(db=db, section_id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    return db_section

@router.get("/course/{course_id}", response_model=List[SectionResponse])
def read_sections_by_course(course_id: int, db: Session = Depends(get_db)):
    # Check if the course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return get_sections_by_course(db=db, course_id=course_id)
