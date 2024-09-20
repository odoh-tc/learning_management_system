from pydantic import BaseModel
from typing import Optional

class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    bio: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True  # Add this line

