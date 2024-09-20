from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schema.content_block import ContentBlockCreate, ContentBlockUpdate, ContentBlockResponse
from services.auth import get_current_user
from services.content_block import (
    create_content_block,
    update_content_block,
    delete_content_block,
    get_content_block,
    get_content_blocks_by_section
)
from models import Course, Section, StudentCourse, User
from typing import List

from services.student_content_block import initialize_student_content_blocks

router = APIRouter()

@router.post("/content_blocks/", response_model=ContentBlockResponse)
def create_new_content_block(
    content_block: ContentBlockCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Only admins and teachers can create content blocks
    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Ensure the section exists
    section = db.query(Section).filter(Section.id == content_block.section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Create the content block linked to the section
    new_content_block = create_content_block(db=db, content_block=content_block)
    
    # Fetch all students enrolled in the course
    course = db.query(Course).filter(Course.id == section.course_id).first()
    enrolled_students = db.query(StudentCourse).filter(StudentCourse.course_id == course.id).all()
    
    # Sync the new content block to all enrolled students
    for enrollment in enrolled_students:
        initialize_student_content_blocks(db=db, student_id=enrollment.student_id, course_id=course.id)
    
    return new_content_block


@router.put("/content_blocks/{content_block_id}", response_model=ContentBlockResponse)
def update_existing_content_block(content_block_id: int, content_block: ContentBlockUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_content_block = get_content_block(db=db, content_block_id=content_block_id)
    if not db_content_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return update_content_block(db=db, content_block_id=content_block_id, content_block=content_block)

@router.delete("/content_blocks/{content_block_id}", response_model=ContentBlockResponse)
def delete_existing_content_block(content_block_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_content_block = get_content_block(db=db, content_block_id=content_block_id)
    if not db_content_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return delete_content_block(db=db, content_block_id=content_block_id)

@router.get("/content_blocks/{content_block_id}", response_model=ContentBlockResponse)
def read_content_block(content_block_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_content_block = get_content_block(db=db, content_block_id=content_block_id)
    if not db_content_block:
        raise HTTPException(status_code=404, detail="Content block not found")
    return db_content_block

@router.get("/content_blocks/section/{section_id}", response_model=List[ContentBlockResponse])
def read_content_blocks_by_section(section_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_content_blocks_by_section(db=db, section_id=section_id)
