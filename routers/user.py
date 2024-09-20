from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Course, User
from schema.course import CourseResponse
from schema.profile import ProfileResponse
from schema.student_content_block import StudentContentBlockResponse
from schema.student_course import StudentCourseResponse
from schema.user import Role, UserCreate, AdminResponse, TeacherResponse, StudentResponse, UserResponse
from services.user import create_user_service, get_user, get_user_by_email, get_user_by_username, update_user_service, delete_user_service
from services.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=AdminResponse | TeacherResponse | StudentResponse)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    created_user = create_user_service(db=db, user=user)
    
    if created_user.role == Role.admin:
        return AdminResponse.from_orm(created_user)
    elif created_user.role == Role.teacher:
        return TeacherResponse.from_orm(created_user)
    else:
        return StudentResponse.from_orm(created_user)

@router.get("/{user_id}", response_model=AdminResponse | TeacherResponse | StudentResponse)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
): 
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.role == Role.admin:
        if db_user.role == Role.admin:
            return AdminResponse.from_orm(db_user)
        elif db_user.role == Role.teacher:
            return TeacherResponse.from_orm(db_user)
        else:
            return StudentResponse.from_orm(db_user)
    elif current_user.role == Role.teacher:
        if db_user.role == Role.teacher:
            return TeacherResponse.from_orm(db_user)
        elif db_user.role == Role.student:
            return StudentResponse.from_orm(db_user)
        else:
            raise HTTPException(status_code=403, detail="Permission denied")
    elif current_user.role == Role.student and db_user.id == current_user.id:
        return StudentResponse.from_orm(db_user)
    else:
        raise HTTPException(status_code=403, detail="Permission denied")




@router.get("/", response_model=AdminResponse | TeacherResponse | StudentResponse)
def get_user_details(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Use `from_orm` directly to convert the current user object
    if current_user.role == Role.admin:
        return AdminResponse.from_orm(current_user)
    elif current_user.role == Role.teacher:
        return TeacherResponse.from_orm(current_user)
    else:
        return StudentResponse.from_orm(current_user)

# @router.get("/", response_model=AdminResponse | TeacherResponse | StudentResponse)
# def get_user_details(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     if current_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     if current_user.role == Role.admin:
#         return AdminResponse.from_orm(current_user)
#     elif current_user.role == Role.teacher:
#         teacher_response = TeacherResponse(
#             id=current_user.id,
#             email=current_user.email,
#             username=current_user.username,
#             role=current_user.role,
#             is_active=current_user.is_active,
#             profile=ProfileResponse.from_orm(current_user.profile) if current_user.profile else None,
#             created_courses=[CourseResponse.from_orm(course) for course in current_user.created_courses]
#         )
#         return teacher_response
#     else:
#         student_response = StudentResponse(
#             id=current_user.id,
#             email=current_user.email,
#             username=current_user.username,
#             role=current_user.role,
#             is_active=current_user.is_active,
#             profile=ProfileResponse.from_orm(current_user.profile) if current_user.profile else None,
#             student_courses=[StudentCourseResponse.from_orm(course) for course in current_user.student_courses] if current_user.student_courses else [],
#             student_content_blocks=[StudentContentBlockResponse.from_orm(block) for block in current_user.student_content_blocks] if current_user.student_content_blocks else []
#         )
#         return student_response


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_user = update_user_service(db=db, user_id=user_id, user_data=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_user = delete_user_service(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
