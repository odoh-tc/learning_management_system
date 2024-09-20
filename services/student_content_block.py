from fastapi import HTTPException
from sqlalchemy.orm import Session
from schema.student_content_block import (
    StudentContentBlockCreate, 
    StudentContentBlockUpdate
)
from models import ContentBlock, Course, StudentContentBlock, StudentCourse

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




# def initialize_student_content_blocks(db: Session, student_id: int, course_id: int):
#     # Fetch all content blocks associated with the course
#     content_blocks = db.query(ContentBlock).filter(ContentBlock.section.has(Course.id == course_id)).all()
    
#     for block in content_blocks:
#         # Check if the student content block already exists
#         existing_record = db.query(StudentContentBlock).filter_by(
#             student_id=student_id,
#             content_block_id=block.id
#         ).first()

#         if existing_record is None:
#             # Create a new StudentContentBlock record if it doesn't exist
#             student_content_block = StudentContentBlock(
#                 student_id=student_id,
#                 content_block_id=block.id
#             )
#             db.add(student_content_block)

#     # Commit the changes to the database
#     db.commit()

def initialize_student_content_blocks(db: Session, student_id: int, course_id: int):
    # Get the student course record
    student_course = db.query(StudentCourse).filter(
        StudentCourse.student_id == student_id,
        StudentCourse.course_id == course_id
    ).first()

    if not student_course:
        raise HTTPException(status_code=404, detail="Student course record not found")

    # Check if the student has already completed the course
    if student_course.completed:
        # Add the new content block as optional without changing the course completion status
        new_content_blocks = db.query(ContentBlock).filter(
            ContentBlock.section.has(course_id=course_id),
            ContentBlock.id.notin_(
                db.query(StudentContentBlock.content_block_id).filter(
                    StudentContentBlock.student_id == student_id
                )
            )
        ).all()

        for block in new_content_blocks:
            student_content_block = StudentContentBlock(
                student_id=student_id,
                content_block_id=block.id,
                completed=False,  # New content is optional
                optional=True     # Mark it as optional
            )
            db.add(student_content_block)

        db.commit()
        return
    


    # If not completed, proceed with the standard behavior
    new_content_blocks = db.query(ContentBlock).filter(
        ContentBlock.section.has(course_id=course_id),
        ContentBlock.id.notin_(
            db.query(StudentContentBlock.content_block_id).filter(
                StudentContentBlock.student_id == student_id
            )
        )
    ).all()

    for block in new_content_blocks:
        student_content_block = StudentContentBlock(
            student_id=student_id,
            content_block_id=block.id,
            completed=False  # Standard behavior for students not yet completed
        )
        db.add(student_content_block)

    db.commit()
