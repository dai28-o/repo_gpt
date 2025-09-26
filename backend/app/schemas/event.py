from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from ..models.event import EnrollmentStatus
from .user import UserRead


class ResourceBase(BaseModel):
    url: Optional[str] = None
    filename: Optional[str] = None
    description: Optional[str] = None


class ResourceCreate(ResourceBase):
    pass


class ResourceRead(ResourceBase):
    id: int

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    title: str
    description: str
    tags: Optional[str] = None
    capacity: int
    start_time: datetime
    end_time: datetime
    location: str


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    tags: Optional[str]
    capacity: Optional[int]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    location: Optional[str]


class EventRead(EventBase):
    id: int
    organizer: UserRead
    resources: List[ResourceRead] = Field(default_factory=list)

    class Config:
        orm_mode = True


class EnrollmentBase(BaseModel):
    status: EnrollmentStatus = EnrollmentStatus.REGISTERED


class EnrollmentCreate(EnrollmentBase):
    event_id: int


class EnrollmentRead(EnrollmentBase):
    id: int
    user: UserRead

    class Config:
        orm_mode = True


class FeedbackBase(BaseModel):
    rating: int
    comment: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    event_id: int


class FeedbackRead(FeedbackBase):
    id: int
    author: UserRead
    created_at: datetime

    class Config:
        orm_mode = True
