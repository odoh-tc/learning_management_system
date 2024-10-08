from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Payment, User, StudentCourse, Course
from schema.student_course import StudentCourseResponse
from schema.user import Role
from services.auth import get_current_user
from services.student_content_block import initialize_student_content_blocks
from database import get_db

router = APIRouter()


# @router.post("/enroll/{course_id}", response_model=StudentCourseResponse)
# def enroll_student(
#     course_id: int, 
#     db: Session = Depends(get_db), 
#     current_user: User = Depends(get_current_user)
# ):
#     # Ensure that only students can enroll in courses
#     if current_user.role != Role.student:
#         raise HTTPException(status_code=403, detail="Only students can enroll in courses")

#     # Check if the course exists
#     course = db.query(Course).filter(Course.id == course_id).first()
#     if not course:
#         raise HTTPException(status_code=404, detail="Course not found")

#     # Check if the student is already enrolled in the course
#     existing_enrollment = db.query(StudentCourse).filter_by(
#         student_id=current_user.id,
#         course_id=course_id
#     ).first()
#     if existing_enrollment:
#         raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

#     # Enroll the student
#     student_course = StudentCourse(student_id=current_user.id, course_id=course_id)
#     db.add(student_course)
#     db.commit()
#     db.refresh(student_course)

#     # Initialize StudentContentBlock entries for this student and course
#     initialize_student_content_blocks(db=db, student_id=current_user.id, course_id=course_id)

#     return student_course

@router.post("/enroll/{course_id}", response_model=StudentCourseResponse)
def enroll_student(
    course_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Ensure only students can enroll in courses
    if current_user.role != Role.student:
        raise HTTPException(status_code=403, detail="Only students can enroll in courses")

    # Retrieve the course
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if the student is already enrolled
    existing_enrollment = db.query(StudentCourse).filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="You are already enrolled in this course")

    # If the course is paid, ensure payment is complete
    if course.is_paid_course:
        # Check if there's a successful payment for this course by the current user
        payment = db.query(Payment).filter(
            Payment.course_id == course_id,
            Payment.user_id == current_user.id,
            Payment.status == 'success'  # Ensure payment is confirmed
        ).first()

        if not payment:
            raise HTTPException(status_code=403, detail="Payment required before enrollment. Please complete the payment.")
    
    # Enroll the student in the course
    student_course = StudentCourse(student_id=current_user.id, course_id=course_id)
    db.add(student_course)
    db.commit()
    db.refresh(student_course)

    # Initialize StudentContentBlock entries for this student and course
    initialize_student_content_blocks(db=db, student_id=current_user.id, course_id=course_id)

    return student_course
