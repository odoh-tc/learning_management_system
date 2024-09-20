from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schema.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from services import profile as profile_service
from models import User
from services.auth import get_current_user

router = APIRouter()



@router.post("/", response_model=ProfileResponse)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile_data = profile.dict()
    profile_data['user_id'] = current_user.id  # Set the user_id from the authenticated user
    return profile_service.create_profile(db=db, profile_data=profile_data)

@router.put("/{profile_id}", response_model=ProfileResponse)
def update_profile(profile_id: int, profile: ProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return profile_service.update_profile(db=db, profile_id=profile_id, profile=profile, current_user=current_user)

@router.delete("/{profile_id}", response_model=ProfileResponse)
def delete_profile(profile_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return profile_service.delete_profile(db=db, profile_id=profile_id, current_user=current_user)

@router.get("/{profile_id}", response_model=ProfileResponse)
def read_user_profile(profile_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = profile_service.get_profile(db=db, profile_id=profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/user/{user_id}", response_model=ProfileResponse)
def read_user_profile_by_user_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = profile_service.get_profile_by_user_id(db=db, user_id=user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
