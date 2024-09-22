from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List

from schema.message import MessageCreate, MessageResponse
from services.auth import get_current_user
from services.message import create_message, delete_message_service, get_message
from database import get_db
from models import User, Role
# from auth import get_current_user  # Assuming authentication function

router = APIRouter()



@router.post("/messages/", response_model=MessageResponse)
def send_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    # Check if the receiver exists
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    return create_message(db=db, current_user_id=current_user.id, message=message)



@router.get("/messages/{message_id}", response_model=MessageResponse)
def read_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_message = get_message(db=db, message_id=message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if current_user.id != db_message.sender_id and current_user.id != db_message.receiver_id:
        raise HTTPException(status_code=403, detail="Unauthorized to access this message") 
    return db_message



@router.delete("/messages/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Make sure current_user is a User instance
):
    db_message = get_message(db=db, message_id=message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Check role and ownership
    if current_user.role == Role.admin or current_user.id in (db_message.sender_id, db_message.receiver_id):
        return delete_message_service(db=db, message_id=message_id)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this message")

