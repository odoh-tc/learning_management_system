from pydantic import BaseModel

class AnnouncementBase(BaseModel):
    title: str
    message: str
    # user_id: int

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(AnnouncementBase):
    pass


class AnnouncementResponse(AnnouncementBase):
    id: int

    class Config:
        orm_mode = True
