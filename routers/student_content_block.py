from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schema.student_content_block import StudentContentBlockCreate, StudentContentBlockUpdate, StudentContentBlockResponse
from models import User
from services.auth import get_current_user
from services.student_content_block import (
    create_student_content_block,
    update_student_content_block,
    delete_student_content_block,
    get_student_content_block,
    get_student_content_blocks_by_student,
    get_student_content_blocks_by_content_block
)
from typing import List

router = APIRouter()

# @router.post("/student_content_blocks/", response_model=StudentContentBlockResponse)
# def create_new_student_content_block(student_content_block: StudentContentBlockCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     if current_user.role == 'student':
#         # Automatically assign the student_id to the logged-in student
#         student_content_block.student_id = current_user.id
#         # Prevent the student from setting feedback or grade
#         student_content_block.feedback = None
#         student_content_block.grade = 0
#     elif current_user.role not in ['admin', 'teacher']:
#         raise HTTPException(status_code=403, detail="Not enough permissions")
    
#     return create_student_content_block(db=db, student_content_block=student_content_block)


@router.put("/student_content_blocks/{student_content_block_id}", response_model=StudentContentBlockResponse)
def update_existing_student_content_block(student_content_block_id: int, student_content_block: StudentContentBlockUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_student_content_block = get_student_content_block(db=db, student_content_block_id=student_content_block_id)
    if not db_student_content_block:
        raise HTTPException(status_code=404, detail="Student content block not found")
    
    if current_user.role == 'student':
        if db_student_content_block.student_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        # Students can only update `completed` and `url`
        if student_content_block.completed is not None:
            db_student_content_block.completed = student_content_block.completed
        if student_content_block.url is not None:
            db_student_content_block.url = student_content_block.url
    elif current_user.role in ['admin', 'teacher']:
        # Teachers and admins can update everything
        for key, value in student_content_block.dict(exclude_unset=True).items():
            setattr(db_student_content_block, key, value)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.commit()
    db.refresh(db_student_content_block)
    return db_student_content_block


@router.delete("/student_content_blocks/{student_content_block_id}")
def delete_existing_student_content_block(student_content_block_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_student_content_block = get_student_content_block(db=db, student_content_block_id=student_content_block_id)
    if not db_student_content_block:
        raise HTTPException(status_code=404, detail="Student content block not found")
    if current_user.role not in ['admin', 'teacher']:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return delete_student_content_block(db=db, student_content_block_id=student_content_block_id)


@router.get("/student_content_blocks/{student_content_block_id}", response_model=StudentContentBlockResponse)
def read_student_content_block(student_content_block_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_student_content_block = get_student_content_block(db=db, student_content_block_id=student_content_block_id)
    if not db_student_content_block:
        raise HTTPException(status_code=404, detail="Student content block not found")
    return db_student_content_block


@router.get("/student_content_blocks/student/{student_id}", response_model=List[StudentContentBlockResponse])
def read_student_content_blocks_by_student(student_id: int, db: Session = Depends(get_db)):
    return get_student_content_blocks_by_student(db=db, student_id=student_id)


@router.get("/student_content_blocks/content_block/{content_block_id}", response_model=List[StudentContentBlockResponse])
def read_student_content_blocks_by_content_block(content_block_id: int, db: Session = Depends(get_db)):
    return get_student_content_blocks_by_content_block(db=db, content_block_id=content_block_id)
