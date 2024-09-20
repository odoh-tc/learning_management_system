from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List

from schema.message import MessageCreate, MessageResponse
from services.auth import get_current_user
from services.message import create_message, get_message, delete_message
from database import get_db
from models import User, Role
# from auth import get_current_user  # Assuming authentication function

router = APIRouter()

@router.websocket("/ws/messages/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            
            # Example logic to determine receiver dynamically
            # For demonstration, let's assume you fetch receiver_id from message data or session
            # Here's a hypothetical example of fetching receiver_id dynamically
            
            # Fetch receiver_id based on your application logic
            # For instance, you might have a service function or method to determine this
            
            receiver_id = get_receiver_id_from_logic(client_id, data, db)
            
            # Create a message object
            message_create = MessageCreate(
                sender_id=int(client_id),
                receiver_id=receiver_id,
                content=data
            )
            
            # Store the message in the database
            created_message = create_message(db=db, message=message_create, sender_id=int(client_id))
            
            # Optionally, broadcast the message to other clients
            # Example: broadcast_message(created_message)
            
            # Send confirmation back to the sender
            await websocket.send_text(f"Message sent: {data}")
    except WebSocketDisconnect:
        # Handle disconnection if needed
        pass
    finally:
        await websocket.close()




def get_receiver_id_from_logic(client_id: str, message_data: str, db: Session) -> int:
    # Implement your custom logic to determine receiver_id here
    # This could involve querying the database, processing the message_data, etc.
    
    # Example: Fetch receiver_id based on some condition (e.g., first user with a specific role)
    receiver = db.query(User).filter(User.role == Role.role).first()
    if receiver:
        return receiver.id
    else:
        # Handle scenario where receiver is not found
        raise HTTPException(status_code=404, detail="Receiver not found")

@router.post("/messages/", response_model=MessageResponse)
def send_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != message.sender_id:
        raise HTTPException(status_code=403, detail="Unauthorized to send message for another user")
    
    # Check if the receiver exists
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    return create_message(db=db, message=message)



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



@router.delete("/messages/{message_id}", response_model=MessageResponse)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_message = get_message(db=db, message_id=message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if current_user.role == Role.admin or current_user.id == db_message.sender_id or current_user.id == db_message.receiver_id:
        return delete_message(db=db, message_id=message_id)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this message")
