from sqlalchemy.orm import Session
from schema.profile import ProfileCreate, ProfileUpdate
from models import Profile
from models import User  # Import the User model to check roles
from fastapi import HTTPException


def create_profile(db: Session, profile_data: dict):
    db_profile = Profile(**profile_data)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, profile_id: int, profile: ProfileUpdate, current_user: User):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Only allow users to update their own profile or admins to update any profile
    if db_profile.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to update this profile")

    for key, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, key, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int, current_user: User):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Only admins should be able to delete profiles
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to delete profiles")

    db.delete(db_profile)
    db.commit()
    return db_profile

def get_profile(db: Session, profile_id: int):
    return db.query(Profile).filter(Profile.id == profile_id).first()

def get_profile_by_user_id(db: Session, user_id: int):
    return db.query(Profile).filter(Profile.user_id == user_id).first()
