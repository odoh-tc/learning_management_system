from pydantic import BaseModel

class MessageBase(BaseModel):
    receiver_id: int
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    sender_id: int  # Still include sender_id in the response

    class Config:
        orm_mode = True
