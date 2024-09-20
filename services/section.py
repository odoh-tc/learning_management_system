from sqlalchemy.orm import Session
from schema.section import SectionCreate, SectionUpdate
from models import Section

def create_section(db: Session, section: SectionCreate):
    db_section = Section(**section.dict())
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section

def update_section(db: Session, section_id: int, section: SectionUpdate):
    db_section = db.query(Section).filter(Section.id == section_id).first()
    if db_section:
        for key, value in section.dict(exclude_unset=True).items():
            setattr(db_section, key, value)
        db.commit()
        db.refresh(db_section)
    return db_section

def delete_section(db: Session, section_id: int):
    db_section = db.query(Section).filter(Section.id == section_id).first()
    if db_section:
        db.delete(db_section)
        db.commit()
    return db_section

def get_section(db: Session, section_id: int):
    return db.query(Section).filter(Section.id == section_id).first()

def get_sections_by_course(db: Session, course_id: int):
    return db.query(Section).filter(Section.course_id == course_id).all()
