from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schema.announcement import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse
from services.announcement import (
    create_announcement, get_announcement, get_announcements, update_announcement, delete_announcement
)
from database import get_db
from models import User, Role
from services.auth import get_current_user


router = APIRouter()

@router.post("/announcements/", response_model=AnnouncementResponse)
def new_announcement(announcement: AnnouncementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [Role.admin, Role.teacher]:
        raise HTTPException(status_code=403, detail="Unauthorized to create announcements")
    return create_announcement(db=db, announcement=announcement, current_user=current_user)

@router.get("/announcements/{announcement_id}", response_model=AnnouncementResponse)
def read_announcement(announcement_id: int, db: Session = Depends(get_db)):
    return get_announcement(db=db, announcement_id=announcement_id)

@router.get("/announcements/", response_model=List[AnnouncementResponse])
def read_announcements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_announcements(db=db, skip=skip, limit=limit)

@router.put("/announcements/{announcement_id}", response_model=AnnouncementResponse)
def update_announcement_existing_announcement(
    announcement_id: int, announcement: AnnouncementUpdate, 
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    db_announcement = get_announcement(db=db, announcement_id=announcement_id)
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    if current_user.role == Role.admin or current_user.id == db_announcement.user_id:
        # Call the function to update the announcement
        return update_announcement(db=db, announcement_id=announcement_id, announcement=announcement)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized to update this announcement")




@router.delete("/announcements/{announcement_id}", response_model=AnnouncementResponse)
def delete_existing_announcement(
    announcement_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_announcement = get_announcement(db=db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    if current_user.role == Role.admin or current_user.id == db_announcement.user_id:
        return delete_announcement(db=db, announcement_id=announcement_id)
    elif current_user.role == Role.teacher:
        if current_user.id != db_announcement.user_id:
            raise HTTPException(status_code=403, detail="Unauthorized to delete this announcement")
        else:
            return delete_announcement(db=db, announcement_id=announcement_id)
    else:
        raise HTTPException(status_code=403, detail="Not authorized to delete announcements")