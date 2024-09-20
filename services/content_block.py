from sqlalchemy.orm import Session
from schema.content_block import ContentBlockCreate, ContentBlockUpdate
from models import ContentBlock

def create_content_block(db: Session, content_block: ContentBlockCreate):
    db_content_block = ContentBlock(**content_block.dict())
    db.add(db_content_block)
    db.commit()
    db.refresh(db_content_block)
    return db_content_block

def update_content_block(db: Session, content_block_id: int, content_block: ContentBlockUpdate):
    db_content_block = db.query(ContentBlock).filter(ContentBlock.id == content_block_id).first()
    if db_content_block:
        for key, value in content_block.dict(exclude_unset=True).items():
            setattr(db_content_block, key, value)
        db.commit()
        db.refresh(db_content_block)
    return db_content_block

def delete_content_block(db: Session, content_block_id: int):
    db_content_block = db.query(ContentBlock).filter(ContentBlock.id == content_block_id).first()
    if db_content_block:
        db.delete(db_content_block)
        db.commit()
    return db_content_block

def get_content_block(db: Session, content_block_id: int):
    return db.query(ContentBlock).filter(ContentBlock.id == content_block_id).first()

def get_content_blocks_by_section(db: Session, section_id: int):
    return db.query(ContentBlock).filter(ContentBlock.section_id == section_id).all()
