from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.event import Event
from ..models.user import User
from ..schemas.event import EventRead
from ..schemas.user import UserRead
from .deps import get_admin_user

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(get_admin_user)])


@router.get("/users", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/events", response_model=List[EventRead])
def list_all_events(db: Session = Depends(get_db)):
    return db.query(Event).all()
