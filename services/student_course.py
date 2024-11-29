from fastapi import HTTPException
from sqlalchemy.orm import Session
from schema.student_course import StudentCourseCreate, StudentCourseUpdate
from models import ContentBlock, StudentContentBlock, StudentCourse




def update_student_course(db: Session, student_course_id: int, student_course: StudentCourseUpdate):
    db_student_course = db.query(StudentCourse).filter(StudentCourse.id == student_course_id).first()
    if not db_student_course:
        raise HTTPException(status_code=404, detail="Student course not found")

    # Check if the status needs to be updated
    for key, value in student_course.dict(exclude_unset=True).items():
        setattr(db_student_course, key, value)

    # If completed flag is set, validate content block completion
    if db_student_course.completed:
        progress_data = get_course_progress(db=db, student_id=db_student_course.student_id, course_id=db_student_course.course_id)
        if progress_data["completed"] < progress_data["total"]:
            raise HTTPException(status_code=400, detail="Cannot mark course as completed until all content blocks are completed")

    db.commit()
    db.refresh(db_student_course)

    return db_student_course



def get_course_progress(db: Session, student_id: int, course_id: int):
    # Get the total number of content blocks in the course
    total_blocks = db.query(ContentBlock).join(ContentBlock.section).filter(
        ContentBlock.section.has(course_id=course_id)
    ).count()

    # Get the number of completed content blocks by the student
    completed_blocks = db.query(StudentContentBlock).filter(
        StudentContentBlock.student_id == student_id,
        StudentContentBlock.content_block_id.in_(
            db.query(ContentBlock.id).join(ContentBlock.section).filter(
                ContentBlock.section.has(course_id=course_id)
            )
        ),
        StudentContentBlock.completed == True
    ).count()

    progress = (completed_blocks / total_blocks) * 100 if total_blocks > 0 else 0

    return {
        "progress": progress,
        "completed": completed_blocks,
        "total": total_blocks
    }





def delete_student_course(db: Session, student_course_id: int):
    db_student_course = db.query(StudentCourse).filter(StudentCourse.id == student_course_id).first()
    if db_student_course:
        db.delete(db_student_course)
        db.commit()
    return db_student_course

def get_student_course(db: Session, student_course_id: int):
    return db.query(StudentCourse).filter(StudentCourse.id == student_course_id).first()

def get_student_courses_by_student(db: Session, student_id: int):
    return db.query(StudentCourse).filter(StudentCourse.student_id == student_id).all()

def get_student_courses_by_course(db: Session, course_id: int):
    return db.query(StudentCourse).filter(StudentCourse.course_id == course_id).all()


