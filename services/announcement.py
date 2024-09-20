from sqlalchemy.orm import Session
from schema.announcement import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse
from models import Announcement
from models import User

def create_announcement(db: Session, announcement: AnnouncementCreate, current_user: User):
    # Remove `user_id` from `announcement` if it's included in `AnnouncementCreate`
    announcement_data = announcement.dict()
    announcement_data["user_id"] = current_user.id
    
    db_announcement = Announcement(**announcement_data)
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement


def get_announcement(db: Session, announcement_id: int):
    return db.query(Announcement).filter(Announcement.id == announcement_id).first()

def get_announcements(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Announcement).offset(skip).limit(limit).all()

def update_announcement(db: Session, announcement_id: int, announcement: AnnouncementUpdate):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if db_announcement:
        for key, value in announcement.dict(exclude_unset=True).items():
            setattr(db_announcement, key, value)
        db.commit()
        db.refresh(db_announcement)
    return db_announcement

def delete_announcement(db: Session, announcement_id: int):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if db_announcement:
        db.delete(db_announcement)
        db.commit()
    return db_announcement
