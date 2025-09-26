from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.event import Enrollment, Event, Feedback, Resource
from ..models.user import User
from ..schemas.event import (
    EnrollmentCreate,
    EnrollmentRead,
    EventCreate,
    EventRead,
    EventUpdate,
    FeedbackCreate,
    FeedbackRead,
    ResourceCreate,
    ResourceRead,
)
from .deps import get_current_user

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(event_in: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = Event(**event_in.dict(), organizer_id=current_user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/", response_model=List[EventRead])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event


@router.put("/{event_id}", response_model=EventRead)
def update_event(
    event_id: int,
    event_in: EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to edit this event")
    for key, value in event_in.dict(exclude_unset=True).items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to delete this event")
    db.delete(event)
    db.commit()
    return None


@router.post("/{event_id}/enroll", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def enroll_event(
    event_id: int,
    enrollment_in: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    enrollment = Enrollment(user_id=current_user.id, event_id=event.id, status=enrollment_in.status)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.post("/{event_id}/resources", response_model=ResourceRead, status_code=status.HTTP_201_CREATED)
def add_resource(
    event_id: int,
    resource_in: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to add resources")
    resource = Resource(event_id=event.id, **resource_in.dict())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


@router.post("/{event_id}/feedback", response_model=FeedbackRead, status_code=status.HTTP_201_CREATED)
def add_feedback(
    event_id: int,
    feedback_in: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    feedback = Feedback(event_id=event.id, author_id=current_user.id, **feedback_in.dict())
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback
