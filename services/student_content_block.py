from sqlalchemy.orm import Session
from schema.student_content_block import (
    StudentContentBlockCreate, 
    StudentContentBlockUpdate
)
from models import ContentBlock, Course, StudentContentBlock

def create_student_content_block(db: Session, student_content_block: StudentContentBlockCreate):
    db_student_content_block = StudentContentBlock(**student_content_block.dict())
    db.add(db_student_content_block)
    db.commit()
    db.refresh(db_student_content_block)
    return db_student_content_block

def update_student_content_block(db: Session, student_content_block_id: int, student_content_block: StudentContentBlockUpdate):
    db_student_content_block = db.query(StudentContentBlock).filter(StudentContentBlock.id == student_content_block_id).first()
    if db_student_content_block:
        for key, value in student_content_block.dict(exclude_unset=True).items():
            setattr(db_student_content_block, key, value)
        db.commit()
        db.refresh(db_student_content_block)
    return db_student_content_block

def delete_student_content_block(db: Session, student_content_block_id: int):
    db_student_content_block = db.query(StudentContentBlock).filter(StudentContentBlock.id == student_content_block_id).first()
    if db_student_content_block:
        db.delete(db_student_content_block)
        db.commit()
    return db_student_content_block

def get_student_content_block(db: Session, student_content_block_id: int):
    return db.query(StudentContentBlock).filter(StudentContentBlock.id == student_content_block_id).first()

def get_student_content_blocks_by_student(db: Session, student_id: int):
    return db.query(StudentContentBlock).filter(StudentContentBlock.student_id == student_id).all()

def get_student_content_blocks_by_content_block(db: Session, content_block_id: int):
    return db.query(StudentContentBlock).filter(StudentContentBlock.content_block_id == content_block_id).all()




def initialize_student_content_blocks(db: Session, student_id: int, course_id: int):
    # Fetch all content blocks associated with the course
    content_blocks = db.query(ContentBlock).filter(ContentBlock.section.has(Course.id == course_id)).all()
    
    for block in content_blocks:
        # Check if the student content block already exists
        existing_record = db.query(StudentContentBlock).filter_by(
            student_id=student_id,
            content_block_id=block.id
        ).first()

        if existing_record is None:
            # Create a new StudentContentBlock record if it doesn't exist
            student_content_block = StudentContentBlock(
                student_id=student_id,
                content_block_id=block.id
            )
            db.add(student_content_block)

    # Commit the changes to the database
    db.commit()