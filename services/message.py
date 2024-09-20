from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Message
from schema.message import MessageCreate
from datetime import datetime

def create_message(db: Session, current_user_id: int, message: MessageCreate):
    if current_user_id == message.receiver_id:
        raise HTTPException(status_code=400, detail="You cannot send a message to yourself.")
    
    db_message = Message(
        sender_id=current_user_id,
        receiver_id=message.receiver_id,
        content=message.content,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()

def delete_message_service(db: Session, message_id: int):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
    return
