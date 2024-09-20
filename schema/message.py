from pydantic import BaseModel

class MessageBase(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int

    class Config:
        orm_mode = True
